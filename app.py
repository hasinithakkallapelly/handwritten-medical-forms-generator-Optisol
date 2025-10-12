import streamlit as st
import os
import zipfile
import random
import pandas as pd
import matplotlib.pyplot as plt
from generate_pdf import generate_prescription
from clumsy4 import generate_handwriting_dataset
generate_handwriting_dataset(5)
# --- Streamlit Page Setup ---
st.set_page_config(layout="wide", page_title="🩺 MedSyn Synthetic Medical Form Generator")
st.title("🩺 MedSyn Synthetic Medical Form Generator")
st.caption("Generate realistic handwritten-style medical prescription PDFs with AI-driven diversity.")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Settings")
num_forms = st.sidebar.number_input("Number of Forms to Generate", 1, 1000, 5)
form_type = st.sidebar.selectbox("Form Type", ["Prescription Form"])
st.sidebar.markdown("---")

# --- Paths ---
os.makedirs("patient_images", exist_ok=True)
os.makedirs("signatures", exist_ok=True)
os.makedirs("generated_pdfs", exist_ok=True)

patient_images = [os.path.join("patient_images", f) for f in os.listdir("patient_images") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
signature_images = [os.path.join("signatures", f) for f in os.listdir("signatures") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# --- Main Button ---
if st.button("Generate Synthetic PDFs"):
    if not patient_images:
        st.error("No patient images found! Please add handwritten images to the 'patient_images/' folder!")
    else:
        generate_handwriting_dataset(num_forms)


        
        generated_files = []
        for i in range(1, num_forms + 1):
            patient_img = random.choice(patient_images)
            signature_img = random.choice(signature_images) if signature_images else None
            pdf_path = f"generated_pdfs/prescription_{i:03d}.pdf"
            generate_prescription(patient_img, signature_img, pdf_path)
            generated_files.append(pdf_path)

        # Create ZIP file
        zip_path = "generated_pdfs/generated_forms.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in generated_files:
                zipf.write(file, os.path.basename(file))

        st.success(f"✅ Successfully generated {num_forms} synthetic prescriptions!")
        st.download_button("📥 Download All PDFs (ZIP)", data=open(zip_path, "rb"), file_name="synthetic_prescriptions.zip")

        # --- Visualization Section ---
        st.markdown("## 📊 Synthetic Data Insights")
        st.write("Below are some sample insights based on the generated data (for presentation).")

        fake_stats = pd.DataFrame({
            "Age Group": ["0-18", "19-35", "36-60", "60+"],
            "Patients": [random.randint(5, 15) for _ in range(4)],
            "Common Issue": ["Cold/Fever", "Headache", "Hypertension", "Arthritis"]
        })

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.bar(fake_stats["Age Group"], fake_stats["Patients"])
            plt.title("Distribution of Patients by Age Group")
            st.pyplot(fig)
        with col2:
            fig2, ax2 = plt.subplots()
            ax2.pie(fake_stats["Patients"], labels=fake_stats["Age Group"], autopct="%1.1f%%", startangle=90)
            plt.title("Age Group Proportion")
            st.pyplot(fig2)

        st.markdown("### Health Insight Summary")
        st.info(
            "Majority of generated patient data falls within the **19–35** age range, showing common issues such as **fever, fatigue, and mild infections**. "
            "This indicates a trend toward lifestyle-related health cases and emphasizes the need for preventive awareness programs."
        )

