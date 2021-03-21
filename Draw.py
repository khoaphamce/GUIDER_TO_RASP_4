import cv2
from math import sqrt

class DrawPath():
    def __init__(self, PathList, Color, NodesCoord):
        self.PathList = PathList
        self.Color = Color
        self.NodesCoord = NodesCoord

    def SaveImage(self):
        ToDrawMap = cv2.imread('ToDrawMap/ToDrawMap.jpg')
        Thickness = int(0.005*sqrt(ToDrawMap.shape[0]*ToDrawMap.shape[0] + ToDrawMap.shape[1]*ToDrawMap.shape[1]))

        PathLength = len(self.PathList)

        i = PathLength-1

        P2 = (self.NodesCoord['Y'][self.PathList[i]], self.NodesCoord['X'][self.PathList[i]])
        
        while (i >= 0):
            P1 = (self.NodesCoord['Y'][self.PathList[i]], self.NodesCoord['X'][self.PathList[i]])
            
            ToDrawMap = cv2.line(ToDrawMap, P1, P2, self.Color, Thickness)
            
            print(self.PathList[i]+1, '> ', end = '')

            i = i-1
            P2 = P1

        print(PathLength + 1)
        P1 = (self.NodesCoord['Y'][PathLength], self.NodesCoord['X'][PathLength])
        ToDrawMap = cv2.line(ToDrawMap, P1, P2, self.Color, Thickness)

        cv2.imwrite('path.jpg', ToDrawMap)