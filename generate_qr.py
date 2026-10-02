import os
import re
import json
import math
import shutil
import qrcode
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Source files in current directory
FACADE_SRC = "source_facade.jpg"
LOGO_SRC = "source_logo.png"
DINING_SRC = "source_dining.jpg"


def load_config(config_path="config.js"):
    """Parse config.js and extract JSON settings safely."""
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"window\.RESTAURANT_CONFIG\s*=\s*(\{.*?\});", content, re.DOTALL)
    if not match:
        return {}
    json_str = match.group(1)
    # Remove full-line comments and inline comments that follow whitespace
    json_str = re.sub(r"^\s*//.*$", "", json_str, flags=re.MULTILINE)
    json_str = re.sub(r"(?<=\s)//.*$", "", json_str, flags=re.MULTILINE)
    # Quote unquoted JS keys
    json_str = re.sub(r"([\{\,\s])([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r'\1"\2":', json_str)
    json_str = re.sub(r",\s*([\]}])", r"\1", json_str)
    try:
        return json.loads(json_str)
    except Exception as e:
        print("Config parse warning:", e)
        return {}


def get_font(size, bold=False, italic=False, serif=False):
    """Load Windows system fonts cleanly with fallbacks."""
    candidates = []
    if serif and italic:
        candidates = ["georgiai.ttf", "timesbi.ttf", "timesi.ttf", "ariali.ttf"]
    elif serif and bold:
        candidates = ["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"]
    elif serif:
        candidates = ["georgia.ttf", "times.ttf", "arial.ttf"]
    elif bold and italic:
        candidates = ["arialbi.ttf", "georgiabi.ttf", "timesbi.ttf"]
    elif bold:
        candidates = ["arialbd.ttf", "segoeuib.ttf", "georgiab.ttf", "timesbd.ttf"]
    elif italic:
        candidates = ["ariali.ttf", "georgiai.ttf", "timesi.ttf"]
    else:
        candidates = ["arial.ttf", "segoeui.ttf", "georgia.ttf"]

    for font_name in candidates:
        font_path = os.path.join("C:\\Windows\\Fonts", font_name)
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass

    # Linux / Ubuntu fallback fonts
    linux_candidates = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if (serif and bold) else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for lf in linux_candidates:
        if os.path.exists(lf):
            try:
                return ImageFont.truetype(lf, size)
            except Exception:
                pass
    return ImageFont.load_default()


def extract_sara_logo():
    """Extract clean transparent logo with white letters and vibrant golden-yellow swoosh."""
    if not os.path.exists(LOGO_SRC):
        print(f"Warning: {LOGO_SRC} not found")
        return None
    
    logo_img = Image.open(LOGO_SRC).convert('RGB')
    arr = np.array(logo_img)
    H, W, _ = arr.shape

    crop_y1, crop_y2 = 75, 330
    crop_x1, crop_x2 = 220, 810
    sub = arr[crop_y1:crop_y2, crop_x1:crop_x2].copy()

    r = sub[:, :, 0].astype(np.float32)
    g = sub[:, :, 1].astype(np.float32)
    b = sub[:, :, 2].astype(np.float32)
    lum = 0.299 * r + 0.587 * g + 0.114 * b

    is_white = (lum > 115) & (abs(r - g) < 35) & (abs(r - b) < 35)
    is_yellow = (r > 150) & (g > 110) & (b < 80)

    import cv2
    mask = (is_white | is_yellow).astype(np.uint8) * 255
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)

    clean_mask = np.zeros_like(mask)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= 10:
            clean_mask[labels == i] = 255

    clean_mask_pil = Image.fromarray(clean_mask, 'L')
    clean_mask_smooth = clean_mask_pil.filter(ImageFilter.GaussianBlur(0.5))
    alpha_arr = np.array(clean_mask_smooth, dtype=np.float32) / 255.0

    out_r = np.full_like(clean_mask, 255)
    out_g = np.full_like(clean_mask, 255)
    out_b = np.full_like(clean_mask, 255)

    yellow_mask = is_yellow & (clean_mask > 0)
    out_r[yellow_mask] = sub[:, :, 0][yellow_mask]
    out_g[yellow_mask] = sub[:, :, 1][yellow_mask]
    out_b[yellow_mask] = sub[:, :, 2][yellow_mask]

    final_rgba = np.stack([out_r, out_g, out_b, (alpha_arr * 255).astype(np.uint8)], axis=2)
    res = Image.fromarray(final_rgba, 'RGBA')
    bbox = res.getbbox()
    if bbox:
        res = res.crop(bbox)
    res.save('sara_logo_clean.png')
    print('Saved sara_logo_clean.png, size:', res.size)
    return res


def create_luxury_medallion(logo_clean, size=600):
    """Create a 24k Gold Rimmed Medallion with deep espresso brownish background."""
    med = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    center = size // 2
    radius = size // 2 - 14

    base_circle = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    base_draw = ImageDraw.Draw(base_circle)

    # Gradient from rich dark bronze/brown (#1a1008) at edge to warm dark amber (#2d1b0f) in center
    for r in range(radius, 0, -1):
        t = r / radius
        red = int(28 * (1 - t) + 52 * t)
        green = int(16 * (1 - t) + 30 * t)
        blue = int(8 * (1 - t) + 16 * t)
        base_draw.ellipse([center - r, center - r, center + r, center + r], fill=(red, green, blue, 255))

    # Outer 24K gold multi-ring bevel
    for i in range(14):
        t = i / 13.0
        gr = int(250 * (1 - 0.35 * abs(t - 0.5)))
        gg = int(210 * (1 - 0.40 * abs(t - 0.5)))
        gb = int(75 * (1 - 0.50 * abs(t - 0.5)))
        base_draw.ellipse([center - radius - 13 + i, center - radius - 13 + i,
                           center + radius + 13 - i, center + radius + 13 - i],
                          outline=(gr, gg, gb, 255), width=2)

    # Inner hairline gold accent ring
    base_draw.ellipse([center - radius + 14, center - radius + 14,
                       center + radius - 14, center + radius - 14],
                      outline=(238, 198, 92, 185), width=2)

    # Place the clean logo in the center
    lw, lh = logo_clean.size
    target_w = int(radius * 1.55)
    scale = target_w / lw
    target_h = int(lh * scale)
    logo_resized = logo_clean.resize((target_w, target_h), Image.Resampling.LANCZOS)

    paste_x = center - target_w // 2
    paste_y = center - target_h // 2
    base_circle.paste(logo_resized, (paste_x, paste_y), logo_resized)

    base_circle.save('logo_medallion.png')
    print('Saved logo_medallion.png, size:', base_circle.size)
    return base_circle


def process_ambience_photos():
    """Extract and enhance ambience photos and synthesize the brownish luxury background."""
    if os.path.exists(DINING_SRC):
        dining = Image.open(DINING_SRC)
        dw, dh = dining.size

        # 1. Ambience 1: Fine Dining Table Setup
        amb1 = dining.crop((int(dw * 0.05), int(dh * 0.48), int(dw * 0.95), int(dh * 0.98)))
        amb1 = ImageEnhance.Color(amb1).enhance(1.2)
        amb1 = ImageEnhance.Contrast(amb1).enhance(1.15)
        amb1 = ImageEnhance.Sharpness(amb1).enhance(1.3)
        amb1.save('ambience_1.jpg', quality=95)

        # 2. Ambience 2: Grand Dining Hall
        amb2 = dining.crop((int(dw * 0.04), int(dh * 0.12), int(dw * 0.96), int(dh * 0.75)))
        amb2 = ImageEnhance.Color(amb2).enhance(1.15)
        amb2 = ImageEnhance.Contrast(amb2).enhance(1.1)
        amb2.save('ambience_2.jpg', quality=95)

        # 4. Ultra-Luxury Brownish Ambience Background (bg_ambience_brownish.jpg)
        bg_base = dining.resize((1200, 1800), Image.Resampling.LANCZOS)
        bg_blur = bg_base.filter(ImageFilter.GaussianBlur(14))
        bg_arr = np.array(bg_blur, dtype=np.float32)

        # Tint with rich dark espresso / bronze: RGB (28, 17, 9)
        tint_r = 28.0
        tint_g = 17.0
        tint_b = 9.0
        tint_factor = 0.68

        bg_tinted_r = np.clip(bg_arr[:, :, 0] * (1.0 - tint_factor) + tint_r * 2.2, 0, 255)
        bg_tinted_g = np.clip(bg_arr[:, :, 1] * (1.0 - tint_factor) + tint_g * 1.8, 0, 255)
        bg_tinted_b = np.clip(bg_arr[:, :, 2] * (1.0 - tint_factor) + tint_b * 1.2, 0, 255)

        # Vignette
        H, W = 1800, 1200
        Y, X = np.ogrid[:H, :W]
        dist_center = np.sqrt(((X - W / 2) / (W / 2)) ** 2 + ((Y - H * 0.35) / (H * 0.6)) ** 2)
        vignette = np.clip(1.0 - 0.45 * dist_center, 0.25, 1.15)[:, :, None]

        final_bg = np.stack([bg_tinted_r, bg_tinted_g, bg_tinted_b], axis=2) * vignette
        final_bg = np.clip(final_bg, 0, 255).astype(np.uint8)

        bg_img = Image.fromarray(final_bg, 'RGB')
        bg_img.save('bg_ambience_brownish.jpg', quality=95)
        print('Saved bg_ambience_brownish.jpg, ambience_1.jpg, ambience_2.jpg')

    if os.path.exists(FACADE_SRC):
        facade = Image.open(FACADE_SRC)
        facade_up = facade.resize((800, 800), Image.Resampling.LANCZOS)
        facade_up = ImageEnhance.Color(facade_up).enhance(1.2)
        facade_up = ImageEnhance.Contrast(facade_up).enhance(1.2)
        facade_up = ImageEnhance.Sharpness(facade_up).enhance(1.4)
        facade_up.save('ambience_3.jpg', quality=95)
        print('Saved ambience_3.jpg')


def draw_google_g_icon(draw, cx, cy, size=32):
    """Draw a clean Google G logo icon."""
    r = size // 2
    # Circular base with white background
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    # Draw segments of Google G
    # Blue right bar
    bar_h = int(size * 0.22)
    draw.rectangle([cx, cy - bar_h // 2, cx + int(r * 0.85), cy + bar_h // 2], fill=(66, 133, 244))
    # Arc cutout
    inner_r = int(r * 0.52)
    # Colored arcs
    hw = int(size * 0.24)
    draw.arc([cx - r + hw//2, cy - r + hw//2, cx + r - hw//2, cy + r - hw//2], start=-45, end=45, fill=(66, 133, 244), width=hw)
    draw.arc([cx - r + hw//2, cy - r + hw//2, cx + r - hw//2, cy + r - hw//2], start=45, end=140, fill=(52, 168, 83), width=hw)
    draw.arc([cx - r + hw//2, cy - r + hw//2, cx + r - hw//2, cy + r - hw//2], start=140, end=225, fill=(251, 188, 5), width=hw)
    draw.arc([cx - r + hw//2, cy - r + hw//2, cx + r - hw//2, cy + r - hw//2], start=225, end=315, fill=(234, 67, 53), width=hw)


def draw_instagram_camera_icon(draw, cx, cy, size=32):
    """Draw an Instagram gradient camera icon."""
    half = size // 2
    # Draw rounded rectangle with Instagram magenta-orange gradient
    draw.rounded_rectangle([cx - half, cy - half, cx + half, cy + half], radius=int(size * 0.28), fill=(225, 48, 108), outline=(255, 255, 255), width=2)
    r_lens = int(size * 0.24)
    draw.ellipse([cx - r_lens, cy - r_lens, cx + r_lens, cy + r_lens], outline=(255, 255, 255), width=2)
    draw.ellipse([cx + half - 7, cy - half + 4, cx + half - 4, cy - half + 7], fill=(255, 255, 255))


def generate_styled_qr(url, target_size=680, center_mode="medallion"):
    """
    Generate an ultra-luxury QR Code with:
    - Circular dot modules in deep bronze & gold accents
    - Rounded finder eyes with 24k gold centers
    - Embedded 24k Gold-Rimmed Circular Medallion in the center
    """
    is_long_url = len(url) > 140
    err_corr = qrcode.constants.ERROR_CORRECT_M if is_long_url else qrcode.constants.ERROR_CORRECT_H

    qr = qrcode.QRCode(
        version=None,
        error_correction=err_corr,
        box_size=20,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    n_mods = len(matrix)
    border = 2

    cell = 24
    canvas_px = n_mods * cell
    img = Image.new("RGBA", (canvas_px, canvas_px), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    center_mod = n_mods / 2.0
    logo_mod_radius = (n_mods * 0.13) if is_long_url else (n_mods * 0.165)

    def is_finder(r, c):
        if border <= r < border + 7 and border <= c < border + 7:
            return True
        if border <= r < border + 7 and (n_mods - border - 7) <= c < (n_mods - border):
            return True
        if (n_mods - border - 7) <= r < (n_mods - border) and border <= c < border + 7:
            return True
        return False

    dot_pad = max(1, int(cell * 0.08))
    for r in range(n_mods):
        for c in range(n_mods):
            if not matrix[r][c]:
                continue
            if is_finder(r, c):
                continue
            dist_c = math.sqrt((r + 0.5 - center_mod) ** 2 + (c + 0.5 - center_mod) ** 2)
            if dist_c < logo_mod_radius:
                continue

            norm_d = dist_c / (n_mods * 0.5)
            # Warm bronze and dark espresso modules
            if norm_d < 0.44 or ((r * 7 + c * 13) % 6 == 0 and norm_d < 0.70):
                fill_col = (180, 120, 30, 255) # Rich amber gold
            else:
                fill_col = (24, 15, 8, 255) # Deep espresso brown

            x1 = c * cell + dot_pad
            y1 = r * cell + dot_pad
            x2 = (c + 1) * cell - dot_pad
            y2 = (r + 1) * cell - dot_pad
            draw.ellipse([x1, y1, x2, y2], fill=fill_col)

    finder_origins = [
        (border, border),
        (border, n_mods - border - 7),
        (n_mods - border - 7, border),
    ]
    for fr, fc in finder_origins:
        fx1, fy1 = fc * cell, fr * cell
        fx2, fy2 = (fc + 7) * cell, (fr + 7) * cell
        # Outer finder frame (deep espresso with gold accent)
        draw.rounded_rectangle(
            [fx1, fy1, fx2, fy2],
            radius=int(cell * 1.8),
            outline=(24, 15, 8, 255),
            width=int(cell * 0.95),
        )
        # Inner hairline gold outline
        draw.rounded_rectangle(
            [fx1 + int(cell*0.1), fy1 + int(cell*0.1), fx2 - int(cell*0.1), fy2 - int(cell*0.1)],
            radius=int(cell * 1.7),
            outline=(212, 175, 55, 200),
            width=2,
        )
        # Center solid eye (24k gold)
        cx1, cy1 = (fc + 2) * cell, (fr + 2) * cell
        cx2, cy2 = (fc + 5) * cell, (fr + 5) * cell
        draw.rounded_rectangle(
            [cx1, cy1, cx2, cy2],
            radius=int(cell * 1.0),
            fill=(218, 165, 32, 255),
            outline=(24, 15, 8, 255),
            width=1,
        )

    # Embed Center Medallion
    center_px = canvas_px // 2
    med_radius_px = int(logo_mod_radius * cell * 0.96)

    # Clear circular white cutout for maximum contrast
    draw.ellipse(
        [center_px - med_radius_px - 4, center_px - med_radius_px - 4,
         center_px + med_radius_px + 4, center_px + med_radius_px + 4],
        fill=(255, 255, 255, 255)
    )

    if center_mode == "medallion" and os.path.exists("logo_medallion.png"):
        med_img = Image.open("logo_medallion.png").convert("RGBA")
        med_scaled = med_img.resize((med_radius_px * 2, med_radius_px * 2), Image.Resampling.LANCZOS)
        img.paste(med_scaled, (center_px - med_radius_px, center_px - med_radius_px), med_scaled)
    elif center_mode == "google":
        # Google Review Center Emblem
        draw.ellipse([center_px - med_radius_px, center_px - med_radius_px, center_px + med_radius_px, center_px + med_radius_px], fill=(255, 255, 255), outline=(218, 165, 32), width=3)
        draw_google_g_icon(draw, center_px, center_px, size=int(med_radius_px * 1.1))
    elif center_mode == "instagram":
        draw.ellipse([center_px - med_radius_px, center_px - med_radius_px, center_px + med_radius_px, center_px + med_radius_px], fill=(255, 255, 255), outline=(218, 165, 32), width=3)
        draw_instagram_camera_icon(draw, center_px, center_px, size=int(med_radius_px * 1.1))

    return img.resize((target_size, target_size), Image.Resampling.LANCZOS)


def draw_stars(draw, cx, cy, count=5, radius=12, gap=8, fill_col=(255, 215, 0), outline_col=(180, 130, 20)):
    """Draw 5 golden stars."""
    total_w = count * (radius * 2) + (count - 1) * gap
    start_x = cx - total_w // 2 + radius
    for i in range(count):
        sx = start_x + i * (radius * 2 + gap)
        points = []
        for p in range(10):
            angle = p * math.pi / 5 - math.pi / 2
            r = radius if p % 2 == 0 else radius * 0.42
            points.append((sx + r * math.cos(angle), cy + r * math.sin(angle)))
        draw.polygon(points, fill=fill_col, outline=outline_col)


def draw_luxury_corners(draw, x1, y1, x2, y2, arm=36, col=(249, 226, 156, 255)):
    """Draw ornate 24k gold corner brackets."""
    # Top-Left
    draw.line([(x1, y1), (x1 + arm, y1)], fill=col, width=3)
    draw.line([(x1, y1), (x1, y1 + arm)], fill=col, width=3)
    draw.ellipse([x1 + arm - 2, y1 - 2, x1 + arm + 2, y1 + 2], fill=col)
    draw.ellipse([x1 - 2, y1 + arm - 2, x1 + 2, y1 + arm + 2], fill=col)

    # Top-Right
    draw.line([(x2, y1), (x2 - arm, y1)], fill=col, width=3)
    draw.line([(x2, y1), (x2, y1 + arm)], fill=col, width=3)
    draw.ellipse([x2 - arm - 2, y1 - 2, x2 - arm + 2, y1 + 2], fill=col)
    draw.ellipse([x2 - 2, y1 + arm - 2, x2 + 2, y1 + arm + 2], fill=col)

    # Bottom-Left
    draw.line([(x1, y2), (x1 + arm, y2)], fill=col, width=3)
    draw.line([(x1, y2), (x1, y2 - arm)], fill=col, width=3)
    draw.ellipse([x1 + arm - 2, y2 - 2, x1 + arm + 2, y2 + 2], fill=col)
    draw.ellipse([x1 - 2, y2 - arm - 2, x1 + 2, y2 - arm + 2], fill=col)

    # Bottom-Right
    draw.line([(x2, y2), (x2 - arm, y2)], fill=col, width=3)
    draw.line([(x2, y2), (x2, y2 - arm)], fill=col, width=3)
    draw.ellipse([x2 - arm - 2, y2 - 2, x2 - arm + 2, y2 + 2], fill=col)
    draw.ellipse([x2 - 2, y2 - arm - 2, x2 + 2, y2 - arm + 2], fill=col)


def generate_single_smart_standee(config, output_filename="table_standee_printable.png", table_num=None, custom_url=None, serial_no=None):
    """
    Generate 300 DPI Ultra-Luxury Acrylic Standee (1200 x 1800 px) for Hotel The Sara:
    - Deep espresso brownish luxury background with ambient chandelier bokeh
    - Ornate 24k gold framing and corner accents
    - Hotel The Sara logo medallion
    - High-contrast styled QR code
    - Table Number Badge (e.g. VIP TABLE #01)
    - Anti-Piracy Tamper-Proof Hologram / Security Seal
    """
    W, H = 1200, 1800
    if os.path.exists("bg_ambience_brownish.jpg"):
        card = Image.open("bg_ambience_brownish.jpg").resize((W, H), Image.Resampling.LANCZOS)
    else:
        card = Image.new("RGB", (W, H), (24, 15, 8))

    draw = ImageDraw.Draw(card)

    # Borders
    # Outer 24k gold border
    draw.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, outline=(218, 175, 58), width=4)
    # Inner hairline gold border
    draw.rounded_rectangle([44, 44, W - 44, H - 44], radius=18, outline=(249, 226, 156, 180), width=2)
    # Corner ornaments
    draw_luxury_corners(draw, 56, 56, W - 56, H - 56, arm=48, col=(249, 226, 156, 255))

    # 1. Header Section:
    f_sub = get_font(20, bold=True, serif=True)
    f_title = get_font(42, bold=True, serif=True)
    f_tagline = get_font(22, bold=True, serif=False)
    f_cta_main = get_font(34, bold=True, serif=True)
    f_cta_sub = get_font(20, bold=False, serif=False)
    f_sec = get_font(15, bold=True, serif=False)

    # Luxury badge at top
    badge_text = "HOTEL THE SARA • GUNA"
    draw.rounded_rectangle([W // 2 - 190, 78, W // 2 + 190, 114], radius=18, fill=(18, 10, 5, 230), outline=(218, 175, 58), width=2)
    draw.text((W // 2, 96), badge_text, fill=(249, 226, 156), font=f_sub, anchor="mm")

    # Center Medallion
    if os.path.exists("logo_medallion.png"):
        med = Image.open("logo_medallion.png").resize((210, 210), Image.Resampling.LANCZOS)
        card.paste(med, (W // 2 - 105, 134), med)

    # Brand Title: "HOTEL THE SARA"
    draw.text((W // 2, 372), "HOTEL THE SARA", fill=(255, 255, 255), font=f_title, anchor="mm")
    draw.text((W // 2, 412), "STAY IN STYLE • FINE DINING & BANQUETS", fill=(218, 175, 58), font=f_tagline, anchor="mm")

    # Divider line with center diamond
    draw.line([(W // 2 - 220, 442), (W // 2 + 220, 442)], fill=(218, 175, 58, 180), width=2)
    draw.polygon([(W // 2, 436), (W // 2 + 7, 442), (W // 2, 448), (W // 2 - 7, 442)], fill=(249, 226, 156))

    # 2. Main Call to Action:
    draw.text((W // 2, 480), "RATE US ON GOOGLE", fill=(255, 245, 220), font=f_cta_main, anchor="mm")
    draw_stars(draw, W // 2, 524, count=5, radius=14, gap=8, fill_col=(255, 215, 0), outline_col=(180, 130, 20))
    draw.text((W // 2, 564), "& FOLLOW US ON INSTAGRAM", fill=(249, 226, 156), font=get_font(26, bold=True, serif=True), anchor="mm")

    # 3. QR Code Section (Large High Contrast 660x660 in 24k Gold Bevel)
    landing_url = custom_url or config.get("landingPageUrl", "https://hospitalityqr.github.io/sara-hotel-guna/")
    qr_img = generate_styled_qr(landing_url, target_size=630, center_mode="medallion")

    qr_box_y = 612
    draw.rounded_rectangle([W // 2 - 340, qr_box_y - 12, W // 2 + 340, qr_box_y + 630 + 12], radius=26, fill=(255, 255, 255), outline=(218, 175, 58), width=5)
    draw.rounded_rectangle([W // 2 - 332, qr_box_y - 4, W // 2 + 332, qr_box_y + 630 + 4], radius=22, outline=(249, 226, 156), width=2)
    card.paste(qr_img, (W // 2 - 315, qr_box_y), qr_img)

    # 4. Under-QR Guidance:
    draw.text((W // 2, 1304), "POINT YOUR PHONE CAMERA TO SCAN", fill=(255, 255, 255), font=get_font(24, bold=True, serif=True), anchor="mm")
    draw.text((W // 2, 1338), "Direct Google Reviews • Instagram • WiFi • Contact", fill=(218, 175, 58), font=f_cta_sub, anchor="mm")

    # 5. Table Number & Security Seal:
    display_table = table_num or config.get("license", {}).get("tableNumber", "VIP TABLE #01")
    draw.rounded_rectangle([W // 2 - 190, 1380, W // 2 + 190, 1432], radius=15, fill=(18, 10, 5, 240), outline=(218, 175, 58), width=2)
    draw.text((W // 2, 1406), f"• {display_table.upper()} •", fill=(255, 220, 130), font=get_font(22, bold=True, serif=True), anchor="mm")

    # Anti-Piracy Tamper-Proof Hologram / Security Footer:
    display_serial = serial_no or config.get("license", {}).get("serialNumber", "HS-GUNA-VIP-001")
    draw.rounded_rectangle([72, 1690, W - 72, 1742], radius=12, fill=(10, 6, 3, 230), outline=(180, 130, 30), width=1)
    draw.text((W // 2, 1716), f"AUTHENTIC HOSPITALITY SMART HUB  |  SERIAL #{display_serial}  |  LICENSED HARDWARE", fill=(180, 150, 100), font=f_sec, anchor="mm")

    card.save(output_filename, dpi=(300, 300), quality=98)
    return card


def generate_dual_direct_standee(config, output_filename="standee_dual_direct_static.png"):
    """
    Generate 300 DPI Dual Standee:
    Left: Google Review QR (with 5 stars)
    Right: Instagram QR (with follow handle)
    """
    W, H = 1200, 1800
    if os.path.exists("bg_ambience_brownish.jpg"):
        card = Image.open("bg_ambience_brownish.jpg").resize((W, H), Image.Resampling.LANCZOS)
    else:
        card = Image.new("RGB", (W, H), (24, 15, 8))

    draw = ImageDraw.Draw(card)

    # Borders
    draw.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, outline=(218, 175, 58), width=4)
    draw.rounded_rectangle([44, 44, W - 44, H - 44], radius=18, outline=(249, 226, 156, 180), width=2)
    draw_luxury_corners(draw, 56, 56, W - 56, H - 56, arm=48, col=(249, 226, 156, 255))

    # Header
    if os.path.exists("logo_medallion.png"):
        med = Image.open("logo_medallion.png").resize((180, 180), Image.Resampling.LANCZOS)
        card.paste(med, (W // 2 - 90, 80), med)

    draw.text((W // 2, 290), "HOTEL THE SARA", fill=(255, 255, 255), font=get_font(42, bold=True, serif=True), anchor="mm")
    draw.text((W // 2, 330), "STAY IN STYLE • FINE DINING & BANQUETS", fill=(218, 175, 58), font=get_font(22, bold=True), anchor="mm")

    draw.line([(W // 2 - 240, 360), (W // 2 + 240, 360)], fill=(218, 175, 58, 180), width=2)

    # Dual Columns:
    # Left: Google Review
    col_w = 480
    left_cx = 320
    right_cx = 880
    qr_size = 420
    box_y = 480

    # Google Column
    draw.text((left_cx, 410), "RATE US ON GOOGLE", fill=(255, 255, 255), font=get_font(24, bold=True, serif=True), anchor="mm")
    draw_stars(draw, left_cx, 445, count=5, radius=11, gap=6, fill_col=(255, 215, 0), outline_col=(180, 130, 20))

    google_url = config.get("googleReviewUrl", "https://www.google.com/maps/search/?api=1&query=Hotel+The+Sara+Guna+Madhya+Pradesh")
    google_qr = generate_styled_qr(google_url, target_size=qr_size, center_mode="google")

    draw.rounded_rectangle([left_cx - qr_size // 2 - 12, box_y - 12, left_cx + qr_size // 2 + 12, box_y + qr_size + 12], radius=20, fill=(255, 255, 255), outline=(218, 175, 58), width=4)
    card.paste(google_qr, (left_cx - qr_size // 2, box_y), google_qr)

    draw.text((left_cx, box_y + qr_size + 36), "Scan to Share Your Experience", fill=(249, 226, 156), font=get_font(18, bold=True), anchor="mm")
    draw_stars(draw, left_cx, box_y + qr_size + 65, count=5, radius=8, gap=4)

    # Right Column: Instagram
    draw.text((right_cx, 410), "FOLLOW ON INSTAGRAM", fill=(255, 255, 255), font=get_font(24, bold=True, serif=True), anchor="mm")
    insta_handle = config.get("instagramHandle", "@hotelthesara_guna")
    draw.text((right_cx, 445), insta_handle, fill=(249, 226, 156), font=get_font(20, bold=True), anchor="mm")

    insta_url = config.get("instagramUrl", "https://www.instagram.com/hotelthesara_guna/")
    insta_qr = generate_styled_qr(insta_url, target_size=qr_size, center_mode="instagram")

    draw.rounded_rectangle([right_cx - qr_size // 2 - 12, box_y - 12, right_cx + qr_size // 2 + 12, box_y + qr_size + 12], radius=20, fill=(255, 255, 255), outline=(218, 175, 58), width=4)
    card.paste(insta_qr, (right_cx - qr_size // 2, box_y), insta_qr)

    draw.text((right_cx, box_y + qr_size + 36), "Scan to Tag & Follow Us", fill=(249, 226, 156), font=get_font(18, bold=True), anchor="mm")
    draw.text((right_cx, box_y + qr_size + 65), "Share Your Dining Moments", fill=(255, 255, 255), font=get_font(16), anchor="mm")

    # Bottom Table & Security Section
    table_num = config.get("license", {}).get("tableNumber", "VIP TABLE #01")
    draw.rounded_rectangle([W // 2 - 180, 1420, W // 2 + 180, 1470], radius=15, fill=(18, 10, 5, 240), outline=(218, 175, 58), width=2)
    draw.text((W // 2, 1445), f"• {table_num.upper()} •", fill=(255, 220, 130), font=get_font(22, bold=True, serif=True), anchor="mm")

    # Anti-Piracy Serial
    serial_no = config.get("license", {}).get("serialNumber", "HS-GUNA-VIP-001")
    draw.rounded_rectangle([72, 1690, W - 72, 1742], radius=12, fill=(10, 6, 3, 230), outline=(180, 130, 30), width=1)
    draw.text((W // 2, 1716), f"AUTHENTIC HOSPITALITY DUAL HUB  |  SERIAL #{serial_no}  |  ALL RIGHTS RESERVED", fill=(180, 150, 100), font=get_font(15, bold=True), anchor="mm")

    card.save(output_filename, dpi=(300, 300), quality=98)
    print(f"Saved {output_filename} (300 DPI, {W}x{H})")
    return card


def generate_single_channel_standees(config):
    """Generate separate Google-only and Instagram-only standees at 300 DPI."""
    # Google Direct
    google_url = config.get("googleReviewUrl", "https://www.google.com/maps/search/?api=1&query=Hotel+The+Sara+Guna+Madhya+Pradesh")
    W, H = 1200, 1800
    card_g = Image.open("bg_ambience_brownish.jpg").resize((W, H), Image.Resampling.LANCZOS)
    draw_g = ImageDraw.Draw(card_g)
    draw_g.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, outline=(218, 175, 58), width=4)
    draw_g.rounded_rectangle([44, 44, W - 44, H - 44], radius=18, outline=(249, 226, 156, 180), width=2)
    draw_luxury_corners(draw_g, 56, 56, W - 56, H - 56, arm=48, col=(249, 226, 156, 255))

    if os.path.exists("logo_medallion.png"):
        med = Image.open("logo_medallion.png").resize((210, 210), Image.Resampling.LANCZOS)
        card_g.paste(med, (W // 2 - 105, 120), med)

    draw_g.text((W // 2, 360), "HOTEL THE SARA", fill=(255, 255, 255), font=get_font(42, bold=True, serif=True), anchor="mm")
    draw_g.text((W // 2, 400), "SHARE YOUR DINING EXPERIENCE", fill=(218, 175, 58), font=get_font(22, bold=True), anchor="mm")
    draw_g.text((W // 2, 470), "RATE US ON GOOGLE", fill=(255, 255, 255), font=get_font(34, bold=True, serif=True), anchor="mm")
    draw_stars(draw_g, W // 2, 515, count=5, radius=14, gap=8)

    qr_g = generate_styled_qr(google_url, target_size=630, center_mode="google")
    draw_g.rounded_rectangle([W // 2 - 340, 580, W // 2 + 340, 580 + 630 + 24], radius=26, fill=(255, 255, 255), outline=(218, 175, 58), width=5)
    card_g.paste(qr_g, (W // 2 - 315, 592), qr_g)

    draw_g.text((W // 2, 1280), "SCAN WITH YOUR PHONE CAMERA", fill=(255, 255, 255), font=get_font(24, bold=True, serif=True), anchor="mm")
    draw_g.text((W // 2, 1318), "Your 5-Star Review Inspires Our Hospitality Team", fill=(218, 175, 58), font=get_font(20), anchor="mm")

    # Table badge & serial
    table_num = config.get("license", {}).get("tableNumber", "VIP TABLE #01")
    draw_g.rounded_rectangle([W // 2 - 180, 1380, W // 2 + 180, 1430], radius=15, fill=(18, 10, 5, 240), outline=(218, 175, 58), width=2)
    draw_g.text((W // 2, 1405), f"• {table_num.upper()} •", fill=(255, 220, 130), font=get_font(22, bold=True, serif=True), anchor="mm")

    serial_no = config.get("license", {}).get("serialNumber", "HS-GUNA-VIP-001")
    draw_g.rounded_rectangle([72, 1690, W - 72, 1742], radius=12, fill=(10, 6, 3, 230), outline=(180, 130, 30), width=1)
    draw_g.text((W // 2, 1716), f"AUTHENTIC HOSPITALITY GOOGLE HUB  |  SERIAL #{serial_no}  |  LICENSED HARDWARE", fill=(180, 150, 100), font=get_font(15, bold=True), anchor="mm")
    card_g.save("standee_google_direct.png", dpi=(300, 300), quality=98)
    print("Saved standee_google_direct.png")

    # Instagram Direct
    insta_url = config.get("instagramUrl", "https://www.instagram.com/hotelthesara_guna/")
    card_i = Image.open("bg_ambience_brownish.jpg").resize((W, H), Image.Resampling.LANCZOS)
    draw_i = ImageDraw.Draw(card_i)
    draw_i.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, outline=(218, 175, 58), width=4)
    draw_i.rounded_rectangle([44, 44, W - 44, H - 44], radius=18, outline=(249, 226, 156, 180), width=2)
    draw_luxury_corners(draw_i, 56, 56, W - 56, H - 56, arm=48, col=(249, 226, 156, 255))

    if os.path.exists("logo_medallion.png"):
        med = Image.open("logo_medallion.png").resize((210, 210), Image.Resampling.LANCZOS)
        card_i.paste(med, (W // 2 - 105, 120), med)

    draw_i.text((W // 2, 360), "HOTEL THE SARA", fill=(255, 255, 255), font=get_font(42, bold=True, serif=True), anchor="mm")
    draw_i.text((W // 2, 400), "TAG US & SHARE YOUR MEMORIES", fill=(218, 175, 58), font=get_font(22, bold=True), anchor="mm")
    draw_i.text((W // 2, 470), "FOLLOW US ON INSTAGRAM", fill=(255, 255, 255), font=get_font(34, bold=True, serif=True), anchor="mm")
    insta_handle = config.get("instagramHandle", "@hotelthesara_guna")
    draw_i.text((W // 2, 515), insta_handle, fill=(249, 226, 156), font=get_font(26, bold=True), anchor="mm")

    qr_i = generate_styled_qr(insta_url, target_size=630, center_mode="instagram")
    draw_i.rounded_rectangle([W // 2 - 340, 580, W // 2 + 340, 580 + 630 + 24], radius=26, fill=(255, 255, 255), outline=(218, 175, 58), width=5)
    card_i.paste(qr_i, (W // 2 - 315, 592), qr_i)

    draw_i.text((W // 2, 1280), "SCAN TO VISIT OUR INSTAGRAM PROFILE", fill=(255, 255, 255), font=get_font(24, bold=True, serif=True), anchor="mm")
    draw_i.text((W // 2, 1318), "Exclusive Stories, Event Updates & Banquet Highlights", fill=(218, 175, 58), font=get_font(20), anchor="mm")

    # Table badge & serial
    draw_i.rounded_rectangle([W // 2 - 180, 1380, W // 2 + 180, 1430], radius=15, fill=(18, 10, 5, 240), outline=(218, 175, 58), width=2)
    draw_i.text((W // 2, 1405), f"• {table_num.upper()} •", fill=(255, 220, 130), font=get_font(22, bold=True, serif=True), anchor="mm")

    draw_i.rounded_rectangle([72, 1690, W - 72, 1742], radius=12, fill=(10, 6, 3, 230), outline=(180, 130, 30), width=1)
    draw_i.text((W // 2, 1716), f"AUTHENTIC HOSPITALITY INSTA HUB  |  SERIAL #{serial_no}  |  LICENSED HARDWARE", fill=(180, 150, 100), font=get_font(15, bold=True), anchor="mm")
    card_i.save("standee_instagram_direct.png", dpi=(300, 300), quality=98)
    print("Saved standee_instagram_direct.png")


def generate_all_table_standees(config, count=20, output_dir="table_standees_1_to_20"):
    """
    Generate 20 separate 300 DPI Standees for Hotel The Sara:
    - Each table has its own unique label: Table #01 to Table #20
    - Each QR code points directly to: https://hospitalityqr.github.io/sara-hotel-guna/?table={i}
    - Each standee has its unique anti-counterfeiting serial: #HS-GUNA-TAB-{i:02d}
    - Archives all 20 PNGs into Hotel_The_Sara_20_Table_Standees_300DPI.zip for 1-click printing!
    """
    import zipfile
    os.makedirs(output_dir, exist_ok=True)
    base_landing_url = config.get("landingPageUrl", "https://hospitalityqr.github.io/sara-hotel-guna/").rstrip('/')
    
    zip_filename = "Hotel_The_Sara_20_Table_Standees_300DPI.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for i in range(1, count + 1):
            table_label = f"VIP TABLE #01" if i == 1 else f"TABLE #{i:02d}"
            table_url = f"{base_landing_url}/?table={i}"
            serial_no = f"HS-GUNA-TAB-{i:02d}"
            filename = os.path.join(output_dir, f"Table_{i:02d}_Standee_Printable.png")
            
            print(f"Generating Table {i:02d}/{count:02d} -> {table_label} ({table_url})...")
            generate_single_smart_standee(
                config=config,
                output_filename=filename,
                table_num=table_label,
                custom_url=table_url,
                serial_no=serial_no
            )
            zipf.write(filename, arcname=f"Table_{i:02d}_Standee_Printable.png")
            
    print(f"\n[SUCCESS] Generated all {count} Table Standees in '{output_dir}/' and zipped to '{zip_filename}'!")


def main():
    print("==================================================")
    print("HOTEL THE SARA (GUNA) — ULTRA-LUXURY QR SUITE BUILD")
    print("==================================================")
    config = load_config()

    # 1. Extract Logo & Build Medallion
    print("\n[1/5] Extracting Logo & Building 24k Gold Medallion...")
    logo_clean = extract_sara_logo()
    if logo_clean:
        create_luxury_medallion(logo_clean, size=600)

    # 2. Ambience Photos & Luxury Brownish Background
    print("\n[2/5] Synthesizing Ambience Photos & Luxury Brownish Background...")
    process_ambience_photos()

    # 3. QR Codes
    print("\n[3/5] Generating High-Resolution Styled QR Codes...")
    landing_url = config.get("landingPageUrl", "https://hospitalityqr.github.io/sara-hotel-guna/")
    google_url = config.get("googleReviewUrl", "https://share.google/vRFMikseO8TDcpg9l")
    insta_url = config.get("instagramUrl", "https://www.instagram.com/hotelthesara?stkn=dzQwc3pzNGx0Y3Jo")

    qr_smart = generate_styled_qr(landing_url, target_size=800, center_mode="medallion")
    qr_smart.save("qr_code.png")
    qr_smart.save("qr_landing_page.png")
    print("Saved qr_code.png and qr_landing_page.png")

    qr_google = generate_styled_qr(google_url, target_size=800, center_mode="google")
    qr_google.save("qr_google_direct.png")
    print("Saved qr_google_direct.png")

    qr_insta = generate_styled_qr(insta_url, target_size=800, center_mode="instagram")
    qr_insta.save("qr_instagram_direct.png")
    print("Saved qr_instagram_direct.png")

    # 4. 300 DPI Printable Standees (Default Hub & Channels)
    print("\n[4/5] Rendering 300 DPI Printable Standees...")
    generate_single_smart_standee(config, "table_standee_printable.png")
    generate_single_smart_standee(config, "standee_front_printable.png")
    generate_dual_direct_standee(config, "standee_dual_direct_static.png")
    generate_single_channel_standees(config)

    # 5. Batch 20 Table Standees (Table 01 to Table 20)
    print("\n[5/5] Generating 20 Unique Table Standees (Table #01 to Table #20)...")
    generate_all_table_standees(config, count=20, output_dir="table_standees_1_to_20")

    print("\n==================================================")
    print("ALL 20 TABLE STANDEES & ASSETS GENERATED SUCCESSFULLY!")
    print("==================================================")


if __name__ == "__main__":
    main()

