import cv2
import numpy as np

# ref: https://www.programcreek.com/python/example/89404/cv2.createBackgroundSubtractorMOG2
# ref: https://docs.opencv.org/3.4.1/d7/d7b/classcv_1_1BackgroundSubtractorMOG2.html#ab8bdfc9c318650aed53ecc836667b56a
class Mog2MotionDetector:
    def __init__(self, backGroundRatio = 0.8, threshRatio = 0.8):
        '''
        Mog class construction.
        The `backGroundRatio is the ratio to update the background object.
        The `threshRatio` is the threshold ratio to check if it is motion or not.
        '''
        #Init the color detector object
        self.fgbg = cv2.createBackgroundSubtractorMOG2()

        # calculate the threshold value
        self.threshValue = 255 * threshRatio

        # preprocess kernel init
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        self.connectivity = 8
        
        # it's considered background and added to the model as a center of a new component. It corresponds to TB parameter in the paper.
        self.fgbg.setBackgroundRatio(backGroundRatio)
    
    def mse(self, image, errThreshold = 2):
        '''
        The 'Mean Squared Error' between the two images is the
        sum of the squared difference between the two images;
        NOTE: the two images must have the same dimension.
        The `image` is the inputarray which it want to track motion.       
        The `errThreshold` is the ratio to mutilply the err value
        '''

        grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        fgmask = self.fgbg.apply(grayimg)

        # use opening phology process to refine the fgmask
        fgmask_open = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)       
        
        ret, thresh_img = cv2.threshold(fgmask, self.threshValue, 255, cv2.THRESH_BINARY)
        err = np.sum((thresh_img.astype("float")) ** errThreshold)
        err /= float(thresh_img.shape[0] * thresh_img.shape[1])
        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return thresh_img, round(err,0)

    def findForegroundObject(self, maskImage, minAreaThresh = 100, maxAreaRatioThresh = 0.5):
        '''
        Use the foreground mask to find the foreground object.
        `maskImage` is the foreground mask inputarray.
        `minAreaThresh` is the threshold value to avoid the noise.
        `maxAreaRatioThresh` is the ratio threshhold to avoid big noise.
        '''
        # ref: https://blog.csdn.net/weixin_34376562/article/details/86397975
        # ref: https://www.cnblogs.com/jsxyhelu/p/7439655.html
        forgroundObject = []
        
        # Only get the second index, it about the foreground object position and area
        foregroundInformation = cv2.connectedComponentsWithStats(maskImage, self.connectivity, cv2.CV_32S)[2]
        # Calculate the maxAreaThresh use the image area
        maxAreaThresh = maskImage.shape[0] * maskImage.shape[1] * maxAreaRatioThresh

        # Because the first index is the whole background information
        if foregroundInformation.shape[0] > 1:
            # delete the first cols object
            foregroundInformation = np.delete(foregroundInformation, [0], axis=0)

            while len(foregroundInformation)!= 0:                 
                # find the max bounding box index 
                max_idx, max_val = self.__explicit(foregroundInformation[:,-1])
                # The threshold value if the bounding box area less than minAreaThresh, remove the object
                if max_val <= minAreaThresh or max_val >= maxAreaThresh:
                    foregroundInformation = np.delete(foregroundInformation, [max_idx], axis = 0)
                    continue

                forgroundObject.append(foregroundInformation[max_idx])
                # Get the max bounding box
                maxInformation = foregroundInformation[max_idx]

                deleteIndex = []
                deleteIndex.append(max_idx)

                # find the bounding box which include the max bounding box
                for index,rect in enumerate(foregroundInformation[1:]): 
                    if (maxInformation[0] < rect[0] and maxInformation[1] < rect[1]):
                        if (maxInformation[0] + maxInformation[2] > rect[0] + rect[2] and maxInformation[1] + maxInformation[3] > rect[1] + rect[3]):
                            deleteIndex.append(index)

                foregroundInformation = np.delete(foregroundInformation, deleteIndex, axis=0)
                
        return forgroundObject

    def __explicit(self, l):
        '''
        Help method to find max value and index in the `l` list
        '''       
        max_idx = np.argmax(l)
        max_val = l[max_idx]
        return max_idx, max_val              
       

# Debug mode
if __name__ == "__main__":
    def main():
        # Detect the webcam
        cap = cv2.VideoCapture(0)
        # If can't detect the webcam
        if cap.isOpened() == False:
            print("Can't detect the webcam")
            return -1      
        
        Mog = Mog2MotionDetector(backGroundRatio = 0.5)
        cap.set(cv2.CAP_PROP_EXPOSURE, -4.0)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        
        while True:
            ref, frame = cap.read()  

            forgroundMaskImg, err = Mog.mse(frame)
            foregroundObject = Mog.findForegroundObject(forgroundMaskImg)
            

            for obj in foregroundObject:
                cv2.rectangle(frame, (obj[0], obj[1]), (obj[0] + obj[2], obj[1] + obj[3]), (0, 0, 255), 2)
            cv2.imshow("thresh", forgroundMaskImg)
            cv2.imshow("TestMog", frame)

            if cv2.waitKey(1) == 27:
                break
        
    main()
