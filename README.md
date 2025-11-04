# Problem Statement
Develop an **AI tool** that generates **realistic synthetic handwritten data** for **medical state forms** in **PDF format**.  
This enables **safe training of niche AI models** while addressing **privacy** and **data scarcity** issues.  

## Architecture
1. **Fake Data Generator** – Uses *Faker* to create synthetic patient data.  
2. **Handwriting Synthesizer** – Converts text into handwriting using fonts or GANs.  
3. **PDF Renderer** – Embeds handwriting into medical form templates using *ReportLab* or *OpenCV*.  
4. **Output Module** – Exports the final synthetic handwritten forms as high-fidelity PDFs.  

## Tech Stack
- **Language:** Python  
- **Data Generation:** Faker  
- **Handwriting Simulation:** PyTorch / TensorFlow, Handwriting Fonts, GANs  
- **Image Processing:** OpenCV, Pillow  
- **PDF Generation:** ReportLab  
- **Optional UI:** Streamlit or Flask  
