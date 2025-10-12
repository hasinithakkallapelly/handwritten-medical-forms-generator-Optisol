# ==========================================
# HANDWRITING IMAGE GENERATOR + CLUMSINESS AI + HUMAN-LIKE STRIKEOUTS & SCRIBBLES
# ==========================================

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, os, numpy as np, cv2
from data_generator import generate_fake_patient

# ------------------------------
# CONFIG
# ------------------------------
FONTS_DIR = "fonts"
OUTPUT_DIR = "output"
CLEAN_DIR = os.path.join(OUTPUT_DIR, "clean")
CLUMSY_DIR = os.path.join(OUTPUT_DIR, "clumsy")

os.makedirs(FONTS_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(CLUMSY_DIR, exist_ok=True)

# ------------------------------
# FUNCTIONS
# ------------------------------

def draw_strikeout(draw, bbox, font_size, color=(0,0,0), opacity=150):
    """Draw subtle human-like strikeout below center of word."""
    x0, y0, x1, y1 = bbox
    y_center = y0 + (y1 - y0) * 0.8  # below center
    thickness = max(1, font_size // 12)  # thinner than before
    num_waves = random.randint(1,3)  # smaller waves for subtlety
    points = []
    for i in range(num_waves+1):
        xi = x0 + i*(x1-x0)/num_waves
        yi = y_center + random.uniform(-thickness/2, thickness/2)
        points.append((xi, yi))
    draw.line(points, fill=color+(opacity,), width=thickness)

def draw_scribble(draw, bbox, font_size, color=(0,0,0), opacity=100):
    """Draw subtle human-like scribble over word."""
    x0, y0, x1, y1 = bbox
    thickness = max(1, font_size // 18)  # thinner lines
    num_points = random.randint(5, 10)  # fewer points
    points = []
    for i in range(num_points):
        xi = random.uniform(x0, x1)
        yi = random.uniform(y0, y1)
        points.append((xi, yi))
    draw.line(points, fill=color+(opacity,), width=thickness)

def text_list_to_image(
    text_list,
    image_width=1024,
    line_height=100,
    char_spacing=-6,
    blur_strength=(0.3, 0.8),
    rotation_range=(-3, 3),
    strikeout_prob=0.05,  # rare
    scribble_prob=0.05    # rare
):
    """Render list of text lines in handwriting style with subtle strikeouts and scribbles."""
    fonts = [os.path.join(FONTS_DIR, f) for f in os.listdir(FONTS_DIR) if f.endswith(".ttf")]
    if not fonts:
        raise ValueError("❌ No fonts found in 'fonts/' folder.")

    font_path = random.choice(fonts)
    font_size = random.randint(50, 70)
    font = ImageFont.truetype(font_path, font_size)
    img_height = line_height * len(text_list) + 40
    img = Image.new("RGBA", (image_width, img_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    color = random.randint(0, 30)
    opacity = random.randint(180, 255)
    space_width = font.getbbox(" ")[2] - font.getbbox(" ")[0]

    y = 20
    for text in text_list:
        x = 20
        for word in text.split(" "):
            word_start_x = x
            for ch in word:
                draw.text((x, y), ch, font=font, fill=(color, color, color, opacity))
                bbox = font.getbbox(ch)
                ch_width = bbox[2] - bbox[0]
                x += ch_width + char_spacing
            word_end_x = x
            word_bbox = (word_start_x, y, word_end_x, y + font_size)

            if random.random() < strikeout_prob:
                draw_strikeout(draw, word_bbox, font_size, color=(color,color,color), opacity=opacity)

            if random.random() < scribble_prob:
                draw_scribble(draw, word_bbox, font_size, color=(color,color,color), opacity=opacity)

            x += space_width + char_spacing

        y += line_height

    img = img.rotate(random.uniform(*rotation_range), expand=1, fillcolor=(255, 255, 255, 255))
    img = img.filter(ImageFilter.GaussianBlur(random.uniform(*blur_strength)))
    return img.convert("RGB")

def apply_random_warp(image, warp_strength=2):
    img = np.array(image)
    h, w, _ = img.shape
    dx = (np.random.rand(h, w) - 0.5) * warp_strength
    dy = (np.random.rand(h, w) - 0.5) * warp_strength
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    map_x = (x + dx).astype(np.float32)
    map_y = (y + dy).astype(np.float32)
    warped = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return warped

# # ------------------------------
# # MAIN
# # ------------------------------
# if __name__ == "__main__":
#     n = 20
#     print(f"🧠 Generating {n} handwriting samples...")

#     for i in range(n):
#         text_lines = generate_fake_patient()

#         clean_img = text_list_to_image(text_lines)
#         clean_path = os.path.join(CLEAN_DIR, f"patient_{i}_clean.png")
#         clean_img.save(clean_path)

#         np_img = np.array(clean_img)
#         noise = np.random.normal(0, 10, np_img.shape).astype(np.int16)
#         np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
#         np_img = apply_random_warp(np_img, warp_strength=2)
#         clumsy_img = cv2.GaussianBlur(np_img, (3, 3), sigmaX=0.5)
#         clumsy_path = os.path.join(CLUMSY_DIR, f"patient_{i}_clumsy.png")
#         Image.fromarray(clumsy_img).save(clumsy_path)

#         print(f"✅ Saved: {clean_path} and {clumsy_path}")

#     print("\n🎉 Done!")
#     print(f"→ Clean images:  {CLEAN_DIR}")
#     print(f"→ Clumsy images: {CLUMSY_DIR}")
 # replace with actual import

def generate_handwriting_dataset(
    n=20,
    clean_dir="clean_img",
    clumsy_dir="patient_images",
    warp_strength=2,
    noise_std=10
):
    """Generate clean and clumsy handwriting images and save them to folders."""
    
    os.makedirs(clean_dir, exist_ok=True)
    os.makedirs(clumsy_dir, exist_ok=True)

    print(f"🧠 Generating {n} handwriting samples...")

    for i in range(n):
        text_lines = generate_fake_patient()

        # Clean image
        clean_img = text_list_to_image(text_lines)
        clean_path = os.path.join(clean_dir, f"sample_{i}_clean.png")
        clean_img.save(clean_path)

        # Clumsy version
        np_img = np.array(clean_img)
        noise = np.random.normal(0, noise_std, np_img.shape).astype(np.int16)
        np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
        np_img = apply_random_warp(np_img, warp_strength=warp_strength)
        clumsy_img = cv2.GaussianBlur(np_img, (3, 3), sigmaX=0.5)
        clumsy_path = os.path.join(clumsy_dir, f"p{i}.jpg")
        Image.fromarray(clumsy_img).save(clumsy_path)

        print(f"✅ Saved: {clean_path} and {clumsy_path}")

    print("\n🎉 Done!")
    print(f"→ Clean images:  {clean_dir}")
    print(f"→ Clumsy images: {clumsy_dir}")
