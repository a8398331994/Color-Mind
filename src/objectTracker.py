import cv2
import numpy as np

class objectTracker:
    def __init__(self, maxStatementStorege = 10):
        # Time record
        self.time = 0
        # object statement list
        self.objectStatementList = []
        # max object statement storege
        self.maxObjectstatementListStorege = maxStatementStorege

    def updateStatement(self, objectBoundingBox):
        # if object statement list size equal to zero
        if len(self.objectStatementList) == 0:
            pass

        # if object statement list size reach to max storege
        elif len(self.objectStatementList) == self.maxObjectstatementListStorege:
            pass
        
    def __addInformation(self, objectBoundingBox):
        
        # objectInformation = {"ID" : 0, "centerPosition" : (objectBoundingBox[0] + objectBoundingBox[2], )}
        


        self.time = self.time + 1
        print(self.time)