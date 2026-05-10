from __future__ import annotations

import os
import random
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from data_generator import generate_fake_patient, patient_to_lines


FONTS_DIR = Path("fonts")


def _available_fonts() -> list[Path]:
    return sorted(FONTS_DIR.glob("*.ttf"))


def draw_strikeout(draw: ImageDraw.ImageDraw, bbox: tuple[float, float, float, float], font_size: int, color: tuple[int, int, int], opacity: int) -> None:
    x0, y0, x1, y1 = bbox
    y_center = y0 + (y1 - y0) * 0.72
    thickness = max(1, font_size // 14)
    points = []
    waves = random.randint(1, 3)
    for i in range(waves + 1):
        xi = x0 + i * (x1 - x0) / waves
        yi = y_center + random.uniform(-thickness, thickness)
        points.append((xi, yi))
    draw.line(points, fill=color + (opacity,), width=thickness)


def draw_scribble(draw: ImageDraw.ImageDraw, bbox: tuple[float, float, float, float], font_size: int, color: tuple[int, int, int], opacity: int) -> None:
    x0, y0, x1, y1 = bbox
    thickness = max(1, font_size // 18)
    points = [(random.uniform(x0, x1), random.uniform(y0, y1)) for _ in range(random.randint(5, 10))]
    draw.line(points, fill=color + (opacity,), width=thickness)


def text_lines_to_image(
    text_lines: list[str],
    image_width: int = 1200,
    line_height: int = 105,
    char_spacing: int = -4,
    blur_strength: tuple[float, float] = (0.2, 0.8),
    rotation_range: tuple[float, float] = (-2.5, 2.5),
    strikeout_prob: float = 0.03,
    scribble_prob: float = 0.03,
) -> Image.Image:
    fonts = _available_fonts()
    if not fonts:
        raise ValueError("No .ttf fonts found in the fonts/ folder.")

    font = ImageFont.truetype(str(random.choice(fonts)), random.randint(48, 68))
    image_height = line_height * len(text_lines) + 60
    img = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    ink = random.randint(0, 35)
    opacity = random.randint(180, 245)
    space_width = font.getbbox(" ")[2] - font.getbbox(" ")[0]
    y = 24

    for text in text_lines:
        x = 24
        for word in str(text).split(" "):
            word_start = x
            for ch in word:
                draw.text((x, y), ch, font=font, fill=(ink, ink, ink, opacity))
                bbox = font.getbbox(ch)
                x += bbox[2] - bbox[0] + char_spacing

            word_bbox = (word_start, y, x, y + font.size)
            if random.random() < strikeout_prob:
                draw_strikeout(draw, word_bbox, font.size, (ink, ink, ink), opacity)
            if random.random() < scribble_prob:
                draw_scribble(draw, word_bbox, font.size, (ink, ink, ink), opacity)

            x += space_width + char_spacing
        y += line_height

    img = img.rotate(random.uniform(*rotation_range), expand=True, fillcolor=(255, 255, 255, 255))
    img = img.filter(ImageFilter.GaussianBlur(random.uniform(*blur_strength)))
    return img.convert("RGB")


def apply_random_warp(image: Image.Image, warp_strength: float = 2.0) -> np.ndarray:
    img = np.array(image)
    h, w, _ = img.shape
    dx = (np.random.rand(h, w) - 0.5) * warp_strength
    dy = (np.random.rand(h, w) - 0.5) * warp_strength
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    map_x = (x + dx).astype(np.float32)
    map_y = (y + dy).astype(np.float32)
    return cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def add_scan_noise(image: Image.Image, noise_std: float = 10, warp_strength: float = 2.0) -> Image.Image:
    np_img = np.array(image)
    noise = np.random.normal(0, noise_std, np_img.shape).astype(np.int16)
    np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    warped = apply_random_warp(Image.fromarray(np_img), warp_strength=warp_strength)
    blurred = cv2.GaussianBlur(warped, (3, 3), sigmaX=0.45)
    return Image.fromarray(blurred)


def generate_handwriting_dataset(
    n: int = 20,
    clean_dir: str = "clean_img",
    clumsy_dir: str = "patient_images",
    form_type: str = "Prescription Form",
    warp_strength: float = 2.0,
    noise_std: float = 10.0,
    strikeout_prob: float = 0.03,
    scribble_prob: float = 0.03,
) -> list[dict[str, object]]:
    os.makedirs(clean_dir, exist_ok=True)
    os.makedirs(clumsy_dir, exist_ok=True)

    records: list[dict[str, object]] = []
    for i in range(n):
        patient = generate_fake_patient()
        lines = patient_to_lines(patient, form_type=form_type)
        clean_img = text_lines_to_image(lines, strikeout_prob=strikeout_prob, scribble_prob=scribble_prob)
        clean_path = Path(clean_dir) / f"sample_{i:03d}_clean.png"
        clean_img.save(clean_path)

        noisy_img = add_scan_noise(clean_img, noise_std=noise_std, warp_strength=warp_strength)
        clumsy_path = Path(clumsy_dir) / f"patient_{i:03d}.jpg"
        noisy_img.save(clumsy_path, quality=92)

        records.append({"patient": patient, "clean_image": str(clean_path), "handwriting_image": str(clumsy_path)})

    return records
