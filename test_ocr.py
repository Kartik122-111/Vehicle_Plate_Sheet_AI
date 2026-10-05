import cv2
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

image_path = "number_plate.jpg"
image = cv2.imread(image_path)

if image is None:
    print("❌ Image not found!")
    exit()

# Resize image
image = cv2.resize(image, None, fx=2, fy=2)

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Improve contrast
gray = cv2.equalizeHist(gray)

# Threshold
_, thresh = cv2.threshold(
    gray, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

images = {
    "Original": image,
    "Grayscale": gray,
    "Threshold": thresh
}

print("\n========== VEHICLE NUMBER OCR ==========\n")

for name, img in images.items():

    results = reader.readtext(
        img,
        detail=1,
        allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    )

    print(f"--- {name} ---")

    if results:
        for result in results:
            text = result[1]
            confidence = result[2]

            print(
                "Detected:",
                text,
                "| Confidence:",
                round(confidence, 2)
            )
    else:
        print("❌ Nothing detected")

    print()

print("========================================")