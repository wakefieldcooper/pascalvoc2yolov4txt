import os
import json
from lxml import etree
from glob import iglob
from pathlib import Path
import argparse

def main():
    labels = {}
    categories = {}
    Path(args.input).mkdir(parents=True, exist_ok=True)
    Path(args.output).mkdir(parents=True, exist_ok=True)
    ##NOTE: May need to ensure it doesn't overwrite existing. not needed 
    #as functionality rn
    with open(os.path.join(args.output, 'manifest.txt'), 'w') as txtfile:
        for xml_file in os.scandir(args.input):
            with open(xml_file.path) as file:
                print(f'Processing file {xml_file.name}...')
                #create annotations object
                annotations = etree.fromstring(file.read())
                #extract 
                image_filename = annotations.find('filename').text
                boxes = annotations.iterfind('object')
                file_line = image_filename
                for box in boxes:
                    annotation_list = []
                    bndbox = box.find('bndbox')
                    xmin = str(bndbox.find('xmin').text)
                    ymin = str(bndbox.find('ymin').text)
                    xmax = str(bndbox.find('xmax').text)
                    ymax = str(bndbox.find('ymax').text)

                    label_name = box.find('name').text

                    if label_name not in labels:
                        labels[label_name] = len(labels)

                    class_id = labels[label_name]
                    categories[class_id] = label_name
                    annotation_list.extend((xmin, ymin, xmax, ymax, str(class_id)))
                    line = ','.join(annotation_list)
                    file_line = ' '.join((file_line, line))
            txtfile.write(f'{file_line}\n')
    txtfile.close()
    print(categories)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,
                        default='data/input',
                        help='Directory location of your input xmls',
                        required=True)
    parser.add_argument('--output', type=str,
                        default='data/output',
                        help='Directory location you want your output txts',
                        required=True)
    args = parser.parse_args()
    main()
