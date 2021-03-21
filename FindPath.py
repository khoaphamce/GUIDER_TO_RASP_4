import pandas as pd
import cv2
import time
import math

class MakePath:

    def __init__(self, StartPoint, EndPoint, MatrixInput, NodesCoord, Color):
        self.StartPoint = StartPoint
        self.EndPoint = EndPoint
        self.MatrixInput = MatrixInput
        self.NodesCoord = NodesCoord
        self.Color = Color

    #-----------------FIND PATH----------------

    def Setup(self):
        self.MinNode = 0
        self.MaxNode = len(self.NodesCoord['Node'])

        self.MatInCols = len(self.MatrixInput)

        self.NodeDistance = []
        self.NodeDistanceTemp = []
        self.TotalDistance = []
        self.NodePassed = []
        self.Queue = []
        self.PathNode = []
    
        # SET UP
        for i in range (0, self.MaxNode + 1):
            self.TotalDistance.append(float('inf')) # SET TOTAL DISTANCE TO EACH NODES INFINITY 
            self.NodeDistanceTemp = []
            self.NodePassed.append(-1)                 #
            for j in range (0, self.MaxNode + 1):      # SET DISTANCE BETWEEN ALL NODES AS 0 
                self.NodeDistanceTemp.append(0)        #
            self.NodeDistance.append(self.NodeDistanceTemp) #
        self.TotalDistance[self.StartPoint] = 0

        for i in range (0, self.MatInCols):
            Node1 = self.MatrixInput[i][0]
            Node2 = self.MatrixInput[i][1]
            if Node1 != Node2:
                DistanceBetween = self.MatrixInput[i][2]
                self.NodeDistance[Node1][Node2] = DistanceBetween
                self.NodeDistance[Node2][Node1] = DistanceBetween

        for i in range (self.MinNode, self.MaxNode + 1):
            self.Queue.append(i)
            for j in range(self.MinNode, self.MaxNode + 1):
                if self.NodeDistance[i][j] > 0:
                    self.Queue.append(j)


    #-------- FIND SHORTEST PATH BY DIJKSTRA -----------

    def FindPath(self):
        while(len(self.Queue) > 0):
            min = float('inf') + 1
            CurrentQueueValue = self.Queue[0]

            for Node in self.Queue:
                if (min > self.TotalDistance[Node]):
                    CurrentQueueValue = Node
                    min = self.TotalDistance[Node]
            
            self.Queue.remove(CurrentQueueValue)

            for Node in range(0, len(self.NodeDistance[CurrentQueueValue])):
                if (self.NodeDistance[CurrentQueueValue][Node] > 0):
                    CheckDistance = self.TotalDistance[CurrentQueueValue] + self.NodeDistance[CurrentQueueValue][Node]
                    if (self.TotalDistance[Node] > CheckDistance):
                        self.TotalDistance[Node] = CheckDistance
                        self.NodePassed[Node] = (CurrentQueueValue)

        PathValue = self.NodePassed[self.EndPoint]
        print(self.NodePassed)

        while(PathValue != -1):
            self.PathNode.append(PathValue)
            PathValue = self.NodePassed[PathValue]

        return self.PathNode, self.TotalDistance[self.EndPoint]

    #------------ DRAW PATH ---------------

    def DrawPath(self):
        ToDrawMap = cv2.imread('ToDrawMap/ToDrawMap.jpg')
        Thickness = int(0.005*math.sqrt(ToDrawMap.shape[0]*ToDrawMap.shape[0] + ToDrawMap.shape[1]*ToDrawMap.shape[1]))
        i = len(self.Path)-1
        P2 = (self.NodesCoord['Y'][self.Path[i]], self.NodesCoord['X'][self.Path[i]])
        while (i >= 0):
            P1 = (self.NodesCoord['Y'][self.Path[i]], self.NodesCoord['X'][self.Path[i]])
            
            ToDrawMap = cv2.line(ToDrawMap, P1, P2, self.Color, Thickness)
            
            print(self.Path[i]+1, '> ', end = '')

            i = i-1
            P2 = P1

        print(self.EndPoint+1)
        P1 = (self.NodesCoord['Y'][self.EndPoint], self.NodesCoord['X'][self.EndPoint])
        ToDrawMap = cv2.line(ToDrawMap, P1, P2, self.Color, Thickness)

        cv2.imwrite('path.jpg', ToDrawMap)

    #------------- MAIN ------------

    def main(self):

        self.Setup()

        self.Path, self.Distance = self.FindPath()

        print('Shortest path to go: ', end = '')
        
        print('Total Distance: ', self.Distance)
        
        self.DrawPath()

        return self.Path, self.Distance

#---------------------------LOADING CLASS------------------------------------------------

class LoadData:
    #-------------- LOAD NAME AND NODES -----------------
    
    def NameAndNodes():
        return pd.read_csv('NameAndNodes.csv')

    #-------------- LOAD NODES AND COORD ----------------

    def NodesAndCoord():
        NodesCoord = pd.read_csv('NodesAndCoord.csv')
        return NodesCoord

    #-------------- LOAD NODES AND DISTANCE -------------

    def NodesAndDistance():
        MatrixInput = []
        temp_mat = []

        Data = pd.read_csv('NodesAndDistance.csv')

        for i in range(len(Data['Node_1'])):
            N_1 = Data['Node_1'][i]
            N_2 = Data['Node_2'][i]
            D = Data['Distance'][i]
            temp_mat.append(N_1)
            temp_mat.append(N_2)
            temp_mat.append(D)
            MatrixInput.append(temp_mat)
            temp_mat = []
        return MatrixInput

#---------------------------TRACING CLASS------------------------------------------------

class MakeTraceMatrix:

    def __init__(self, StartPoint, EndPoint, MatrixInput, NodesCoord):
        self.StartPoint = StartPoint
        self.EndPoint = EndPoint
        self.MatrixInput = MatrixInput
        self.NodesCoord = NodesCoord

    #-----------------FIND PATH----------------

    def Setup(self):
        self.MinNode = 0
        self.MaxNode = len(self.NodesCoord['Node'])

        self.MatInCols = len(self.MatrixInput)

        self.NodeDistance = []
        self.NodeDistanceTemp = []
        self.TotalDistance = []
        self.NodePassed = []
        self.Queue = []
        self.PathNode = []

        # SET UP
        for i in range (0, self.MaxNode + 1):
            self.TotalDistance.append(float('inf')) # SET TOTAL DISTANCE TO EACH NODES INFINITY 
            self.NodeDistanceTemp = []
            self.NodePassed.append(-1)                 #
            for j in range (0, self.MaxNode + 1):      # SET DISTANCE BETWEEN ALL NODES AS 0 
                self.NodeDistanceTemp.append(0)        #
            self.NodeDistance.append(self.NodeDistanceTemp) #
        self.TotalDistance[self.StartPoint] = 0

        for i in range (0, self.MatInCols):
            Node1 = self.MatrixInput[i][0]
            Node2 = self.MatrixInput[i][1]
            if Node1 != Node2:
                DistanceBetween = self.MatrixInput[i][2]
                self.NodeDistance[Node1][Node2] = DistanceBetween
                self.NodeDistance[Node2][Node1] = DistanceBetween

        for i in range (self.MinNode, self.MaxNode + 1):
            self.Queue.append(i)
            for j in range(self.MinNode, self.MaxNode + 1):
                if self.NodeDistance[i][j] > 0:
                    self.Queue.append(j)


    #-------- FIND SHORTEST PATH BY DIJKSTRA -----------

    def FindPath(self):
        while(len(self.Queue) > 0):
            min = float('inf') + 1
            CurrentQueueValue = self.Queue[0]

            for Node in self.Queue:
                if (min > self.TotalDistance[Node]):
                    CurrentQueueValue = Node
                    min = self.TotalDistance[Node]
            
            self.Queue.remove(CurrentQueueValue)

            for Node in range(0, len(self.NodeDistance[CurrentQueueValue])):
                if (self.NodeDistance[CurrentQueueValue][Node] > 0):
                    CheckDistance = self.TotalDistance[CurrentQueueValue] + self.NodeDistance[CurrentQueueValue][Node]
                    if (self.TotalDistance[Node] > CheckDistance):
                        self.TotalDistance[Node] = CheckDistance
                        self.NodePassed[Node] = (CurrentQueueValue)

        # PathValue = self.NodePassed[self.EndPoint]
        
        return self.NodePassed

    #------------- MAIN ------------

    def main(self):
        
        StartTime = time.time()

        self.Setup()

        self.Path = self.FindPath()
        
        print(f'Total time: {time.time() - StartTime} seconds')
        
        return self.Path



def GetIndex(Arr, Val):
    Ind = 0
    flag = False
    i = 0
    while(flag == False) and (i < len(Arr)):
        if Arr[i] == Val:
            Ind = i
            flag = True
        i += 1
    return Ind

