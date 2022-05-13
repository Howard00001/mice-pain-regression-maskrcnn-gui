from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QMessageBox,QInputDialog
import os
from svm import trainmodel
import shutil


work_address = ''
path = './data'
folder_path = ''

def makefolder(text):
    global outside_path
    outside_path = os.path.join('/home/lorsmip/sinica_data',text)
    os.makedirs(outside_path)

    global docker_path
    docker_path = os.path.join('/data/sinica_data', text)


class oneSet(QtWidgets.QGroupBox):
    def __init__(self, numAddWidget,label):
        QtWidgets.QGroupBox.__init__(self)
        self.numAddWidget = numAddWidget
        self.label = label
        self.initSubject()
        self.organize()

    def initSubject(self):
        self.toolButton = QtWidgets.QToolButton()
        self.toolButton.setFixedSize(21,21)
        self.toolButton.setText("...")
        self.toolButton.clicked.connect(self.read_movie_file)
        self.textEdit = QtWidgets.QLineEdit()
        #self.textEdit.setFixedSize(241, 21)
        self.label_3 = QtWidgets.QLabel()
        #self.label_3.setFixedSize(81, 16)
        self.label_3.setText("選取" + self.label + "影片{}:".format(self.numAddWidget))

    def organize(self):
        layoutH = QtWidgets.QGridLayout(self)
        layoutH.addWidget(self.label_3,0,0)
        layoutH.addWidget(self.textEdit,0,1)
        layoutH.addWidget(self.toolButton,0,3)

    def read_movie_file(self):
        filename = QFileDialog.getOpenFileName(None,"選取"+ self.label +"影片","/home/lorsmip/sinica_videos","MP4 File (*.MP4 *.mp4)")
        self.root_movie = filename[0]
        name = self.root_movie.split('/',3)
        self.root_movie = os.path.join('/data',name[3])
        self.textEdit.setText(self.root_movie)


class Ui_train(object):
    def setupUi(self, Dialog):
        self.numAddWidget = 1
        self.saveFolder = []

        Dialog.setObjectName("Dialog")
        Dialog.resize(852, 541)
        Dialog.setWindowTitle("Trainning Windows")
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(340, 360, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Train")
        self.pushButton.clicked.connect(self.start)

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(560, 30, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("健康老鼠")

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(170, 440, 58, 15))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(150, 480, 71, 20))
        self.label_6.setObjectName("label_6")
        self.label_4.setText("總進度")
        self.label_6.setText("段落進度")

        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(230, 440, 361, 21))
        self.progressBar.setProperty("value", 100)
        self.progressBar.setObjectName("progressBar")

        self.progressBar_2 = QtWidgets.QProgressBar(Dialog)
        self.progressBar_2.setGeometry(QtCore.QRect(230, 480, 361, 21))
        self.progressBar_2.setProperty("value", 100)
        self.progressBar_2.setObjectName("progressBar_2")

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(800, 210, 31, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("+")
        self.pushButton_2.clicked.connect(self.addSet)

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(800, 160, 31, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("-")
        self.pushButton_3.clicked.connect(self.delSet)

        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(10, 70, 381, 261))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 379, 259))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(160, 30, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("疼痛老鼠")

        self.scrollArea_2 = QtWidgets.QScrollArea(Dialog)
        self.scrollArea_2.setGeometry(QtCore.QRect(400, 70, 381, 261))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 379, 259))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        ###1
        self.set1 = []
        self.box1 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.set1.append(oneSet(self.numAddWidget,'疼痛'))
        self.box1.addWidget(self.set1[0])
        ###2
        self.set2 = []
        self.box2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.set2.append(oneSet(self.numAddWidget,'健康'))
        self.box2.addWidget(self.set2[0])
        ###
        
    def addSet(self):
        self.numAddWidget += 1
        self.set1.append(oneSet(self.numAddWidget,'疼痛'))
        self.set2.append(oneSet(self.numAddWidget,'健康'))
        self.box1.addWidget(self.set1[self.numAddWidget-1])
        self.box2.addWidget(self.set2[self.numAddWidget-1])

    def delSet(self):
        self.box1.removeWidget(self.set1[self.numAddWidget-1])
        self.set1[self.numAddWidget-1].deleteLater()
        self.set1.pop()
        self.box2.removeWidget(self.set2[self.numAddWidget-1])
        self.set2[self.numAddWidget-1].deleteLater()
        self.set2.pop()
        self.numAddWidget -= 1


    def iterate(self):
        for i in range(self.numAddWidget-1):
            self.root_pain_movie.append(self.set1[i])
            self.root_health_movie.append(self.set2[i])
            self.start(self)

    def start(self):
        import os
        self.saveFolder = [] 
        for i in range(self.numAddWidget):
            text, ok = QInputDialog.getText(None, 'select save folder', '儲存資料夾名稱 {}'.format(i+1))
            
            if not os.path.isdir('/home/lorsmip/sinica_data/' + text):
                self.saveFolder.append(text)
                makefolder(text)
            else:
                while(os.path.isdir('/home/lorsmip/sinica_data/' + text)):
                    msg = QMessageBox()
                    msg.setText("目的地已有該資料夾，請重新命名")
                    msg.setWindowTitle("MessageBox demo")
                    retval = msg.exec_()
                    text, ok = QInputDialog.getText(None, '', '儲存資料夾名稱 {}'.format(i+1))
                makefolder(text)
                self.saveFolder.append(text)
        self.progressBar.setProperty("value", 0)
        mainProgress = 0
        msgW = []
        error = 0
        for i in range(self.numAddWidget):
            self.progressBar_2.setProperty("value", 0)
            self.root_pain_movie = self.set1[i].root_movie
            self.root_health_movie = self.set2[i].root_movie

            # makefolder(self.saveFolder[i])
            work_PWD = '/data/.sinica_codes/gui/'
            global outside_path
            global docker_path

            os.makedirs(outside_path + '/pain')
            os.makedirs(outside_path + '/health')

            paintxt = open(outside_path + '/pain.txt', "w")
            healthtxt = open(outside_path + "/health.txt", "w")
            painxml = open(outside_path + "/pain.xml", "w")
            healthxml = open(outside_path + "/health.xml", "w")
            self.root_pain_txt = docker_path + '/pain.txt'
            self.root_health_txt = docker_path + '/health.txt'
            self.root_pain_xml = docker_path + '/pain.xml'
            self.root_health_xml = docker_path + '/health.xml'
            progress_txt = '/home/lorsmip/.sinica_codes/gui/progress.txt'
            model = work_PWD + "maskrcnn/mask_rcnn_mouseface1001_imagenet_0030.h5"

            os.system("sudo docker exec -i sinica_running_docker python3 " + work_PWD +  "ViToIm.py " + self.root_pain_movie + " " + docker_path + "/pain " + "疼痛 &")
            ###get progress
            while(1):
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(4000, loop.quit)
                loop.exec_()
                
                with open(progress_txt,'r') as f:  ##############progress file
                    tmp = f.readlines()
                    progress = int(tmp[-1])
                
                self.progressBar_2.setProperty("value", progress)
                if progress == 100:
                    break
            mainProgress = mainProgress+25/self.numAddWidget
            self.progressBar.setProperty("value", mainProgress)
            ###process done
            print("疼痛影片切割完成")

            os.system(
                "sudo docker exec -i sinica_running_docker python3 " + work_PWD + "createImagesList.py --imageLoc " + docker_path + "/pain" + " --saveFile " + docker_path + "/pain.txt")
            print("pain txt 完成")

            paintxt.close()

            os.system(
                "sudo docker exec -i sinica_running_docker python3 " + work_PWD + "maskrcnn/main_mouseDectect.py -imagesList {:} -facialFeatureLog {:} -model {:} 1 &".format(
                    self.root_pain_txt, self.root_pain_xml, model))
            
            with open(progress_txt ,'w') as f:
                f.writelines("0\n")

            while(1):
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(4000, loop.quit)
                loop.exec_()
                
                with open(progress_txt,'r') as f:  ##############progress file
                    tmp = f.readlines()
                    progress = int(tmp[-1])
                
                self.progressBar_2.setProperty("value", progress)
                if progress == 100:
                    break
            mainProgress = mainProgress+25/self.numAddWidget
            self.progressBar.setProperty("value", mainProgress)
            print("pain xml 完成")
            shutil.rmtree(outside_path + "/pain")
            painxml.close()

            # ----------------------------------------------------------------------------------------------------------------------

            os.system("sudo docker exec -i sinica_running_docker python3 " + work_PWD + "ViToIm.py " + self.root_health_movie + " " + docker_path + "/health " + "健康 &")
            ###get progress
            while(1):
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(4000, loop.quit)
                loop.exec_()
                with open(progress_txt,'r') as f:  ##############progress file
                    tmp = f.readlines()
                    progress = int(tmp[-1])
                self.progressBar_2.setProperty("value", progress)
                if progress == 100:
                    break
            mainProgress = mainProgress+25/self.numAddWidget
            self.progressBar.setProperty("value", mainProgress)
            ###process done
            
            print('健康影片切割完成')

            os.system(
                "sudo docker exec -i sinica_running_docker python3 " + work_PWD + "createImagesList.py --imageLoc " + docker_path + "/health" + " --saveFile " + docker_path + "/health.txt")
            print("health txt 完成")

            healthtxt.close()

            os.system(
                "sudo docker exec -i sinica_running_docker python3 " + work_PWD + "maskrcnn/main_mouseDectect.py -imagesList {:} -facialFeatureLog {:} -model {:} 2 &".format(
                    self.root_health_txt, self.root_health_xml, model))
            ###get progress


            with open(progress_txt ,'w') as f:
                f.writelines("0\n")


            while(1):
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(4000, loop.quit)
                loop.exec_()
                with open(progress_txt,'r') as f:  ##############progress file
                    tmp = f.readlines()
                    progress = int(tmp[-1])
                self.progressBar_2.setProperty("value", progress)
                if progress == 100:
                    break
            mainProgress = mainProgress+25/self.numAddWidget
            self.progressBar.setProperty("value", mainProgress)
            ###process done
            print("health xml 完成")
            shutil.rmtree(outside_path + "/health")
        
            healthxml.close()

            pain = outside_path + "/pain.xml"
            no_pain = outside_path + "/health.xml"

            trainNum1 = "/home/lorsmip/.sinica_codes/gui/trainNum1.txt"
            trainNum2 = "/home/lorsmip/.sinica_codes/gui/trainNum2.txt"
            check = True
            with open(trainNum1,"r") as f:
                if int(f.readline()) < 10:
                    check = False
            with open(trainNum2,"r") as f:
                if int(f.readline()) < 10:
                    check = False
            
            if check:
                trainmodel.svr(pain,no_pain,outside_path)
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(4000, loop.quit)
                loop.exec_()
                mainProgress = 100*(i+1)/self.numAddWidget
                self.progressBar.setProperty("value", mainProgress)
            else:
                msgW.append(QMessageBox())
                msgW[error].setText("Training {:} less than 10 samples".format(self.saveFolder[i]))
                msgW[error].setWindowTitle("Warning")
                msgW[error].show()
                error = error + 1

        msg = QMessageBox()
        msg.setText("Training_Finish")
        msg.setWindowTitle("MessageBox demo")
        retval = msg.exec_()
        