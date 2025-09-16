import os
import random
from PIL import Image
import matplotlib.pyplot as plt

IMAGES_DIR = 'D:/image captioning- CNN (ANKIT)/dataset/archive/VOC2012_train_val/JPEGImages/'
CAPTION_FILE = 'D:/image captioning- CNN (ANKIT)/dataset/archive/captions.txt'

captions_dict = {}
with open(CAPTION_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if '\t' in line:
            img_name, caption = line.split('\t')
            captions_dict[img_name] = caption

print(f"✅ Total captions loaded: {len(captions_dict)}")

image_filename = random.choice(list(captions_dict.keys()))
image_path = os.path.join(IMAGES_DIR, image_filename)

if not image_filename.lower().endswith('.jpg'):
    image_path += '.jpg'

caption = captions_dict[image_filename]

# 🚀 Clean special tokens
caption = caption.replace('startseq', '').replace('endseq', '').strip()

image = Image.open(image_path)
plt.figure(figsize=(8, 6))
plt.imshow(image)
plt.axis('off')
plt.title(f"Generated Caption:\n{caption}", fontsize=14)
plt.show()
