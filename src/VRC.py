import argparse, os
import cv2
from Mog2 import Mog2MotionDetector
from window_utils import winMouseControl

def argparses():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s',action="store",dest="video_savepath",type=str,default=None,help="Store path dir (Ex:D:/python/source/storedir)")
    parser.add_argument('-f',action="store",dest="video_filename",type=str,default=None,help="Input videofilename_dir (Ex:D:/python/source/testname.mp4)")
    # parser.add_argument('-fl',action="store",dest="video_listname",type=str,default=None,help="Input videolistname_dir (Ex:D:/python/source/testdir)")
    # parser.add_argument('-err',action='store',dest='err_low_limit',type=int,default=1000,help='MOG err low thresold(default=1000)')
    # parser.add_argument('-sp',action='store',dest='speed',type=float,default=1,help='Video speed up')
    # parser.add_argument('-pt',action='store',dest='pass_time',type=float,default=0.5,help='If pass roi region time upon on (-pt) secs will be record(default=0.5s)')
    # parser.add_argument('-ed',action='store',dest='early_delay',type=float,default=7,help='Record time will earilier (-ed) secs (default=7s) ')
    # parser.add_argument('-ld',action='store',dest='late_delay',type=float,default=5,help='Record time will later (-ld) secs (default=5s) ')
    # parser.add_argument('-rt',action='store_true',dest='record_time_to_txt',default=False,help='Record time to txt (default=False)')
    # parser.add_argument('-vrt',action='store_true',dest='video_record_time',default=False,help='Record time to video (default=False)')
    # parser.add_argument('-eimg',action='store_true',dest='err_imshow',default=False,help='Inshow err_img (default=False)')
    # parser.add_argument('-sroi',action='store_true',dest='store_roi',default=False,help='If True store the region of roi (default=False)')

    args = parser.parse_args()
    if args.video_savepath is None:
        parser.print_help()
        return None
    else:
        return args

def main():
    # Get the argv and argc value
    args = argparses()

    winMCSize = (640, 480)
    winMCName = "ROI"
    capExposureValue = -4.0
    capAutoFocus = 0
    frameWindowName = "Result"
    maxObjectAreaThreshRatio = 0.5
    minObjectArea = 200
    mogBackGroundRatio = 0.5


    # Get the video capture
    cap = cv2.VideoCapture(0) 
    if cap.isOpened() == False:
        return -1

    # Call the window control member
    winMC = winMouseControl(winMCName)

    # Get frame from the camera
    _, frame = cap.read()

    winMC.setFrame(frame)
    winMC.showFrame(winMCSize)
    # Get ROI region from the winMouseContoll method
    selectROI = winMC.getROIRegion()

    # Adjust the camera parameter
    cap.set(cv2.CAP_PROP_EXPOSURE, capExposureValue)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, capAutoFocus)

    cv2.namedWindow(frameWindowName)
    # Init the mog2 foreground object class
    Mog2 = Mog2MotionDetector(mogBackGroundRatio)

    while True:
        _, frame = cap.read()
        
        
        foreground, err = Mog2.mse(frame)
        foregroundObject = Mog2.findForegroundObject(foreground, minObjectArea, maxObjectAreaThreshRatio)

        for obj in foregroundObject:
            cv2.rectangle(frame, (obj[0], obj[1]), (obj[0] + obj[2], obj[1] + obj[3]), (0, 0, 255), 2)


        # Draw the analysis region 
        cv2.rectangle(frame, selectROI[:2], selectROI[2:], (0, 255, 0), 2)        
        cv2.imshow(frameWindowName, frame)   

        
        if cv2.waitKey(1) == 27:
            break
    
    
main()
