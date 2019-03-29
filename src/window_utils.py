import cv2
import numpy as np

class winMouseControl:
    def __init__(self, windowName):
        '''
        This is the window mouse control class method.
        `windowName` is the main window name. 
        '''
        # Mouse control flag
        self.flag = -1
        self.done = -1
        self.buttonDownX = -1
        self.buttonDownY = -1
        self.buttonUpX = -1
        self.buttonUpY = -1

        # Original frame
        self.frame = None
        # Processing frame
        self.temp = None
        # Frame size 
        self.frameSize = None

        # Main window name
        self.windowName = windowName
        
    
    def mouse_callback(self, event, x, y, flags, param):
        '''
        Mouse callback function
        '''
        # if mouse button down
        if event == cv2.EVENT_LBUTTONDOWN:
            self.flag = 1
            self.done = 0
            self.buttonDownX, self.buttonDownY = x, y
            # Copy the original frame to process frame
            self.temp = np.copy(self.frame)           
        
        if event == cv2.EVENT_LBUTTONUP:
            self.flag = 0
            self.done = 1
            self.buttonUpX, self.buttonUpY = x, y

            print((self.buttonDownX, self.buttonDownY, self.buttonUpX, self.buttonUpY))

        if event == cv2.EVENT_MOUSEMOVE:
            # when left button press down 
            if self.flag == 1 and self.done == 0:
                self.temp = np.copy(self.frame)
                # Draw the red rectangle if the left mouse press down
                cv2.rectangle(self.temp, (self.buttonDownX, self.buttonDownY), (x, y), (0, 0, 255))

    def setFrame(self, frame):
        # Original frame
        self.frame = frame
        # Processing frame
        self.temp = frame
        self.frameSize = frame.shape[:2]

    def showFrame(self, windowSize):
        '''
        Show frame attach the mouse callback function, 
        `windowSize` is the window size which you want to resize.
        '''
        cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.windowName, windowSize)
        # Set the mouseCallBack function to the window
        cv2.setMouseCallback(self.windowName, self.mouse_callback)
        while True:                              
            cv2.imshow(self.windowName, self.temp)
            # if press the button "ESC" close the window
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyWindow(self.windowName)

    def getROIRegion(self):       
        '''
        Return the selected ROI region, each value represent to the 
        (leftUpX, leftUpY, rightDownX, rightDownY)
        '''
        # If the region is none, return the frame size region 
        if self.buttonDownX == -1 or self.buttonUpX == -1:
            return (0, 0, self.frame.shape[1], self.frame.shape[0])

        # To adjust leftUp value must less than rightDown value
        if self.buttonDownX > self.buttonUpX:
            temp = self.buttonDownX
            self.buttonDownX = self.buttonUpX
            self.buttonUpX = temp
        if self.buttonDownY > self.buttonUpY:
            temp = self.buttonDownY
            self.buttonDownY = self.buttonUpY
            self.buttonUpY = temp          

        return (self.buttonDownX, self.buttonDownY, self.buttonUpX, self.buttonUpY)

# Debug mode
if __name__ == "__main__": 
    def main():
        # Detect the webcam
        cap = cv2.VideoCapture(0)
        # If can't detect the webcam
        if cap.isOpened() == False:
            print("Can't detect the webcam")
            return -1

        ref, frame = cap.read()  
        
        winMC = winMouseControl("windowControl")
        winMC.setFrame(frame)
        
        winMC.showFrame((1280, 720))
        print(winMC.getROIRegion())

    main()