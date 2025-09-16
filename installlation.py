import os
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.utils import Sequence

# --------- SETTINGS ---------
IMAGE_FOLDER = r"D:\image captioning- CNN (ANKIT)\dataset\archive\VOC2012_train_val\JPEGImages"
FEATURE_FOLDER = r"D:\image captioning- CNN (ANKIT)\dataset\archive\features"
METADATA_FILE = r"D:\image captioning- CNN (ANKIT)\dataset\archive\metadata.csv"
BATCH_SIZE = 500  # Number of images to process in one batch

# --------- LOAD MODEL ---------
base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')


# --------- HELPER FUNCTIONS ---------
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    return img_array


def save_features(img_id, features, save_dir=FEATURE_FOLDER):
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"{img_id}.npy")
    np.save(file_path, features)
    return file_path


# --------- BATCH PROCESSING ---------
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
metadata = []

for i in range(0, len(image_files), BATCH_SIZE):
    batch_files = image_files[i:i + BATCH_SIZE]
    batch_images = np.array([preprocess_image(os.path.join(IMAGE_FOLDER, f)) for f in batch_files])

    # Extract features for the whole batch
    batch_features = base_model.predict(batch_images, verbose=0)

    # Save features individually
    for j, img_file in enumerate(batch_files):
        img_id = os.path.splitext(img_file)[0]
        feature_file_path = save_features(img_id, batch_features[j])
        metadata.append({"image_id": img_id, "feature_file": feature_file_path})

    print(f"{i + len(batch_files)}/{len(image_files)} images processed...")

# --------- SAVE METADATA ---------
metadata_df = pd.DataFrame(metadata)
metadata_df.to_csv(METADATA_FILE, index=False)
print("Feature extraction complete!")
print(f"Features saved in '{FEATURE_FOLDER}'")
print(f"Metadata saved as '{METADATA_FILE}'")   


