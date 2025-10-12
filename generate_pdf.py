from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import green, black
import random
import os

# === Random Clinic Names ===
clinic_names = [
    "Sunrise Medical Center",
    "TruHeal Clinic",
    "Apollo Family Care",
    "MedSyn Health Hub",
    "St. Mary’s Health Point"
]

def generate_prescription(patient_image, signature_image, pdf_path):
    """Generate a single synthetic prescription PDF with random consent image."""
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    border_margin = 0.4 * inch
    inner_margin = 0.3 * inch

    # === Outer Border ===
    c.setLineWidth(3)
    c.setStrokeColor(black)
    c.rect(border_margin, border_margin, width - 2 * border_margin, height - 1.5 * border_margin)

    # === Header (Clinic Name) ===
    header_height = 1.3 * inch
    c.setLineWidth(2.5)
    c.setStrokeColor(green)
    c.rect(border_margin + inner_margin, height - border_margin - header_height,
           width - 2 * (border_margin + inner_margin), header_height)
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(green)
    clinic_name = random.choice(clinic_names)
    c.drawCentredString(width / 2, height - border_margin - header_height / 2 + 6, clinic_name)

    # === Content Box (Patient Info) ===
    content_y_top = height - border_margin - 1.2 * header_height + 1.8 * inner_margin
    content_height = content_y_top - border_margin - 2 * inch
    c.setLineWidth(2)
    c.setStrokeColor(green)
    c.rect(border_margin + inner_margin, border_margin + 1.5 * inch,
           width - 2 * (border_margin + inner_margin), content_height)

    # === Field Labels ===
    labels = ["Name", "Date of Birth", "Main Complaint", "Allergies", "Medications", "Insurance"]
    label_x = border_margin + 1 * inch
    image_x = width / 2.5
    start_y = content_y_top - 1.5 * inch
    gap = 0.8 * inch

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(green)
    y = start_y
    for label in labels:
        c.drawString(label_x, y, label + ":")
        y -= gap

    # === Patient Image (Right Side) ===
    if os.path.exists(patient_image):
        image_width = 4.1 * inch
        image_height = len(labels) * gap * 1.2
        c.drawImage(patient_image, image_x, start_y - image_height + 0.8 * inch,
                    width=image_width, height=image_height, mask='auto')

    # === Random Consent Image (from 'generated/' folder) ===
    consent_folder = "generated/"
    consent_images = [os.path.join(consent_folder, f) for f in os.listdir(consent_folder)
                  if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if consent_images:
        consent_image = random.choice(consent_images)

    # Bottom of patient details
    patient_details_bottom = start_y - len(labels) * gap - 0.1*inch  # slight gap after last label

    # Top of footer
    footer_height = 1 * inch
    footer_top = border_margin + footer_height + inner_margin + 0.05*inch

    # Available height for consent image (3/4 of vertical space)
    available_height = patient_details_bottom - footer_top
    consent_height = available_height * 0.75

    # Maximum width inside borders
    max_consent_width = width - 2 * (border_margin + inner_margin)

    # Load image and preserve aspect ratio
    from PIL import Image as PILImage
    pil_img = PILImage.open(consent_image)
    w, h = pil_img.size
    aspect_ratio = w / h

    # Scale width and height proportionally
    if consent_height * aspect_ratio <= max_consent_width:
        consent_w = consent_height * aspect_ratio
        consent_h = consent_height
    else:
        consent_w = max_consent_width
        consent_h = max_consent_width / aspect_ratio

    # Increase width by 20% but stay within max width
    consent_w = min(consent_w * 1.2, max_consent_width)
    consent_h = consent_w / aspect_ratio  # adjust height to preserve ratio

    # Slightly raise the image (shift up)
    shift_up = 0.6 * inch
    consent_y = footer_top + shift_up

    # Draw the consent image, centered horizontally
    c.drawImage(
        consent_image,
        border_margin + inner_margin + (max_consent_width - consent_w)/2,
        consent_y,
        width=consent_w,
        height=consent_h,
        preserveAspectRatio=True,
        mask='auto'
    )


    # === Footer (Doctor Signature Section) ===
    footer_height = 1 * inch
    c.setLineWidth(2)
    c.setStrokeColor(green)
    c.rect(border_margin + inner_margin, border_margin + inner_margin,
           width - 2 * (border_margin + inner_margin), footer_height)

    # === Doctor Signature ===
    if signature_image and os.path.exists(signature_image):
        sig_w = 2.5 * inch
        sig_h = 0.7 * inch
        sig_x = width - border_margin - inner_margin - sig_w - 0.2 * inch
        sig_y = border_margin + inner_margin + 0.15 * inch
        c.drawImage(signature_image, sig_x, sig_y, width=sig_w, height=sig_h, mask='auto')

    # === Footer Text ===
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(black)
    c.drawString(border_margin + inner_margin, border_margin + inner_margin / 2,
                 "Generated by MedSyn Form System")

    c.save()
    print(f"✅ Prescription PDF saved at: {pdf_path}")


# === Example Usage ===
if __name__ == "__main__":
    generate_prescription(
        patient_image="patient_sample.png",   # Replace with your actual path
        signature_image="doctor_sign.png",    # Replace with your actual path
        pdf_path="final_prescription.pdf"
    )

