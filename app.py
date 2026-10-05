import re
import cv2
import numpy as np
import requests
import streamlit as st
import easyocr


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Vehicle Number Plate AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CONFIGURATION
# =========================================================

# IMPORTANT:
# Paste your existing Google Apps Script /exec URL here.
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzDjRiuUmnVQp-LXBgksgi-Qg4cjUlsDdyw_LTuwjDfycLX4Hkr1vPtSJFDWrRduA3seA/exec"


# =========================================================
# HTML RENDER HELPER
# =========================================================

def render_html(html_code):
    st.html(html_code)


# =========================================================
# CUSTOM 3D UI / CSS
# =========================================================

st.html("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(0,255,255,0.08),
            transparent 25%
        ),
        radial-gradient(
            circle at 85% 20%,
            rgba(120,0,255,0.10),
            transparent 25%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(0,150,255,0.06),
            transparent 30%
        ),
        #050814;

    color: white;
}

.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* ================= HERO ================= */

.hero {
    position: relative;
    padding: 30px 20px;
    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.09),
            rgba(255,255,255,0.02)
        );

    border: 1px solid rgba(255,255,255,0.12);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(255,255,255,0.05);

    backdrop-filter: blur(15px);

    text-align: center;

    margin-bottom: 25px;
}


/* ================= AI CORE ================= */

.ai-core {
    width: 74px;
    height: 74px;

    margin: 0 auto 12px auto;

    border-radius: 50%;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            circle,
            rgba(0,230,255,0.30),
            rgba(80,50,255,0.10)
        );

    border:
        2px solid rgba(90,230,255,0.35);

    box-shadow:
        0 0 25px rgba(0,220,255,0.25),
        inset 0 0 20px rgba(0,220,255,0.10);
}


/* ================= HERO TITLE ================= */

.hero-title {
    font-size: 31px;
    font-weight: 900;
    letter-spacing: 1.5px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #6ee7ff,
            #b28cff
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


/* ================= HERO SUBTITLE ================= */

.hero-subtitle {
    font-size: 14px;
    color: #aeb8d0;

    margin-top: 6px;
    margin-bottom: 14px;
}


/* ================= STATUS ================= */

.status {
    display: inline-block;

    padding: 6px 16px;

    border-radius: 20px;

    background:
        rgba(0,255,170,0.10);

    border:
        1px solid rgba(0,255,170,0.28);

    color: #63ffc8;

    font-size: 11px;
    font-weight: 800;

    letter-spacing: 0.5px;
}


/* ================= INPUT CARDS ================= */

.glass-card {
    padding: 18px;
    min-height: 95px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.08),
            rgba(255,255,255,0.02)
        );

    border:
        1px solid rgba(255,255,255,0.09);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.30);

    backdrop-filter: blur(12px);

    text-align: center;

    margin-bottom: 10px;
}

.card-icon {
    font-size: 28px;
    margin-bottom: 5px;
}

.card-title {
    font-size: 16px;
    font-weight: 800;
    color: #ffffff;
}

.card-subtitle {
    font-size: 11px;
    color: #8995ad;
    margin-top: 4px;
}


/* ================= CAPTURE ================= */

.capture-title {
    margin-top: 25px;
    margin-bottom: 8px;

    padding: 18px 20px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.06),
            rgba(255,255,255,0.015)
        );

    border:
        1px solid rgba(255,255,255,0.10);

    box-shadow:
        0 12px 35px rgba(0,0,0,0.30);
}

.capture-heading {
    font-size: 23px;
    font-weight: 800;
    color: white;
}

.capture-description {
    font-size: 13px;
    color: #9da8be;
    margin-top: 5px;
}


/* ================= RESULT ================= */

.result-box {
    margin-top: 22px;

    padding: 24px;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            rgba(0,255,170,0.09),
            rgba(0,200,255,0.04)
        );

    border:
        1px solid rgba(0,255,170,0.28);

    text-align: center;

    box-shadow:
        0 10px 30px rgba(0,255,170,0.06);
}

.result-label {
    font-size: 11px;
    color: #63ffc8;

    font-weight: 800;

    letter-spacing: 1px;

    margin-bottom: 7px;
}

.plate-number {
    font-size: 35px;

    font-weight: 900;

    letter-spacing: 4px;

    color: white;

    text-shadow:
        0 0 18px rgba(0,220,255,0.35);
}


/* ================= FLOW ================= */

.flow {
    display: flex;

    justify-content: center;
    align-items: center;

    gap: 8px;

    flex-wrap: wrap;

    margin-top: 28px;

    padding: 15px;
}

.flow-item {
    padding: 9px 13px;

    border-radius: 11px;

    background:
        rgba(255,255,255,0.05);

    border:
        1px solid rgba(255,255,255,0.08);

    color: #c7d1e5;

    font-size: 12px;

    font-weight: 600;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.15);
}

.arrow {
    color: #55dfff;
    font-size: 20px;
    font-weight: bold;
}


/* ================= BUTTON ================= */

div.stButton > button {
    width: 100%;

    min-height: 52px;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            rgba(0,190,255,0.28),
            rgba(100,70,255,0.28)
        );

    color: white;

    border:
        1px solid rgba(100,220,255,0.35);

    font-weight: 900;

    font-size: 16px;

    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color:
        rgba(100,220,255,0.75);

    box-shadow:
        0 0 25px rgba(0,200,255,0.25);

    transform:
        translateY(-1px);
}


/* ================= FILE UPLOADER ================= */

[data-testid="stFileUploader"] {
    border-radius: 12px;
}


/* ================= MOBILE ================= */

@media (max-width: 700px) {

    .hero-title {
        font-size: 23px;
    }

    .hero-subtitle {
        font-size: 12px;
    }

    .plate-number {
        font-size: 27px;
    }

    .capture-heading {
        font-size: 20px;
    }

}

</style>
""")


# =========================================================
# HEADER
# =========================================================

render_html("""
<div class="hero">

    <div class="ai-core">
        <div style="font-size:32px;">
            🤖
        </div>
    </div>

    <div class="hero-title">
        VEHICLE NUMBER PLATE AI
    </div>

    <div class="hero-subtitle">
        Intelligent Plate Detection & Automatic Records
    </div>

    <div class="status">
        ● AI CORE ONLINE
    </div>

</div>
""")


# =========================================================
# LOAD EASY OCR
# =========================================================

@st.cache_resource(show_spinner=False)
def load_ocr():

    return easyocr.Reader(
        ['en'],
        gpu=False
    )


# =========================================================
# INDIAN STATE / UT CODES
# =========================================================

INDIAN_STATE_CODES = {

    # States

    "AP",
    "AR",
    "AS",
    "BR",
    "CG",
    "GA",
    "GJ",
    "HR",
    "HP",
    "JH",
    "KA",
    "KL",
    "MP",
    "MH",
    "MN",
    "ML",
    "MZ",
    "NL",
    "OD",
    "PB",
    "RJ",
    "SK",
    "TN",
    "TS",
    "TR",
    "UP",
    "UK",
    "WB",

    # Union Territories

    "AN",
    "CH",
    "DD",
    "DL",
    "JK",
    "LA",
    "LD",
    "PY",

    # Legacy codes

    "OR",
    "DN"
}


# =========================================================
# NORMALIZE
# =========================================================

def normalize_plate(text):

    if text is None:
        return ""

    return re.sub(
        r"[^A-Z0-9]",
        "",
        str(text).upper()
    )


# =========================================================
# VALIDATE INDIAN PLATE
# =========================================================

def is_valid_indian_plate(text):

    text = normalize_plate(text)

    if not text:
        return False

    # -----------------------------------------------------
    # BH SERIES
    # Example: 24BH1234AA
    # -----------------------------------------------------

    bh_pattern = (
        r"^\d{2}"
        r"BH"
        r"\d{4}"
        r"[A-Z]{2}$"
    )

    if re.fullmatch(
        bh_pattern,
        text
    ):
        return True

    # -----------------------------------------------------
    # NORMAL INDIAN REGISTRATION
    # Example:
    # DL7CQ1939
    # MH29CD0038
    # KA01AB1234
    # -----------------------------------------------------

    normal_pattern = (
        r"^[A-Z]{2}"
        r"\d{1,2}"
        r"[A-Z]{1,3}"
        r"\d{1,4}$"
    )

    if not re.fullmatch(
        normal_pattern,
        text
    ):
        return False

    return text[:2] in INDIAN_STATE_CODES


# =========================================================
# EXTRACT VALID PLATE
# =========================================================

def extract_valid_from_text(text):

    cleaned = normalize_plate(text)

    if not cleaned:
        return None

    # Direct match
    if is_valid_indian_plate(cleaned):
        return cleaned

    # Search inside longer OCR text
    max_len = min(
        len(cleaned),
        12
    )

    for start in range(len(cleaned)):

        for end in range(
            start + 7,
            max_len + 1
        ):

            candidate = cleaned[start:end]

            if is_valid_indian_plate(candidate):
                return candidate

    return None


# =========================================================
# PLATE CANDIDATE SCORE
# =========================================================

def plate_format_score(plate):

    plate = normalize_plate(plate)

    if not plate:
        return 0

    score = 0

    # Correct Indian state / UT prefix
    if plate[:2] in INDIAN_STATE_CODES:
        score += 40

    # Correct length
    if 8 <= len(plate) <= 10:
        score += 20

    # Normal registration structure
    if re.fullmatch(
        r"^[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{1,4}$",
        plate
    ):
        score += 30

    # BH series
    if re.fullmatch(
        r"^\d{2}BH\d{4}[A-Z]{2}$",
        plate
    ):
        score += 30

    return score


# =========================================================
# IMAGE ENHANCEMENT
# =========================================================

def enhance_plate_crop(crop):

    if crop is None:
        return []

    if crop.size == 0:
        return []

    try:

        # -------------------------------------------------
        # BIG UPSCALE
        # -------------------------------------------------

        upscaled = cv2.resize(
            crop,
            None,
            fx=6,
            fy=6,
            interpolation=cv2.INTER_CUBIC
        )

        # -------------------------------------------------
        # GRAYSCALE
        # -------------------------------------------------

        gray = cv2.cvtColor(
            upscaled,
            cv2.COLOR_BGR2GRAY
        )

        # -------------------------------------------------
        # DENOISE
        # -------------------------------------------------

        denoised = cv2.fastNlMeansDenoising(
            gray,
            None,
            h=7,
            templateWindowSize=7,
            searchWindowSize=21
        )

        # -------------------------------------------------
        # CLAHE
        # -------------------------------------------------

        clahe = cv2.createCLAHE(
            clipLimit=2.5,
            tileGridSize=(8, 8)
        )

        enhanced = clahe.apply(
            denoised
        )

        # -------------------------------------------------
        # SHARPEN
        # -------------------------------------------------

        blur = cv2.GaussianBlur(
            enhanced,
            (0, 0),
            1.2
        )

        sharpened = cv2.addWeighted(
            enhanced,
            1.7,
            blur,
            -0.7,
            0
        )

        # -------------------------------------------------
        # OTSU
        # -------------------------------------------------

        _, otsu = cv2.threshold(
            sharpened,
            0,
            255,
            cv2.THRESH_BINARY +
            cv2.THRESH_OTSU
        )

        # -------------------------------------------------
        # INVERTED OTSU
        # -------------------------------------------------

        _, otsu_inv = cv2.threshold(
            sharpened,
            0,
            255,
            cv2.THRESH_BINARY_INV +
            cv2.THRESH_OTSU
        )

        # -------------------------------------------------
        # ADAPTIVE
        # -------------------------------------------------

        adaptive = cv2.adaptiveThreshold(
            sharpened,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            7
        )

        return [
            upscaled,
            gray,
            denoised,
            enhanced,
            sharpened,
            otsu,
            otsu_inv,
            adaptive
        ]

    except Exception:
        return []


# =========================================================
# ADD CROP SAFELY
# =========================================================

def add_crop(
    candidates,
    img,
    x1,
    y1,
    x2,
    y2
):

    h, w = img.shape[:2]

    x1 = max(
        0,
        int(x1)
    )

    y1 = max(
        0,
        int(y1)
    )

    x2 = min(
        w,
        int(x2)
    )

    y2 = min(
        h,
        int(y2)
    )

    if x2 <= x1 or y2 <= y1:
        return

    crop = img[
        y1:y2,
        x1:x2
    ]

    if crop.size == 0:
        return

    ch, cw = crop.shape[:2]

    if ch < 8 or cw < 30:
        return

    ratio = cw / float(ch)

    if 1.5 <= ratio <= 10.0:
        candidates.append(crop)


# =========================================================
# GENERATE PLATE CANDIDATES
# =========================================================

def generate_plate_candidates(img):

    candidates = []

    h, w = img.shape[:2]

    image_area = h * w

    # =====================================================
    # METHOD 1: EDGE + CONTOUR
    # =====================================================

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.bilateralFilter(
        gray,
        9,
        75,
        75
    )

    edges = cv2.Canny(
        blur,
        25,
        180
    )

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (7, 3)
    )

    edges = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True
    )

    for contour in contours[:250]:

        x, y, cw, ch = cv2.boundingRect(
            contour
        )

        if cw <= 0 or ch <= 0:
            continue

        ratio = cw / float(ch)

        area = cw * ch

        if ratio < 1.6 or ratio > 10:
            continue

        if cw < max(30, int(w * 0.12)):
            continue

        if ch < 7:
            continue

        if area < image_area * 0.00015:
            continue

        if area > image_area * 0.45:
            continue

        pad_x = int(cw * 0.20)
        pad_y = int(ch * 0.45)

        add_crop(
            candidates,
            img,
            x - pad_x,
            y - pad_y,
            x + cw + pad_x,
            y + ch + pad_y
        )


    # =====================================================
    # METHOD 2: WHITE PLATE DETECTION
    # =====================================================

    hsv = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2HSV
    )

    lower_white = np.array(
        [0, 0, 125],
        dtype=np.uint8
    )

    upper_white = np.array(
        [180, 100, 255],
        dtype=np.uint8
    )

    white_mask = cv2.inRange(
        hsv,
        lower_white,
        upper_white
    )

    white_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (9, 5)
    )

    white_mask = cv2.morphologyEx(
        white_mask,
        cv2.MORPH_CLOSE,
        white_kernel
    )

    white_mask = cv2.morphologyEx(
        white_mask,
        cv2.MORPH_OPEN,
        np.ones(
            (3, 3),
            np.uint8
        )
    )

    white_contours, _ = cv2.findContours(
        white_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in white_contours:

        x, y, cw, ch = cv2.boundingRect(
            contour
        )

        if cw <= 0 or ch <= 0:
            continue

        ratio = cw / float(ch)

        area = cw * ch

        if not 1.8 <= ratio <= 8.5:
            continue

        if area < image_area * 0.0002:
            continue

        pad_x = int(cw * 0.12)
        pad_y = int(ch * 0.35)

        add_crop(
            candidates,
            img,
            x - pad_x,
            y - pad_y,
            x + cw + pad_x,
            y + ch + pad_y
        )


    # =====================================================
    # METHOD 3: LOWER FRONT VEHICLE REGION
    #
    # Very important for tiny / blurry images.
    # Number plates are generally located in the lower
    # central front area.
    # =====================================================

    roi_y1 = int(h * 0.45)
    roi_y2 = int(h * 0.92)

    roi_x1 = int(w * 0.10)
    roi_x2 = int(w * 0.90)

    lower_roi = img[
        roi_y1:roi_y2,
        roi_x1:roi_x2
    ]

    if lower_roi.size > 0:

        rh, rw = lower_roi.shape[:2]

        # Several horizontal slices
        for frac1, frac2 in [
            (0.20, 0.55),
            (0.30, 0.70),
            (0.40, 0.85),
            (0.50, 0.95)
        ]:

            y1 = int(rh * frac1)
            y2 = int(rh * frac2)

            add_crop(
                candidates,
                lower_roi,
                0,
                y1,
                rw,
                y2
            )


        # Central plate-focused region
        add_crop(
            candidates,
            lower_roi,
            int(rw * 0.18),
            int(rh * 0.20),
            int(rw * 0.82),
            int(rh * 0.78)
        )


    # =====================================================
    # METHOD 4: CENTRAL LOWER STRIPS
    # =====================================================

    for y_start, y_end in [
        (0.52, 0.72),
        (0.58, 0.78),
        (0.64, 0.84),
        (0.68, 0.90)
    ]:

        add_crop(
            candidates,
            img,
            int(w * 0.18),
            int(h * y_start),
            int(w * 0.82),
            int(h * y_end)
        )


    # =====================================================
    # METHOD 5: FULL IMAGE
    # Last fallback only
    # =====================================================

    candidates.append(img)

    # =====================================================
    # REMOVE DUPLICATE / VERY SIMILAR CROPS
    # =====================================================

    final_candidates = []

    seen_shapes = set()

    for crop in candidates:

        if crop is None or crop.size == 0:
            continue

        ch, cw = crop.shape[:2]

        key = (
            round(cw / max(ch, 1), 1),
            round(cw / max(w, 1), 1),
            round(ch / max(h, 1), 1)
        )

        if key in seen_shapes:
            continue

        seen_shapes.add(key)

        final_candidates.append(crop)

    return final_candidates


# =========================================================
# FIND BEST PLATE
# =========================================================

def find_best_plate(
    reader,
    image
):

    if image is None:
        return None, None

    img = image.copy()

    # =====================================================
    # RESIZE LARGE IMAGES
    # =====================================================

    if img.shape[1] > 1600:

        scale = 1600 / img.shape[1]

        img = cv2.resize(
            img,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA
        )


    # =====================================================
    # GENERATE CANDIDATES
    # =====================================================

    candidates = generate_plate_candidates(
        img
    )

    # =====================================================
    # COLLECT OCR EVIDENCE
    # =====================================================

    evidence = []

    # Maximum OCR candidates to keep processing reasonable
    candidates = candidates[:80]

    for crop_index, crop in enumerate(
        candidates
    ):

        try:

            versions = enhance_plate_crop(
                crop
            )

            for version_index, version in enumerate(
                versions
            ):

                try:

                    results = reader.readtext(
                        version,
                        detail=1,
                        paragraph=False,
                        allowlist=(
                            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                            "0123456789"
                        ),
                        text_threshold=0.35,
                        low_text=0.20,
                        link_threshold=0.20,
                        mag_ratio=1.5
                    )

                except Exception:
                    continue


                for (
                    box,
                    detected_text,
                    confidence
                ) in results:

                    if not detected_text:
                        continue

                    detected_text = normalize_plate(
                        detected_text
                    )

                    if len(detected_text) < 7:
                        continue

                    plate = extract_valid_from_text(
                        detected_text
                    )

                    if plate is None:
                        continue

                    try:
                        confidence = float(
                            confidence
                        )

                    except Exception:
                        confidence = 0.0

                    format_score = plate_format_score(
                        plate
                    )

                    evidence.append(
                        {
                            "plate": plate,
                            "confidence": confidence,
                            "format_score": format_score,
                            "crop_index": crop_index,
                            "version_index": version_index
                        }
                    )

        except Exception:
            continue


    # =====================================================
    # NO VALID OCR
    # =====================================================

    if not evidence:
        return None, None


    # =====================================================
    # VOTING
    #
    # If several preprocessing versions detect the same
    # plate, increase its score.
    # =====================================================

    grouped = {}

    for item in evidence:

        plate = item["plate"]

        if plate not in grouped:

            grouped[plate] = {
                "count": 0,
                "confidence_sum": 0.0,
                "max_confidence": 0.0,
                "format_score": item["format_score"],
                "best_crop_index": item["crop_index"]
            }

        grouped[plate]["count"] += 1

        grouped[plate]["confidence_sum"] += (
            item["confidence"]
        )

        grouped[plate]["max_confidence"] = max(
            grouped[plate]["max_confidence"],
            item["confidence"]
        )


    # =====================================================
    # FINAL SCORING
    # =====================================================

    ranked = []

    for plate, data in grouped.items():

        average_confidence = (
            data["confidence_sum"]
            /
            max(data["count"], 1)
        )

        # Consensus bonus
        vote_bonus = min(
            data["count"] * 8,
            40
        )

        confidence_score = (
            average_confidence * 100
        )

        total_score = (
            data["format_score"]
            + confidence_score
            + vote_bonus
        )

        ranked.append(
            (
                total_score,
                plate,
                data
            )
        )


    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )


    # =====================================================
    # REQUIRE VALID INDIAN FORMAT
    # =====================================================

    for (
        total_score,
        plate,
        data
    ) in ranked:

        if not is_valid_indian_plate(
            plate
        ):
            continue

        # Strong enough evidence
        #
        # Because we already require a valid Indian
        # registration structure, this protects against
        # random OCR strings.
        if (
            data["count"] >= 2
            or data["max_confidence"] >= 0.45
        ):

            best_crop_index = data[
                "best_crop_index"
            ]

            best_crop = candidates[
                best_crop_index
            ]

            return (
                plate,
                best_crop
            )


    return (
        None,
        None
    )


# =========================================================
# GOOGLE SHEET SAVE
# =========================================================

def save_to_google_sheet(
    vehicle_number
):

    if (
        not WEB_APP_URL
        or
        "PASTE_YOUR" in WEB_APP_URL
    ):

        return (
            False,
            "Google Apps Script URL is not configured."
        )

    try:

        response = requests.post(
            WEB_APP_URL,
            json={
                "vehicle_number":
                    vehicle_number
            },
            timeout=20
        )

        response.raise_for_status()

        result = response.json()

        return (
            bool(
                result.get(
                    "success",
                    False
                )
            ),
            result.get(
                "message",
                "Unknown response"
            )
        )

    except requests.exceptions.Timeout:

        return (
            False,
            "Google Sheet request timed out."
        )

    except requests.exceptions.RequestException as e:

        return (
            False,
            f"Connection error: {e}"
        )

    except ValueError:

        return (
            False,
            "Invalid response from Google Apps Script."
        )

    except Exception as e:

        return (
            False,
            str(e)
        )


# =========================================================
# SESSION STATE
# =========================================================

if "last_saved_plate" not in st.session_state:
    st.session_state.last_saved_plate = ""


# =========================================================
# INPUT SECTION
# =========================================================

col1, col2, col3 = st.columns(
    3,
    gap="medium"
)


# =========================================================
# CAMERA
# =========================================================

with col1:

    render_html("""
    <div class="glass-card">

        <div class="card-icon">
            📷
        </div>

        <div class="card-title">
            Camera
        </div>

        <div class="card-subtitle">
            Capture vehicle image
        </div>

    </div>
    """)

    cam_file = st.camera_input(
        "Camera",
        key="camera_input",
        label_visibility="collapsed"
    )


# =========================================================
# GALLERY
# =========================================================

with col2:

    render_html("""
    <div class="glass-card">

        <div class="card-icon">
            🖼️
        </div>

        <div class="card-title">
            Gallery
        </div>

        <div class="card-subtitle">
            JPG / PNG
        </div>

    </div>
    """)

    gallery_file = st.file_uploader(
        "Gallery",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key="gallery_input",
        label_visibility="collapsed"
    )


# =========================================================
# TEXT ENTRY
# =========================================================

with col3:

    render_html("""
    <div class="glass-card">

        <div class="card-icon">
            ✍️
        </div>

        <div class="card-title">
            Text Entry
        </div>

        <div class="card-subtitle">
            Manual vehicle number
        </div>

    </div>
    """)

    text_input_val = st.text_input(
        "Manual Number",
        placeholder="MH29CD0038",
        key="text_input",
        label_visibility="collapsed"
    )


# =========================================================
# CAPTURE SECTION
# =========================================================

render_html("""
<div class="capture-title">

    <div class="capture-heading">
        📷 Capture Vehicle Image
    </div>

    <div class="capture-description">
        Select Camera or Gallery, then start AI detection.
    </div>

</div>
""")


# =========================================================
# ACTIVE IMAGE
# =========================================================

active_image = None


# =========================================================
# CAMERA IMAGE
# =========================================================

if cam_file is not None:

    active_image = cv2.imdecode(
        np.frombuffer(
            cam_file.getvalue(),
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )

    if active_image is not None:

        st.image(
            cv2.cvtColor(
                active_image,
                cv2.COLOR_BGR2RGB
            ),
            caption="Captured Vehicle Image",
            width="stretch"
        )


# =========================================================
# GALLERY IMAGE
# =========================================================

elif gallery_file is not None:

    active_image = cv2.imdecode(
        np.frombuffer(
            gallery_file.getvalue(),
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )

    if active_image is not None:

        st.image(
            cv2.cvtColor(
                active_image,
                cv2.COLOR_BGR2RGB
            ),
            caption="Uploaded Vehicle Image",
            width="stretch"
        )


# =========================================================
# DETECTION BUTTON
# =========================================================

detect_clicked = st.button(
    "🚀 START AI DETECTION",
    type="primary",
    width="stretch"
)


# =========================================================
# EXECUTION
# =========================================================

if detect_clicked:

    detected_plate = None
    cropped_img = None


    # =====================================================
    # IMAGE OCR
    # =====================================================

    if active_image is not None:

        with st.spinner(
            "🤖 AI Processing... Detecting and validating plate..."
        ):

            reader = load_ocr()

            (
                detected_plate,
                cropped_img
            ) = find_best_plate(
                reader,
                active_image
            )


    # =====================================================
    # MANUAL TEXT
    # =====================================================

    elif text_input_val:

        cleaned_manual = normalize_plate(
            text_input_val
        )

        if is_valid_indian_plate(
            cleaned_manual
        ):

            detected_plate = cleaned_manual

        else:

            st.error(
                "❌ Invalid Indian vehicle number format."
            )

            st.info(
                "Examples: "
                "MH29CD0038, "
                "DL01AB1234, "
                "KA01AB1234, "
                "24BH1234AA"
            )


    # =====================================================
    # NOTHING SELECTED
    # =====================================================

    else:

        st.warning(
            "⚠️ Please capture an image, "
            "upload a vehicle image, "
            "or enter a vehicle number."
        )


    # =====================================================
    # SUCCESSFUL DETECTION
    # =====================================================

    if detected_plate:

        render_html(
            f"""
            <div class="result-box">

                <div class="result-label">
                    ✓ VALIDATED NUMBER PLATE
                </div>

                <div class="plate-number">
                    {detected_plate}
                </div>

            </div>
            """
        )


        # =================================================
        # SHOW CROPPED PLATE
        # =================================================

        if cropped_img is not None:

            st.image(
                cv2.cvtColor(
                    cropped_img,
                    cv2.COLOR_BGR2RGB
                ),
                caption="AI Detected Plate Region",
                width=400
            )


        # =================================================
        # LOCAL DUPLICATE CHECK
        # =================================================

        if (
            st.session_state.last_saved_plate
            == detected_plate
        ):

            st.warning(
                f"⚠️ {detected_plate} "
                "was already processed recently. "
                "Duplicate request skipped."
            )

        else:

            # =============================================
            # GOOGLE SHEET SAVE
            # =============================================

            with st.spinner(
                "📊 Saving vehicle number to Google Sheet..."
            ):

                (
                    success,
                    message
                ) = save_to_google_sheet(
                    detected_plate
                )


            if success:

                st.session_state.last_saved_plate = (
                    detected_plate
                )

                st.success(
                    "✅ Vehicle number saved successfully "
                    "to Google Sheet!"
                )

            else:

                # Apps Script itself handles duplicate
                # vehicle numbers already present in Sheet.
                if "Duplicate" in message:

                    st.warning(
                        f"⚠️ {detected_plate} "
                        "already exists in Google Sheet."
                    )

                else:

                    st.warning(
                        f"⚠️ {message}"
                    )


    # =====================================================
    # NO PLATE DETECTED
    # =====================================================

    elif active_image is not None:

        st.error(
            "❌ Could not detect a valid Indian "
            "number plate."
        )

        st.info(
            "The AI rejected uncertain OCR results. "
            "Try an image where the plate occupies more "
            "pixels and is clearly visible."
        )


# =========================================================
# BOTTOM FLOW
# =========================================================

render_html("""
<div class="flow">

    <div class="flow-item">
        📷 Plate Detection
    </div>

    <div class="arrow">
        ›
    </div>

    <div class="flow-item">
        ✂️ Plate Crop
    </div>

    <div class="arrow">
        ›
    </div>

    <div class="flow-item">
        🔍 OCR + Validation
    </div>

    <div class="arrow">
        ›
    </div>

    <div class="flow-item">
        📋 Duplicate Check
    </div>

    <div class="arrow">
        ›
    </div>

    <div class="flow-item">
        📊 Google Sheet
    </div>

</div>
""")