from cc3d.cpp.PlayerPython import * 
from cc3d import CompuCellSetup
from cc3d.core.PySteppables import *

class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)
        self.track_cell_level_scalar_attribute(field_name='Pressure', attribute_name='PressureDict')
        self.track_cell_level_scalar_attribute(field_name='SurfTen', attribute_name='TensionDict')
        
           
    def start(self):
        x = self.dim.x//2
        y = self.dim.y//2
        size = 8
        cell = self.new_cell(self.CELL)
        # size of cell will be SIZExSIZEx1
        self.cell_field[x-size//2:x + size//2 - 1, y-size//2:y + size//2 - 1, 0] = cell
        
        cell.lambdaVolume = 3.0
        cell.targetVolume = 30.0
        cell.lambdaSurface = 4.0
        cell.targetSurface = 40.0
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)
    
    def start(self):
        self.plot_win = self.add_new_plot_window(title='Pressure, Volume, Surface Tension vs. Time',
                                         x_axis_title='MonteCarlo Step (MCS)',
                                         y_axis_title='Variables', x_scale_type='linear', y_scale_type='linear',
                                         grid=False)                                                                                                        
    
        self.plot_win.add_plot("MVol", style='Lines', color='red', size=3)
        self.plot_win.add_plot("MSur", style='Lines', color='green', size=3)
        self.plot_win.add_plot("Pressure", style='Lines', color='cyan', size=3)
       
        # # arguments are (name of the data series, x, y)
        # self.plot_win.add_data_point("MVol", mcs, cell.volume)
        # self.plot_win.add_data_point("MSur", mcs, cell.surface)
        
        self.msg_win = self.add_new_message_window(title='Message')
        
        # initialize setting for Histogram
        # self.plot_winHist = self.add_new_plot_window(title='Histogram of Cell Pressures', x_axis_title='Number of Cells',
                                                 # y_axis_title='Pressure')
        # _alpha is transparency 0 is transparent, 255 is opaque
        # self.plot_winHist.add_histogram_plot(plot_name='Hist 1', color='green', alpha=100)
        
        
        
    def step(self, mcs):
        pressure_list=[]
        targetpress = 3
        for cell in self.cell_list:
            if mcs%500==0:
                cell.targetVolume += 25
                pressure_list.append(-cell.pressure)
                # self.plot_winHist.add_histogram(plot_name='Hist 1', value_array=pressure_list, number_of_bins=10)
            # if cell.pressure>targetpress:
                # cell.targetSurface-=5
            # if cell.pressure<targetpress:
                # cell.targetSurface+=5
        # arguments are (name of the data series, x, y)
        self.plot_win.add_data_point("MVol", mcs, cell.volume)
        self.plot_win.add_data_point("MSur", mcs, cell.surfaceTension)
        self.plot_win.add_data_point("Pressure", mcs, cell.pressure) 
        cell.dict['PressureDict']=-cell.pressure
        cell.dict['TensionDict']=-cell.surfaceTension
        self.msg_win.print('step=',mcs,'pressure=',cell.pressure,style=BOLD,color='blue')

        
        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        # field = self.field.CHEMICAL_FIELD_NAME
        
        # for cell in self.cell_list:
            # concentrationAtCOM = field[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]

            # # you can use here any fcn of concentrationAtCOM
            # cell.targetVolume += 0.01 * concentrationAtCOM       

        
# class MitosisSteppable(MitosisSteppableBase):
    # def __init__(self,frequency=1):
        # MitosisSteppableBase.__init__(self,frequency)

    # def step(self, mcs):

        # cells_to_divide=[]
        # for cell in self.cell_list:
            # if cell.volume>50:
                # cells_to_divide.append(cell)

        # for cell in cells_to_divide:

            # self.divide_cell_random_orientation(cell)
            # # Other valid options
            # # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # # self.divide_cell_along_major_axis(cell)
            # # self.divide_cell_along_minor_axis(cell)
        
    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        if self.parent_cell.type==1:
            self.child_cell.type=2
        else:
            self.child_cell.type=1

        