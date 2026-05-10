# MedSyn Synthetic Medical Form Generator

MedSyn creates privacy-safe synthetic medical forms that look handwritten, scanned, and varied enough to support demos, OCR experiments, and training-data prototypes without exposing real patient records.

The project combines realistic fake patient data, handwriting-style rendering, visual noise, signature overlays, and PDF generation into a Streamlit app.

## Why It Matters

Medical forms often contain protected health information, which makes real handwritten data difficult to share for AI development. This project generates fully synthetic records so teams can test document-processing workflows while avoiding real patient data.

## Features

- Generate batches of synthetic prescription, intake, and lab request forms
- Create coherent fake patient records with complaints, diagnoses, allergies, and medication rules
- Render handwriting with font variation, blur, noise, warp, strikeouts, and scribbles
- Add optional synthetic doctor signatures
- Preview generated handwriting and PDF output inside the Streamlit app
- Download individual PDFs or a ZIP archive
- Keep generated runtime files out of Git with a focused `.gitignore`

## Tech Stack

- Python
- Streamlit
- Faker
- Pillow
- OpenCV
- ReportLab
- Pandas and Matplotlib

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app expects at least one `.ttf` handwriting-style font in the `fonts/` directory. Signature PNGs in `signatures/` are optional.

## Project Structure

```text
.
├── app.py                    # Streamlit product demo
├── data_generator.py         # Coherent synthetic patient data
├── handwriting_generator.py  # Handwriting image generation
├── generate_pdf.py           # Medical form PDF renderer
├── main.py                   # Small CLI smoke example
├── fonts/                    # Handwriting fonts
├── signatures/               # Optional synthetic signatures
├── templates/                # Future JSON templates
└── requirements.txt
```

Generated files are written to `generated_pdfs/`, `patient_images/`, `clean_img/`, and `outputs/`. Those folders are intentionally ignored by Git.

## How It Works

1. `data_generator.py` creates fake patient records with rule-based medical consistency.
2. `handwriting_generator.py` renders those records into handwriting-like images.
3. `generate_pdf.py` places the handwriting on realistic medical form layouts.
4. `app.py` gives users controls, previews, metrics, and downloads.

## Suggested Next Steps

- Add a live Streamlit Community Cloud deployment link
- Add screenshots or a short GIF of the UI to this README
- Add tests for medication-allergy consistency and PDF generation
- Add more form templates from JSON metadata
- Export metadata as CSV alongside the PDFs

## Privacy Note

All generated records are synthetic. The output should still be labeled as synthetic data so downstream users do not confuse it with real clinical documentation.
