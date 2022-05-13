
import os
import tensorflow as tf

def findJpgFile(filePath):
    for root, dirs, files in os.walk(filePath):
        for file in files:
            if file.endswith(".jpg"):
                yield [os.path.join(root, file), root]

def writeFiles(fileName,loc):
    # os.rename(fileName, fileName.replace(' ', '_'))
    # print(": working status=> {:<70}".format(fileName.replace(' ', '_')))

    print(f"{fileName}", file=loc)

    return 0

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Create Images list.')
    parser.add_argument('--imageLoc', required=False,
                        metavar="/path/to/dataset/",
                        help='Directory of the imagess')
    parser.add_argument('--saveFile', required=False,
                        metavar="/path/to/saveFile/",
                        help='Path to save file')
    args = parser.parse_args()

    jpgPath = args.imageLoc

    # for name in os.listdir(jpgPath):
    #     print(name)
    with tf.device('/device:GPU:0'):
       # '/dev/NAS-Server/小鼠資料庫/2018-Feb-CFA-experiment/pre-CFA/SW/'

        with open(args.saveFile, "w") as text_file:
            for i in range(len(os.listdir(jpgPath))):
                a = i + 1
                file_name = jpgPath + '/frame' + str(a) + '.jpg'
                writeFiles(fileName=file_name,loc=text_file)

        #     for file, root in findJpgFile(filePath=jpgPath):
        #         writeFiles(fileName=file,loc=text_file)
        # text_file.close()
