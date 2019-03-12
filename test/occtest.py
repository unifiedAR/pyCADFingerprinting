
from OCC.Visual3d import *
from OCC.Quantity import *
from OCC.Aspect import *
from OCC.Graphic3d import *
from OCC.Display.SimpleGui import *

from OCC.STEPControl import STEPControl_Reader
step_reader = STEPControl_Reader()
#step_reader.ReadFile('models/cylinder_block.stp')
step_reader.ReadFile('models/NonSymTest/NonSymTest.step')
step_reader.TransferRoot()
block_cylinder_shape = step_reader.Shape()

from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()


display.DisplayShape(block_cylinder_shape, update=True, color="BLACK")
display.View.SetBackgroundColor(Quantity_NOC_BLACK)
display.SetBackgroundImage("background.jpg", stretch = True)
display.Repaint()