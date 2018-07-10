#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 17:04:58 2018

@author: yyp
"""

import os
import sys
import xml.etree.ElementTree as ET
import glob

classes = ["bicycle", "bus", "car", "motorbike", "person"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def xml_to_txt(indir,outdir):

    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations)+'*.xml')
    
    file_dir_list = open('%s/trailval.txt'%(os.getcwd()), 'w')
    

    for i, file in enumerate(annotations):

        file_txt_label = file.split('.')[0]+'.txt'
        file_txt=os.path.join(outdir,file_txt_label)
        f_w_label = open(file_txt,'w')

        # actual parsing
        in_file = open(file)
        tree=ET.parse(in_file)
        root = tree.getroot()
        
        #get images path
        path = root.find('path').text
        file_dir_list.write(path+ '\n')
        
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
                current = list()
                name = obj.find('name').text

                xmlbox = obj.find('bndbox')
                xn = float(xmlbox.find('xmin').text)
                xx = float(xmlbox.find('xmax').text)
                yn = float(xmlbox.find('ymin').text)
                yx = float(xmlbox.find('ymax').text)
                
                b = (xn, xx, yn, yx)
                bb = convert((w,h), b)
                cls_id = classes.index(name)
                f_w_label.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

indir='/data/darknet/from-pic2/' #xml目录
outdir='/data/darknet/from-pic2/'  #txt目录

xml_to_txt(indir,outdir)
