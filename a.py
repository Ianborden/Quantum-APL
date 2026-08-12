# import qiskit_metal as metal
# metal.view(design)
# #gui = metal.MetalGUI(design)

import sys
from PySide6.QtWidgets import QApplication

import qiskit_metal as qm

# 1. ALWAYS initialize your Metal design and GUI first
design = qm.designs.DesignPlanar()

design.overwrite_enabled = True
design.chips.main.size.size_x = '6.25mm'
design.chips.main.size.size_y = '6.25mm'
design.chips.main.size.size_z = '-270um'
design.chips.main.size.sample_holder_top = '50um'
design.chips.main.size.sample_holder_bottom = '800um'

gui = qm.MetalGUI(design)


from qiskit_metal.qlibrary.terminations.launchpad_wb_driven import LaunchpadWirebondDriven

port_1  = LaunchpadWirebondDriven(design, 'port_1', options = dict(pos_x = '-2.496mm',
                                                                   pos_y = '-0mm',
                                                                   orientation = '0',
                                                                   pad_width = '350um',
                                                                   pad_height = '129 um',
                                                                   pad_gap = '150um',
                                                                   trace_width = '10um',
                                                                   trace_gap = '6um',
                                                                   lead_length = '9um',
                                                                   taper_height = '350um'))


port_2  = LaunchpadWirebondDriven(design, 'port_2', options = dict(pos_x = '2.496mm',
                                                                   pos_y = '-0mm',
                                                                   orientation = '180',
                                                                   pad_width = '350um',
                                                                   pad_height = '129 um',
                                                                   pad_gap = '150um',
                                                                   trace_width = '10um',
                                                                   trace_gap = '6um',
                                                                   lead_length = '9um',
                                                                   taper_height = '350um'))


from qiskit_metal.qlibrary.tlines.straight_path import RouteStraight

bus_1 = RouteStraight(design,
                      'bus_1',
                      options= dict(hfss_wire_bonds = True,
                                    pin_inputs = dict(start_pin = dict(component = 'port_1', pin = 'tie'),
                                                      end_pin = dict(component = 'port_2', pin = 'tie')),
                                    trace_width = '10um',
                                    trace_gap = '6um'))

from qiskit_metal.qlibrary.couplers.coupled_line_tee import CoupledLineTee

coupl_1 = CoupledLineTee(design, 'coupl_1', options= dict(pos_x = '-0.55mm',
                                                          pos_y = '0',
                                                          orientation = '180',
                                                          coupling_length = '650um',
                                                          down_length = '100um',
                                                          fillet = '50um',
                                                          coupling_space = '4um',
                                                          open_termination = True))


from qiskit_metal.analyses.em.cpw_calculations import guided_wavelength
def find_resonator_length(frequency, line_width, line_gap, N):
    [lambdaG, etfSart, q] = guided_wavelength(frequency, line_width,
                                              line_gap, substrate_thickness=350*10**-6,film_thickness = 200*10**-9)
    return str(lambdaG/N*10**3)+" mm"


gui.rebuild()
gui.autoscale()

gui.qApp.setActiveWindow(gui.main_window)
gui.main_window.show()
gui.main_window.raise_()
gui.main_window.activateWindow()


app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)
sys.exit(app.exec())


