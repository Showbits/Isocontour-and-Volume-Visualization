##Import VTK
from vtk import *

##Loading dataset using vtkXMLImageDataReader() and created a data object from readers output

reader = vtkXMLImageDataReader() 
reader.SetFileName('Data/Isabel_3D.vti') 
reader.Update() 
data = reader.GetOutput()

#created instances of vtkColorTransferFunction and vtkPiecewiseFunction
color = vtkColorTransferFunction()
opacity = vtkPiecewiseFunction()

#setting up the values for color Transfer Function
color.AddRGBPoint(-4931.54, 0, 1, 1)
color.AddRGBPoint(-2508.95, 0, 0, 1)
color.AddRGBPoint(-1873.9, 0, 0, 0.5)
color.AddRGBPoint(-1027.16, 1, 0, 0)
color.AddRGBPoint(-298.031, 1, 0.4, 0)
color.AddRGBPoint(2594.97, 1, 1, 0)

#setting up the values for Opacity Transfer Function
opacity.AddPoint(-4931.54, 1.0)
opacity.AddPoint(101.815, 0.002)
opacity.AddPoint(2594.97, 0.0)


#created vtkSmartVolumeMapper object to perform volume rendering
volumeMapper = vtkSmartVolumeMapper()
volumeMapper.SetInputData(data)
properties = vtkVolumeProperty()
properties.SetColor(color)
properties.SetScalarOpacity(opacity)

#created vtkOutlineFilter object to add an outline to the volume rendered data
outline_filter = vtkOutlineFilter()
outline_filter.SetInputData(data)
outline_filter.Update()

#taking input from the user if the user want phong shading or not
input_phong = input("Enter y or n:")
if(input_phong == 'y'):
    properties.ShadeOn()
    properties.SetAmbient(0.5)
    properties.SetDiffuse(0.5)
    properties.SetSpecular(0.5)

#created vtkVolume object
volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(properties)

#created vtkPolyDataMapper object
polydata_mapper= vtkPolyDataMapper()
polydata_mapper.SetInputConnection(outline_filter.GetOutputPort())
actor = vtkActor() #created acter and give the polydata_mapper to it
actor.SetMapper(polydata_mapper)
renderer = vtkRenderer() #created renderer and give the actor and volume to it
renderer.AddActor(actor)
renderer.AddActor(volume)
renderer.SetBackground(1.0, 1.0, 1.0)
rwindow = vtkRenderWindow() #Created a renderwindow and attach it with the renderer and interactor
rwindow.SetSize(1000, 1000) #created 1000 x 1000 sized render window to show the rendering result
rwindow.AddRenderer(renderer)



##Created render_windowInteractor and setting up the renderWindow to interactor
render_windowInteractor = vtkRenderWindowInteractor() 
render_windowInteractor.SetRenderWindow(rwindow) 


##render the object
rwindow.Render()
render_windowInteractor.Start()
