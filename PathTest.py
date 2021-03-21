import json
import multiprocessing as mp
import sys
import os
import time
# IMPORT HEADER FILES
import FindPath
from Draw import DrawPath

# log = open('log.txt', 'w')
# sys.stdout = log

NameNodes = FindPath.LoadData.NameAndNodes()

MatIn = FindPath.LoadData.NodesAndDistance()

nac = FindPath.LoadData.NodesAndCoord()

def MakeCache(N1, N2):
    if N1 != N2:
        flag = False
        try:
            MakeMap = FindPath.MakePath(N1, N2, MatIn, nac)
            Path, Distance = MakeMap.main()
            flag = True
        except:
            print(f'Fail finding path at {N1} to {N2}')

        if flag == True:
            JsonPath = []

            for node in Path:
                JsonPath.append(int(node))

            with open(f'cache/{N1}_{N2}.json', 'w') as FileOut:
                json.dump(JsonPath, FileOut)
                FileOut.close()

        # except:
        #     print(f'Fail at {Node_1} to {Node_2}')

def SaveTraceMat(N1):
    TraceFlag = False
    N2 = nac['Node'][0]
    JsonSave = []
    while TraceFlag == False:
        if N2 == N1:
            N2 += 1
        try:
            MakeMap = FindPath.MakeTraceMatrix(N1, N2, MatIn, nac)
            TraceMat = MakeMap.main()
            TraceFlag = True
        except:
            TraceFlag = False
    if TraceFlag == True:
        for i in TraceMat:
            JsonSave.append(i)
        with open (f'cache/Trace_{N1}.json', 'w') as FileIn:
            json.dump(JsonSave, FileIn)
            FileIn.close()



# mpcount = 0
# for i in range(len(nac['Node'])):
#     Node_1 = int(nac['Node'][i])
#     mp1 = mp.Process(target = SaveTraceMat, args = [Node_1])
#     mpcount += 1
#     if mpcount <= 7:
#         mp1.start()
#     else:
#         mp1.start()
#         mp1.join()
#         mpcount = 0

# log.close()

StartPlace = input("Type in start place: ")
EndPlace = input("Type in destination: ")

StartTime = time.time()

FinalPath = []

Ind = FindPath.GetIndex(NameNodes['Name'], StartPlace)
StartPoint = int(NameNodes['Node'][Ind]) - 1
Ind = FindPath.GetIndex(NameNodes['Name'], EndPlace)
EndPoint = int(NameNodes['Node'][Ind]) - 1

CacheName = 'cache'
TraceName = f'Trace_{StartPoint}.json'

# if TraceName in os.listdir(CacheName):
#     FileIn = open(f'{CacheName}/{TraceName}', 'r')
#     JsonPath = json.load(FileIn)

#     PathValue = JsonPath[EndPoint]

#     while(PathValue != -1):
#         FinalPath.append(PathValue)
#         PathValue = JsonPath[PathValue]

#     Color = (30,45,160)

#     DrawPath(FinalPath, Color, nac).SaveImage()

# else:

#     FindPath.MakePath(StartPoint, EndPoint, MatIn, nac).main()

Co = (0,100,255)
FindPath.MakePath(StartPoint, EndPoint, MatIn, nac, Co).main()

print(f'Total time: {time.time() - StartTime} seconds')
