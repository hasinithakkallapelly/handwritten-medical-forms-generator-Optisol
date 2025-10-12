import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# === Directories ===
FONTS_DIR = "fonts/"
OUTPUT_DIR = "generated/"
os.makedirs(FONTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Utility: Random blue ink shade ===
def random_blue_ink():
    """Return a random natural blue ink shade (slightly varied)."""
    base_blues = [
        (10, 40, 120), (15, 50, 140), (20, 60, 160),
        (25, 70, 180), (30, 80, 200), (35, 90, 220), (40, 100, 240)
    ]
    return random.choice(base_blues)

# === Decorations ===
def draw_strikeout(draw, bbox, font_size, color=(0,0,0), opacity=150):
    """Draw subtle human-like strikeout below center of word."""
    x0, y0, x1, y1 = bbox
    y_center = y0 + (y1 - y0) * 0.8
    thickness = max(1, font_size // 12)
    num_waves = random.randint(1, 3)
    points = []
    for i in range(num_waves + 1):
        xi = x0 + i * (x1 - x0) / num_waves
        yi = y_center + random.uniform(-thickness / 2, thickness / 2)
        points.append((xi, yi))
    draw.line(points, fill=color + (opacity,), width=thickness)

def draw_scribble(draw, bbox, font_size, color=(0,0,0), opacity=100):
    """Draw subtle human-like scribble over word."""
    x0, y0, x1, y1 = bbox
    thickness = max(1, font_size // 18)
    num_points = random.randint(5, 10)
    points = []
    for i in range(num_points):
        xi = random.uniform(x0, x1)
        yi = random.uniform(y0, y1)
        points.append((xi, yi))
    draw.line(points, fill=color + (opacity,), width=thickness)

# === Text rendering ===
def text_to_image(
    text,
    image_width=1000,
    margin=50,
    line_height=None,
    char_spacing=-4,
    blur_strength=(0.3, 0.8),
    rotation_range=(-2, 2),
    strikeout_prob=0.05,
    scribble_prob=0.05
):
    """Render long paragraph neatly wrapped and handwritten."""
    fonts = [os.path.join(FONTS_DIR, f) for f in os.listdir(FONTS_DIR) if f.endswith(".ttf")]
    if not fonts:
        raise ValueError("❌ No fonts found in 'fonts/' folder. Please add some .ttf handwriting fonts.")

    font_path = random.choice(fonts)
    font_size = random.randint(46, 58)
    font = ImageFont.truetype(font_path, font_size)

    wrapper = textwrap.TextWrapper(width=60)
    wrapped_lines = wrapper.wrap(text)

    if line_height is None:
        line_height = font_size + 20

    img_height = line_height * len(wrapped_lines) + margin * 2
    img = Image.new("RGBA", (image_width, img_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    ink_color = random_blue_ink()
    opacity = random.randint(200, 255)
    space_width = font.getbbox(" ")[2] - font.getbbox(" ")[0]

    y = margin
    for line in wrapped_lines:
        x = margin
        for word in line.split(" "):
            word_start_x = x
            for ch in word:
                draw.text((x, y), ch, font=font, fill=ink_color + (opacity,))
                bbox = font.getbbox(ch)
                ch_width = bbox[2] - bbox[0]
                x += ch_width + char_spacing
            word_end_x = x
            word_bbox = (word_start_x, y, word_end_x, y + font_size)

            if random.random() < strikeout_prob:
                draw_strikeout(draw, word_bbox, font_size, color=ink_color, opacity=opacity)
            if random.random() < scribble_prob:
                draw_scribble(draw, word_bbox, font_size, color=ink_color, opacity=opacity)

            x += space_width + char_spacing

        y += line_height

    img = img.rotate(random.uniform(*rotation_range), expand=1, fillcolor=(255, 255, 255, 255))
    img = img.filter(ImageFilter.GaussianBlur(random.uniform(*blur_strength)))
    return img.convert("RGB")

# === Consent Paragraphs ===
consent_form_paragraphs = [
    "I hereby give my full consent to receive medical treatment and care as advised by the attending doctor. I understand that this includes diagnostic tests, medication, and other necessary medical procedures as part of my treatment plan.",
    "The nature and purpose of the proposed procedure have been clearly explained to me. I have been given sufficient information to understand why the procedure is being performed and what it aims to achieve.",
    "I acknowledge that the doctor has made no promises or guarantees regarding the outcome or success of the procedure. I understand that results may vary depending on my health condition and response to treatment.",
    "I have been informed of the potential risks, complications, and side effects associated with the proposed medical procedure. I understand that while every effort will be made to ensure my safety, unforeseen events can still occur.",
    "I understand that I have the right to withdraw my consent for treatment at any stage before the procedure begins. I am aware that such withdrawal may affect the continuity or success of my treatment plan.",
]

# === Function to Generate N Handwriting Images ===
def generate_consent_images(n=10):
    """
    Generate n handwriting-style consent form images.
    Randomly reuses paragraphs if n > available paragraphs.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"🧠 Generating {n} consent handwriting images...")

    for i in range(1, n + 1):
        paragraph = random.choice(consent_form_paragraphs)  # random reuse
        img = text_to_image(paragraph)
        output_path = os.path.join(OUTPUT_DIR, f"consent_{i}.png")
        img.save(output_path)
        print(f"✅ Saved {output_path}")

    print(f"\n🎉 All {n} consent paragraphs generated successfully!")

# === Example Run ===
generate_consent_images(50)
