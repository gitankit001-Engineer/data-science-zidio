import os
import xml.etree.ElementTree as ET

ANNOTATIONS_FOLDER = r"D:\image captioning- CNN (ANKIT)\dataset\archive\VOC2012_train_val\Annotations"
OUTPUT_FILE = r"D:\image captioning- CNN (ANKIT)\dataset\archive\captions.txt"

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
    for xml_file in os.listdir(ANNOTATIONS_FOLDER):
        if not xml_file.endswith('.xml'):
            continue
        img_id = os.path.splitext(xml_file)[0]
        tree = ET.parse(os.path.join(ANNOTATIONS_FOLDER, xml_file))
        root = tree.getroot()
        objects = [obj.find('name').text for obj in root.findall('object')]
        caption = ' '.join(objects) + ' endseq'  # 'endseq' for LSTM sequence end
        f_out.write(f"{img_id}\t{caption}\n")
