import cv2
import sys
import progressbar
import os

print('*'*70)


if __name__ == '__main__':
  args_media = sys.argv[1]
  args_save = sys.argv[2]
  args_name = sys.argv[3]

  vidcap = cv2.VideoCapture(args_media)
  total_frame_count = vidcap.get(7)
  bar = progressbar.ProgressBar(maxval= total_frame_count, widgets=[args_name + '影片裁切進度:',progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
  bar.start()
  #save_folder = '/home/tina/workSpace/Project_Mouse/OUT_mask-video/2018-Sep-CFA-ipl-experiment_CFA_D1_diclofenac_treatment_1hr_3mg_kg_Diclofenec_TW/'
  success,image = vidcap.read()
  count = 1

  progress = '/data/.sinica_codes/gui/progress.txt'
  # print(progress)

  with open('/data/.sinica_codes/gui/progress.txt' ,'w') as f:
    f.writelines('0' + '\n')

  while success:
    #cv2.imwrite(args_save + "/frame.jpg" % count, image)  # save frame as JPEG file
    cv2.imwrite(args_save + "/frame" + str(count) + ".jpg", image)  # save frame as JPEG file
    bar.update(count)
    success, image = vidcap.read()
    count += 1
    if ((count % int(total_frame_count / 100) == 0) | (count == total_frame_count)):
      with open(progress ,'a') as f:
        f.writelines(str(int(count / total_frame_count * 100))+'\n')
        # print(str(int(count / total_frame_count * 100)))
    

    #print('Read a new frame: ', count)
    

  bar.finish()