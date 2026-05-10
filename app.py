from __future__ import annotations

import base64
import random
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from generate_pdf import generate_medical_form
from handwriting_generator import generate_handwriting_dataset


st.set_page_config(layout="wide", page_title="MedSyn Synthetic Medical Forms")

FORM_TYPES = ["Prescription Form", "Patient Intake Form", "Lab Request Form"]
OUTPUT_DIR = Path("generated_pdfs")
PATIENT_IMAGE_DIR = Path("patient_images")
CLEAN_IMAGE_DIR = Path("clean_img")
SIGNATURE_DIR = Path("signatures")


def _signature_images() -> list[str]:
    if not SIGNATURE_DIR.exists():
        return []
    return [str(path) for path in SIGNATURE_DIR.iterdir() if path.suffix.lower() in {".png", ".jpg", ".jpeg"}]


def _pdf_preview(path: str) -> None:
    with open(path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("utf-8")
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{encoded}" width="100%" height="560" type="application/pdf"></iframe>',
        unsafe_allow_html=True,
    )


def _zip_files(pdf_paths: list[str]) -> str:
    zip_path = OUTPUT_DIR / "synthetic_medical_forms.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for file in pdf_paths:
            zipf.write(file, Path(file).name)
    return str(zip_path)


for directory in (OUTPUT_DIR, PATIENT_IMAGE_DIR, CLEAN_IMAGE_DIR):
    directory.mkdir(exist_ok=True)

st.title("MedSyn Synthetic Medical Forms")
st.caption("Generate privacy-safe handwritten medical PDFs for OCR demos, training prototypes, and document AI experiments.")

with st.sidebar:
    st.header("Generation")
    num_forms = st.number_input("Forms", min_value=1, max_value=250, value=5, step=1)
    form_type = st.selectbox("Form type", FORM_TYPES)
    include_signatures = st.toggle("Doctor signatures", value=True)
    noise_std = st.slider("Scan noise", 0.0, 25.0, 10.0, 1.0)
    warp_strength = st.slider("Handwriting warp", 0.0, 5.0, 2.0, 0.5)
    strikeout_prob = st.slider("Strikeouts", 0.0, 0.15, 0.03, 0.01)
    scribble_prob = st.slider("Scribbles", 0.0, 0.15, 0.03, 0.01)

left, right = st.columns([0.62, 0.38])

with left:
    st.subheader("Generator")
    st.write("Create synthetic records, render handwriting, place the result on medical templates, then export PDFs.")
    generate = st.button("Generate forms", type="primary", use_container_width=True)

with right:
    st.subheader("Repository health")
    st.metric("Supported templates", len(FORM_TYPES))
    st.metric("Synthetic only", "Yes")

if generate:
    signatures = _signature_images() if include_signatures else []

    progress = st.progress(0)
    status = st.empty()
    status.write("Generating handwriting samples...")

    try:
        records = generate_handwriting_dataset(
            n=int(num_forms),
            clean_dir=str(CLEAN_IMAGE_DIR),
            clumsy_dir=str(PATIENT_IMAGE_DIR),
            form_type=form_type,
            warp_strength=float(warp_strength),
            noise_std=float(noise_std),
            strikeout_prob=float(strikeout_prob),
            scribble_prob=float(scribble_prob),
        )
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    generated_files: list[str] = []
    for index, record in enumerate(records, start=1):
        status.write(f"Rendering PDF {index} of {len(records)}...")
        signature = random.choice(signatures) if signatures else None
        pdf_path = OUTPUT_DIR / f"{form_type.lower().replace(' ', '_')}_{index:03d}.pdf"
        generate_medical_form(
            handwriting_image=str(record["handwriting_image"]),
            signature_image=signature,
            pdf_path=str(pdf_path),
            patient=record["patient"],
            form_type=form_type,
        )
        generated_files.append(str(pdf_path))
        progress.progress(index / len(records))

    zip_path = _zip_files(generated_files)
    status.empty()
    st.success(f"Generated {len(generated_files)} synthetic {form_type.lower()} PDFs.")

    preview_record = records[0]
    preview_pdf = generated_files[0]
    preview_patient = preview_record["patient"]

    tab_pdf, tab_handwriting, tab_data, tab_downloads = st.tabs(["PDF preview", "Handwriting", "Data profile", "Downloads"])
    with tab_pdf:
        _pdf_preview(preview_pdf)
    with tab_handwriting:
        st.image(str(preview_record["handwriting_image"]), use_container_width=True)
    with tab_data:
        patients = pd.DataFrame([record["patient"] for record in records])
        st.dataframe(patients, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            patients["condition"].value_counts().plot(kind="bar", ax=ax)
            ax.set_title("Generated conditions")
            ax.set_xlabel("")
            ax.set_ylabel("Forms")
            st.pyplot(fig)
        with col2:
            fig2, ax2 = plt.subplots()
            patients["age"].plot(kind="hist", bins=8, ax=ax2)
            ax2.set_title("Synthetic age distribution")
            ax2.set_xlabel("Age")
            st.pyplot(fig2)

        st.info(f"Preview patient: {preview_patient['name']} | {preview_patient['condition']} | {preview_patient['medications']}")
    with tab_downloads:
        with open(preview_pdf, "rb") as file:
            st.download_button("Download preview PDF", file, file_name=Path(preview_pdf).name, mime="application/pdf")
        with open(zip_path, "rb") as file:
            st.download_button("Download all PDFs as ZIP", file, file_name="synthetic_medical_forms.zip", mime="application/zip")
else:
    st.info("Choose generation settings in the sidebar, then generate a batch to preview and download.")
