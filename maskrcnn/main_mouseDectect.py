import os
import numpy as np
import skimage.io
import yaml
import tensorflow as tf
import coco
import model as modellib
# import visualize_cuz as visualize
import xml.etree.cElementTree as ET
import time
import progressbar

###########################################################
#  XML
###########################################################
class xmlManager(object):
    def __init__(self, filePath):
        self.root = ET.Element("root")
        self.filePath = filePath
        self.handle=[]

    def createDescriptor(self, name, tag):
        self.handle = []
        self.handle = ET.SubElement(self.root, str(tag), name=str(name))
        return self.handle

    def updateDescriptor(self, tag, value):
        ET.SubElement(self.handle, str(tag)).text = str(value)

    def saveFile(self):
        tree = ET.ElementTree(self.root)
        tree.write(self.filePath)

def xmlConfigWritting():
    xml.createDescriptor(name="Mask-RCNN", tag="config")
    xml.updateDescriptor(tag="configName", value=str(config.name))
    xml.updateDescriptor(tag="MODEL_DIR", value=str(MODEL_DIR))
    xml.updateDescriptor(tag="COCO_MODEL_PATH", value=str(COCO_MODEL_PATH))
    xml.updateDescriptor(tag="DETECTION_MIN_CONFIDENCE", value=str(config.DETECTION_MIN_CONFIDENCE))
    xml.updateDescriptor(tag="NUM_CLASSES", value=str(config.NUM_CLASSES))
    xml.updateDescriptor(tag="STEPS_PER_EPOCH", value=str(config.STEPS_PER_EPOCH))
    xml.saveFile()

    xml.createDescriptor(name="testVideos", tag="sourcefile")
    xml.updateDescriptor(tag="IMGLIST", value=str(args_imagesList))
    xml.updateDescriptor(tag="facialFeatureLog", value=str(args_facialFeatureLog))

    xml.saveFile()
    return 0

def recordBoxInfo(boxes, masks, class_ids, class_names, frame, scores=None):
    num_face = sum(class_ids == 1)
    num_ear = sum(class_ids == 2)
    num_eye = sum(class_ids == 3)
    num_nose = sum(class_ids == 4)
    if (num_ear > 1) and (num_eye > 1) and (num_nose == 1):
        # Number of instances
        N = boxes.shape[0]
        if not N:
            print("\n*** No instances to display *** \n")
        else:
            assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

        # seperate eyes
        LeyeX = False
        ReyeX = False
        for i in range(N):
            # Bounding box
            if not np.any(boxes[i]):
                # Skip this instance. Has no bbox. Likely lost in image cropping.
                continue
            y1, x1, y2, x2 = boxes[i]
            X = x1
            # Label
            class_id = class_ids[i]
            label = class_names[class_id]
            if label == 'eye':
                if not (LeyeX or ReyeX):
                    LeyeX = int(X)
                    ReyeX = int(X)
                else:
                    if int(X) < LeyeX:
                        LeyeX = int(X)
                    elif int(X) > ReyeX:
                        ReyeX = int(X)
        # seperate ears
        LearX = False
        RearX = False
        for i in range(N):
            # Bounding box
            if not np.any(boxes[i]):
                # Skip this instance. Has no bbox. Likely lost in image cropping.
                continue
            y1, x1, y2, x2 = boxes[i]
            X = x1
            # Label
            class_id = class_ids[i]
            label = class_names[class_id]
            if label == 'ear':
                if not (LearX or RearX):
                    LearX = int(X)
                    RearX = int(X)
                else:
                    if int(X) < LearX:
                        LearX = int(X)
                    elif int(X) > RearX:
                        RearX = int(X)

        for i in range(N):
            # Bounding box
            if not np.any(boxes[i]):
                # Skip this instance. Has no bbox. Likely lost in image cropping.
                continue
            y1, x1, y2, x2 = boxes[i]
            X = x1
            Y = y1
            width = x2 - x1
            height = y2 - y1

            # Label
            class_id = class_ids[i]
            label = class_names[class_id]
            score = scores[i] if scores is not None else None

            if label == 'face':
                ET.SubElement(xmlFaceHandle, "bbox", frame=str(frame),
                              x=str(X), y=str(Y), width=str(width), height=str(height), score=str(score)
                              )
            elif label == 'ear':
                if int(X) == LearX:
                    ET.SubElement(xmlLearHandle, "bbox", frame=str(frame),
                                  x=str(X), y=str(Y), width=str(width), height=str(height), score=str(score)
                                  )
                elif int(X) == RearX:
                    ET.SubElement(xmlRearHandle, "bbox", frame=str(frame),
                                  x=str(X), y=str(Y), width=str(width), height=str(height), score=str(score)
                                  )
            elif label == 'eye':
                if int(X) == LeyeX:
                    ET.SubElement(xmlLeyeHandle, "bbox", frame=str(frame),
                                  x=str(X), y=str(Y), width=str(width), height=str(height), score=str(score)
                                  )
                elif int(X) == ReyeX:
                    ET.SubElement(xmlReyeHandle, "bbox", frame=str(frame),
                                  x=str(X), y=str(Y), width=str(width), height=str(height), score=str(score)
                                  )
            elif label == 'nose':
                ET.SubElement(xmlNoseHandle, "bbox", frame=str(frame),
                              x=str(X), y=str(Y), width=str(width), height=str(height), score=str(score)
                              )
        return 1
    return 0

###########################################################
#  Ground truth
###########################################################



if __name__ == '__main__':

    start = time.time()
    tfconfig = tf.ConfigProto()
    tfconfig.gpu_options.allow_growth = True
    tfconfig.gpu_options.per_process_gpu_memory_fraction = 0.7
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

    # config
    # import argparse
    # parser = argparse.ArgumentParser(description='Create Images list.')
    # parser.add_argument('-imagesList', required=True,
    #                     metavar="/path/to/file/",
    #                     help='Path to the file which contains images list. e.g./home/tina/workSpace/Project_Mouse/info.txt')
    # parser.add_argument('-facialFeatureLog', required=True,
    #                     metavar="/path/to/log/",
    #                     help='Path to the log which saves facial features. '+'\n'+
    #                          'e.g./home/tina/workSpace/Project_Mouse/result/post-CFA_Diclofenac_10mg_kg_drug_3hr_BK_test.xml')
    # parser.add_argument('-model', required=True,
    #                     metavar="/path/to/model/",
    #                     help='Path to mode e.g. /home/tina/workSpace/Project_Mouse/Mask_RCNN/mask_rcnn_mouseface1001_imagenet_0030.h5')
    # parser.add_argument('--saveImg', required=False,
    #                     metavar="/path/to/save/imglog/",
    #                     help='Path to the save image. e.g./home/tina/workSpace/Project_Mouse/result/imgs/')
    # parser.add_argument('--earThreshold', required=False,
    #                     metavar="number of ear greater than X",
    #                     help='The condition of saving images, save only the detected amount of ears greater than threshold e.g. amount of ears >= threshold')
    # parser.add_argument('--eyeThreshold', required=False,
    #                     metavar="number of eye greater than X",
    #                     help='The condition of saving images, save only the detected amount of eyes greater than threshold e.g. amount of eyes >= threshold')
    # args = parser.parse_args()
    import sys
    print('*'*70)
    print(len(sys.argv))
    if len(sys.argv) != 8:
        raise IndexError("The arguments should be 1.imgsList , 2. facialFeatureLog, 3.model path ")

    args_model = sys.argv[6]
    args_facialFeatureLog = sys.argv[4]
    args_imagesList = sys.argv[2]

    with tf.device('/device:GPU:0'):  # # # # # #
        OPTION_RESTRICTION = "all" # frontFaceOnly or others or all

        ROOT_DIR = os.getcwd()
        MODEL_DIR = os.path.join(ROOT_DIR, "logs")
        # COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_mouseface1001_imagenet_0030.h5") # mask_rcnn_coco.h5
        COCO_MODEL_PATH = args_model
        # COCO_MODEL_PATH = '../maskrcnn/mask_rcnn_mouseface1001_imagenet_0030.h5'

        class GroundTruth(object):
            def __init__(self, folderPath, fileList, loadingObject="GROUND_TRUTH"):
                self.loadingObject = loadingObject
                self.folderPath = folderPath
                self.fileList = fileList
                self.index = len(fileList)

            def __str__(self):
                print("--")
                print("  name : {:<10}".format(self.loadingObject.center(20, '*')))
                print("  fileList      :" + str(self.fileList))
                print("  folder path   : {:<30}".format(self.folderPath))
                return '\n'

            def __iter__(self):
                return self

            def __next__(self):
                if self.index == 0:
                    raise StopIteration
                self.index = self.index - 1
                return [self.folderPath, self.fileList[len(self.fileList) - self.index - 1]]

        class InferenceConfig(coco.CocoConfig):
            # Set batch size to 1 since we'll be running inference on
            # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1
            DETECTION_MIN_CONFIDENCE = 0.7
            name = "MouseFace"
            # name = "shape"
            NUM_CLASSES = 5
            STEPS_PER_EPOCH = 100

        config = InferenceConfig()
        config.display()

        # Create model object in inference mode.
        model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

        # Load weights trained on MS-COCO
        model.load_weights(COCO_MODEL_PATH, by_name=True)

        # COCO Class names
        class_names = ['BG', 'face', 'ear', 'eye', 'nose']

        # XML
        xml = xmlManager(
            filePath=args_facialFeatureLog)

        xmlConfigWritting()

        xmlFaceHandle = xml.createDescriptor(name="face", tag="attribute")
        xmlReyeHandle = xml.createDescriptor(name="Reye", tag="attribute")
        xmlLeyeHandle = xml.createDescriptor(name="Leye", tag="attribute")
        xmlRearHandle = xml.createDescriptor(name="Rear", tag="attribute")
        xmlLearHandle = xml.createDescriptor(name="Lear", tag="attribute")
        xmlNoseHandle = xml.createDescriptor(name="nose", tag="attribute")

        stack = []
        with open(args_imagesList) as fp:
            for imgPath in fp:
                if 'jpg' in imgPath:
                    stack.append(imgPath.strip())
        frame = 0
        get = 0
        maxBarLen = len(stack)
        bar = progressbar.ProgressBar(maxval=maxBarLen, widgets=['五官偵測中:', progressbar.Bar('*', '[', ']'), ' ',
                                                                         progressbar.Percentage()])
        bar.start()
        print('*' * 35 + '{:^30}'.format('AUTO LABELING FOR FACIAL FEATURE') + '*' * 35)
        progress = '/data/.sinica_codes/gui/progress.txt'
        
        while stack:
            # print('PROCESS [{:10}]'.format('*'*(int(frame*10) // maxBarLen)))
            # print(frame/maxBarLen)
            bar.update(frame)
            imgLoc = stack.pop(0)
            image = skimage.io.imread(imgLoc) # imgPath
            which_frame = imgLoc.split('\\')
            name_size = len(which_frame)
            which_frame = which_frame[name_size - 1].split('frame')
            which_frame = which_frame[1].split('.jpg')
            which_frame = which_frame[0]
            results = model.detect([image], verbose=0)
            r = results[0]

            get = get + recordBoxInfo(r['rois'], r['masks'], r['class_ids'], class_names, int(which_frame), r['scores'])
            frame += 1

            if ((frame % int(maxBarLen / 100) == 0) | (frame == maxBarLen)):
                with open(progress ,'a') as f:
                    f.writelines(str(int(frame / maxBarLen * 100))+'\n')

            
            xml.saveFile()
            
        print('*' * 35 + '{:^30}'.format('END') + '*' * 35)

        if sys.argv[7] == '1':
            trainNum = '/data/.sinica_codes/gui/trainNum1.txt'
        else:
            trainNum = '/data/.sinica_codes/gui/trainNum2.txt'
        with open(trainNum,"w") as f:
            f.writelines(str(get))


        
