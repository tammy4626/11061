
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

#('0714', 'train'), ('0714', 'valid'),
sets=[('0714','test')]

classes = [ "None","text","btn-active","row","single","double","quadruple","small-title","start","menu","next","back","play","cancel"]

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
    in_file = open('train%s/Annotations/%s.xml'%(year, image_id))
    out_file = open('train%s/labels/%s.txt'%(year, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()


for year, image_set in sets:
    if not os.path.exists('train%s/labels/'%(year)):
        os.makedirs('train%s/labels/'%(year))
    image_ids = open('train%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/train%s/JPEGImages/difficult_%s.jpg\n'%(wd, year, image_id))
        convert_annotation(year, image_id)
    list_file.close()


# for year, image_set in sets:
#     if not os.path.exists('VOCdevkit/VOC%s/labels/'%(year)):
#         os.makedirs('VOCdevkit/VOC%s/labels/'%(year))
#     image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
#     list_file = open('%s_%s.txt'%(year, image_set), 'w')
#     for image_id in image_ids:
#         list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
#         convert_annotation(year, image_id)
#     list_file.close()


#os.system("train.txt")
#os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")
