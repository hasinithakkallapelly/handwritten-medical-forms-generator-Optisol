#Problem Statement

Develop an AI tool that generates realistic synthetic handwritten data for medical state forms in PDF format.
This enables safe training of niche AI models while addressing privacy and data scarcity issues.

In healthcare, handwritten forms are still common, but real data cannot be shared due to privacy regulations like HIPAA and GDPR.
This project synthetically generates medical forms that look authentic but use entirely fake data, ensuring privacy-safe AI development.

#Architecture

Fake Data Generator – Uses Faker library to create synthetic patient data.

Handwriting Synthesizer – Converts text into handwriting using fonts, GAN models, or stroke-level simulation.

PDF Renderer – Embeds the synthesized handwriting into medical form templates using ReportLab, Pillow, or OpenCV.

Output Module – Exports the final synthetic handwritten medical forms as high-fidelity PDF files.

#Tech Stack

Language: Python

Data Generation: Faker

Handwriting Simulation: PyTorch / TensorFlow, Handwriting Fonts, GANs

Image Processing: OpenCV, Pillow

PDF Generation: ReportLab

Optional UI: Streamlit or Flask
