import cv2
import os
import sys
import progressbar
import skimage.io
from sklearn.externals import joblib
import xml.etree.cElementTree as ET
import numpy as np
import scipy.spatial.distance as dist
from sklearn import preprocessing
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pyqtgraph as pg


pain_tree = ET.ElementTree(file='C:/Users/kevin/Desktop/gui2/data/newdata/test.xml')
input_name = 'F:/mouse_eachframe/20200115_CFA_ipl_pain_face_B'
save_address = 'F:/mouse_eachframe/color_map/frame'

pain_root = pain_tree.getroot()
pain_child = []
for child_of_root in pain_root:
    pain_child.append(child_of_root)

Reye = []
Leye = []
Rear = []
Lear = []
nose = []
frame = []

for j in pain_child[3]:
    Reye.append([j.attrib.get('x'), j.attrib.get('y')])
for j in pain_child[4]:
    Leye.append([j.attrib.get('x'), j.attrib.get('y')])
for j in pain_child[5]:
    Rear.append([j.attrib.get('x'), j.attrib.get('y')])
for j in pain_child[6]:
    Lear.append([j.attrib.get('x'), j.attrib.get('y')])
for j in pain_child[7]:
    nose.append([j.attrib.get('x'), j.attrib.get('y')])
for j in pain_child[3]:
    frame.append([j.attrib.get('frame')])

Reye = np.array(Reye, dtype='int_')
Leye = np.array(Leye, dtype='int_')
Rear = np.array(Rear, dtype='int_')
Lear = np.array(Lear, dtype='int_')
nose = np.array(nose, dtype='int_')
frame = np.array(frame, dtype='int_')

pain_feature = np.array([Reye, Leye, Rear, Lear, nose])
n = pain_feature.shape[0]

md_matrix = []
for i in range(0, n):
    for j in range(i + 1, n):
        a = dist.cdist(pain_feature[i], pain_feature[j], metric='mahalanobis')
        b = a.diagonal()
        md_matrix.extend([b])

pain = []
for i in range(len(md_matrix[0])):
    pain.append(
        [md_matrix[0][i], md_matrix[1][i], md_matrix[2][i], md_matrix[3][i], md_matrix[4][i], md_matrix[5][i],
         md_matrix[6][i], md_matrix[7][i], md_matrix[8][i], md_matrix[9][i]])

min_max_scale = preprocessing.MinMaxScaler()
pain = min_max_scale.fit_transform(pain)

model = 'C:/Users/kevin/Desktop/gui2/data/SVR_linear/20200115_B.train'
with open(model,"rb+") as train:
    svr = joblib.load(train)
    predictpain = svr.predict(pain)

green = (0, 255, 0)
red = (0, 0, 255)
blue = (255, 0, 0)
i = 0
for name in os.listdir(input_name):
    name = name.split('frame')
    name = name[1].split('.jpg')
    name = name[0]

    input_image = cv2.imread(input_name + '/frame' + name + '.jpg')

    if int(name) == frame[i]:
        if predictpain[i] > 0.3:
            cv2.rectangle(input_image, (1400, 100), (1500, 200), red, -1)
            cv2.imwrite(save_address + name + '.jpg', input_image)
        elif predictpain[i] < -0.3:
            cv2.rectangle(input_image, (1400, 100), (1500, 200), green, -1)
            cv2.imwrite(save_address + name + '.jpg', input_image)
        else:
            cv2.rectangle(input_image, (1400, 100), (1500, 200), blue, -1)
            cv2.imwrite(save_address + name + '.jpg', input_image)
        i = i + 1
    else:
        cv2.imwrite(save_address + name + '.jpg', input_image)








