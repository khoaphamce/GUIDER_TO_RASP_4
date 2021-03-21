from queue import PriorityQueue
import pandas as pd
from math import sqrt
import cv2
import time
import json
import numpy as np

class Data:
    def __init__(self, NameAndNodes, NodesAndCoord, NodesAndDistance):
        self.NameAndNodes = NameAndNodes
        self.NodesAndCoord = NodesAndCoord
        self.NodesAndDistance = NodesAndDistance

    def NameNodes(self):
        ReturnValue = pd.read_csv(self.NameAndNodes)
        return ReturnValue
          
    def NodesCoord(self):
        ReturnValue = pd.read_csv(self.NodesAndCoord)
        return ReturnValue

    def NodesDistance(self):
        ReturnValue = pd.read_csv(self.NodesAndDistance)
        return ReturnValue

    def NodeToCoord(self, Node):
        CoordData = self.NodesCoord()
        CoordX = CoordData['X'][Node]
        CoordY = CoordData['Y'][Node]
        Coord = (CoordX, CoordY)
        return Coord

    def GetIndex(self, Arr, Value):
        for i in range(len(Arr)):
            if Value == Arr[i]:
                return i
        return -1

    def NameToNode(self, Name):
        NodeData = self.NameNodes()
        Ind = self.GetIndex(NodeData['Name'], Name)
        return int(NodeData['Node'][Ind])-1


class Algorithm:
    def __init__ (self, StartNode, EndNode, Graph, NodesAndCoord):
        self.StartNode = StartNode
        self.EndNode = EndNode
        self.Graph = Graph
        self.NodesAndCoord = NodesAndCoord


    def Euclidean(self, P1, P2):
        X1 = int(self.NodesAndCoord['X'][P1])
        Y1 = int(self.NodesAndCoord['Y'][P1])
        X2 = int(self.NodesAndCoord['X'][P2])
        Y2 = int(self.NodesAndCoord['Y'][P2])

        return sqrt((X1-X2)*(X1-X2) + (Y1-Y2)*(Y1-Y2))


    def AStar(self):
        # StartTimeLoop = time.time()
        NodeDistance = []
        NodeDistanceTemp = []
        PriCount = 0
        OpenSet = PriorityQueue()
        OpenSet.put((0, PriCount, self.StartNode))
        CameFrom = {}
        GDist = {}
        FDist = {}
        Path = []

        for Node_1 in self.NodesAndCoord['Node']:
            GDist[int(Node_1)] = float('inf')
            FDist[int(Node_1)] = float('inf')
            for Node_2 in self.NodesAndCoord['Node']:
                NodeDistanceTemp.append(0)
            NodeDistance.append(NodeDistanceTemp)
            NodeDistanceTemp = []

        GDist[self.StartNode] = 0
        FDist[self.StartNode] = self.Euclidean(self.StartNode, self.EndNode)

        for i in range(len(self.Graph['Distance'])):
            Node_1 = self.Graph['Node_1'][i]
            Node_2 = self.Graph['Node_2'][i]
            GraphDist = self.Graph['Distance'][i]
            if Node_1 != Node_2:
                NodeDistance[int(Node_1)][int(Node_2)] = GraphDist
                NodeDistance[int(Node_2)][int(Node_1)] = GraphDist

        OpenSetHash = {self.StartNode}

        while not OpenSet.empty() > 0:
            Current = OpenSet.get()[2]
            OpenSetHash.remove(Current)

            if Current == self.EndNode:
                # JsonSaveFile = open(f'cache/{self.StartNode}_{self.EndNode}.json', 'w')
                print('found path')
                # print(f'{self.EndNode+1} > ', end = '')
                Path.append(self.EndNode)
                Current = CameFrom[Current]
                Path.append(Current)
                # print(f'{Current+1} > ', end = '')
                while Current in CameFrom:
                    Current = CameFrom[Current]
                    Path.append(Current)
                    # print(f'{Current+1} > ', end = '')

                # json.dump(Path, JsonSaveFile)
                # JsonSaveFile.close()
                # print(f'Time find: {time.time() - StartTimeLoop} seconds')
                # print('')
                return Path

            for Neighbor in range(len(NodeDistance[Current])):
                Distance = NodeDistance[Current][Neighbor]
                if Distance > 0:

                    TempG = GDist[Current] + Distance
                    
                    if TempG < GDist[Neighbor]:
                        GDist[Neighbor] = TempG
                        FDist[Neighbor] = TempG + self.Euclidean(Neighbor, self.EndNode)
                        
                        CameFrom[Neighbor] = Current
                        if Neighbor not in OpenSetHash:
                            PriCount += 1
                            OpenSet.put((FDist[Neighbor], PriCount, Neighbor))
                            OpenSetHash.add(Neighbor)

        # JsonSaveFile = open(f'cache/{self.StartNode}_{self.EndNode}_Fail.json', 'w')
        # print(f'Time to find path: {time.time() - StartTimeLoop} seconds')
        # print('')

        return False   


class Draw:
    def __init__ (self, Image, NodeList, Color, MarkOption, MarkColor):
        self.Image = Image
        self.Color = Color
        self.NodeList = NodeList

        self.PathOnlyColor = [0,0,0,0]

        for i in range(3):
            self.PathOnlyColor[i] = Color[i]
        self.PathOnlyColor[3] = 255

        self.PathMarkerColor = [0,0,0,0]

        for i in range(3):
            self.PathMarkerColor[i] = MarkColor[i]
        self.PathMarkerColor[3] = 255

        if MarkOption:
            self.MarkOption = MarkOption
        else:
            self.MarkOption = False
        if MarkColor:
            self.MarkColor = MarkColor
        else:
            self.MarkColor = (0,0,0)

    def Path(self):
        ReturnImage = self.Image
        Thickness = int(0.005*sqrt(ReturnImage.shape[0]*ReturnImage.shape[0] + ReturnImage.shape[1]*ReturnImage.shape[1]))
        # Thickness = 200\
        Blank = (255, 255, 255, 0)
        PathOnly = np.full((ReturnImage.shape[0], ReturnImage.shape[1], 4), Blank, np.uint8)

        for i in range(len(self.NodeList)-1):
            P1 = (self.NodeList[i][1], self.NodeList[i][0])
            P2 = (self.NodeList[i+1][1], self.NodeList[i+1][0])
            ReturnImage = cv2.line(ReturnImage, P1, P2, self.PathOnlyColor, Thickness)
            PathOnly = cv2.line(PathOnly, P1, P2, self.PathOnlyColor, Thickness)

        if self.MarkOption == True:
            P1 = (self.NodeList[0][1], self.NodeList[0][0])
            Radius = int(round(Thickness*0.5, 0))
            MarkThickness = int(round(Radius*1.8, 0))
            ReturnImage = cv2.circle(ReturnImage, P1, Radius, self.MarkColor, MarkThickness)
            ReturnImage = cv2.circle(ReturnImage, P2, Radius, self.MarkColor, MarkThickness)
            PathOnly = cv2.circle(PathOnly, P1, Radius, self.PathMarkerColor, MarkThickness)
            PathOnly = cv2.circle(PathOnly, P2, Radius, self.PathMarkerColor, MarkThickness)

        return ReturnImage, PathOnly

#------------- TEST AREA ---------------

