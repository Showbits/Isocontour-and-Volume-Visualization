##Import VTK
from vtk import *

##Loading dataset using vtkXMLImageDataReader() and created a data object from readers output

reader = vtkXMLImageDataReader() 
reader.SetFileName('Data/Isabel_2D.vti') 
reader.Update() 
data = reader.GetOutput()
numCells = data.GetNumberOfCells()


C = int(input("Input Iso Value:"))  #taking iso value from user
dataArr = data.GetPointData().GetArray('Pressure')
points = vtkPoints() #created points object
polyLine = vtkPolyLine() #created polyline object
polyData = vtkPolyData() #created polydata object
cells = vtkCellArray()  #created cell array
count = 0
#iterating loop for each cell 

for i in range(numCells):  
    cell = data.GetCell(i)  #cell Index from 0 to numcells
    #getting the 4 corner points of the cell
    pid1 = cell.GetPointId(0)
    pid2 = cell.GetPointId(1)
    pid3 = cell.GetPointId(3)
    pid4 = cell.GetPointId(2)
    #getting the 3D coordinates of the points
    p1 = data.GetPoint(pid1)
    p2 = data.GetPoint(pid2)
    p3 = data.GetPoint(pid3)
    p4 = data.GetPoint(pid4)
     #getting the pressure value at each points
    v1 = dataArr.GetTuple1(pid1)
    v2 = dataArr.GetTuple1(pid2)
    v3 = dataArr.GetTuple1(pid3)
    v4 = dataArr.GetTuple1(pid4)

    #getting the isopoints for each cells
    if((v1 < C and v2 > C) or (v1 > C and v2 < C)):
        iso_pointX = (v1 - C)/(v1 - v2) * (p2[0] - p1[0]) + p1[0]
        iso_pointY = (v1 - C)/(v1 - v2) * (p2[1] - p1[1]) + p1[1]
        iso_pointZ = (v1 - C)/(v1 - v2) * (p2[2] - p1[2]) + p1[2]
        points.InsertNextPoint([iso_pointX, iso_pointY, iso_pointZ])
        count = count + 1
    if((v2 < C and v3 > C) or (v2 > C and v3 < C)):

        iso_pointX = (v2 - C)/(v2 - v3) * (p3[0] - p2[0]) + p2[0]
        iso_pointY = (v2 - C)/(v2 - v3) * (p3[1] - p2[1]) + p2[1]
        iso_pointZ = (v2 - C)/(v2 - v3) * (p3[2] - p2[2]) + p2[2]
        points.InsertNextPoint([iso_pointX, iso_pointY, iso_pointZ])
        count = count + 1
    if((v3 < C and v4 > C) or (v3 > C and v4 < C)):

        iso_pointX = (v3 - C)/(v3 - v4) * (p4[0] - p3[0]) + p3[0]
        iso_pointY = (v3 - C)/(v3 - v4) * (p4[1] - p3[1]) + p3[1]
        iso_pointZ = (v3 - C)/(v3 - v4) * (p4[2] - p3[2]) + p3[2]
        points.InsertNextPoint([iso_pointX, iso_pointY, iso_pointZ])
        count = count + 1
    if((v4 < C and v1 > C) or (v4 > C and v1 < C)):

        iso_pointX = (v4 - C)/(v4 - v1) * (p1[0] - p4[0]) + p4[0]
        iso_pointY = (v4 - C)/(v4 - v1) * (p1[1] - p4[1]) + p4[1]
        iso_pointZ = (v4 - C)/(v4 - v1) * (p1[2] - p4[2]) + p4[2]
        points.InsertNextPoint([iso_pointX, iso_pointY, iso_pointZ])
        count = count + 1;

j = 0
while(j < count):
    #created ids of two points which is there in polyline
    polyLine.GetPointIds().SetNumberOfIds(2) 
    polyLine.GetPointIds().SetId(0, j)
    polyLine.GetPointIds().SetId(1, j + 1)
    #inserting the cell in the cells array
    cells.InsertNextCell(polyLine)
    j += 2

polyData.SetPoints(points)  #inserting points in polydata
polyData.SetLines(cells)    #inserting cells in polydata

# Storing the polydata into a vtkpolydata file with extension .vtp
writer = vtkXMLPolyDataWriter()
writer.SetInputData(polyData)
writer.SetFileName('output.vtp')
writer.Write()
