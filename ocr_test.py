import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv2.imread("test.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

text = pytesseract.image_to_string(gray, config='--oem 3 --psm 6')
lines = [l.strip() for l in text.split("\n") if l.strip()]

print("\nRAW OCR TEXT:\n", text)

# -----------------------------
# FIND DOB LINE INDEX
# -----------------------------
dob = "Not found"
dob_index = -1

for i, line in enumerate(lines):
    match = re.search(r'\d{2}/\d{2}/\d{4}', line)
    if match:
        dob = match.group()
        dob_index = i
        break

# -----------------------------
# FIND GENDER
# -----------------------------
gender = "Not found"
if "FEMALE" in text.upper():
    gender = "FEMALE"
elif "MALE" in text.upper():
    gender = "MALE"

# -----------------------------
# FIND NAME (ABOVE DOB)
# -----------------------------
name = "Not found"

blocked_words = [
    "DOB", "YEAR", "GOVERNMENT", "INDIA", "UIDAI",
    "AADHAAR", "IDENTITY", "MALE", "FEMALE",
    "BIRTH", "PROOF"
]

if dob_index != -1:
    for j in range(dob_index - 1, -1, -1):
        line = lines[j]

        if (
            2 <= len(line.split()) <= 4 and
            line.replace(" ", "").isalpha() and
            not line.isupper() and
            not any(word in line.upper() for word in blocked_words)
        ):
            name = line.replace(":", "").strip()
            break

print("\n===== EXTRACTED DETAILS =====")
print("Name   :", name)
print("DOB    :", dob)
print("Gender :", gender)
print("=============================")
