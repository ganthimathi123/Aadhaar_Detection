import cv2
import os

input_folder = 'train/'
output_folder = 'train_processed/'
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.endswith(".jpg") or file.endswith(".png"):
        img = cv2.imread(os.path.join(input_folder, file))
        img = cv2.resize(img, (1024, 1024))
        # Optional: enhance image
        cv2.imwrite(os.path.join(output_folder, file), img)
