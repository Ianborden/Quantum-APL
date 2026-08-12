
from qiskit_metal.qlibrary.couplers.coupled_line_tee import CoupledLineTee

from qiskit_metal.qlibrary.terminations.launchpad_wb_driven import LaunchpadWirebondDriven

from qiskit_metal.qlibrary.tlines.straight_path import RouteStraight

from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket

from qiskit_metal.qlibrary.tlines.meandered import RouteMeander

from qiskit_metal.qlibrary.terminations.open_to_ground import OpenToGround

import qiskit_metal
from qiskit_metal import designs, MetalGUI

design = designs.DesignPlanar()

gui = MetalGUI(design)


port_1 = LaunchpadWirebondDriven(
design,
name='port_1',
options={'lead_length': '9um',
 'orientation': '0',
 'pad_gap': '150um',
 'pad_height': '129 um',
 'pad_width': '350um',
 'pos_x': '-2.496mm',
 'pos_y': '-0mm',
 'taper_height': '350um',
 'trace_gap': '6um',
 'trace_width': '10um'},

component_template=None,
)




port_2 = LaunchpadWirebondDriven(
design,
name='port_2',
options={'lead_length': '9um',
 'orientation': '180',
 'pad_gap': '150um',
 'pad_height': '129 um',
 'pad_width': '350um',
 'pos_x': '2.496mm',
 'pos_y': '-0mm',
 'taper_height': '350um',
 'trace_gap': '6um',
 'trace_width': '10um'},

component_template=None,
)




bus_1 = RouteStraight(
design,
name='bus_1',
options={'_actual_length': '4.974 mm',
 'hfss_wire_bonds': True,
 'pin_inputs': {'end_pin': {'component': 'port_2',
                            'pin': 'tie'},
                'start_pin': {'component': 'port_1',
                              'pin': 'tie'}},
 'trace_gap': '6um',
 'trace_width': '10um'},

type='CPW',
)




coupl_1 = CoupledLineTee(
design,
name='coupl_1',
options={'coupling_length': '650um',
 'coupling_space': '4um',
 'fillet': '50um',
 'orientation': '180',
 'pos_x': '-0.55mm',
 'pos_y': '0'},

component_template=None,
)




open_end = OpenToGround(
design,
name='open_end',
options={'orientation': '90',
 'pos_x': '-0.55mm',
 'pos_y': '2.25mm'},

component_template=None,
)




res_1 = RouteMeander(
design,
name='res_1',
options={'_actual_length': '11.999999999999996 '
                   'mm',
 'fillet': '50um',
 'hfss_wire_bonds': True,
 'lead': {'end_jogged_extension': '',
          'end_straight': '0um',
          'start_jogged_extension': '',
          'start_straight': '0mm',
          'start_straigt': '0um'},
 'meander': {'asymmetry': '-300um',
             'spacing': '150um'},
 'pin_inputs': {'end_pin': {'component': 'open_end',
                            'pin': 'open'},
                'start_pin': {'component': 'coupl_1',
                              'pin': 'second_end'}},
 'total_length': '12mm',
 'trace_gap': '6um',
 'trace_width': '10um'},

type='CPW',
)




coupl_2 = CoupledLineTee(
design,
name='coupl_2',
options={'coupling_length': '650um',
 'coupling_space': '4um',
 'fillet': '50um',
 'orientation': '0',
 'pos_x': '1mm',
 'pos_y': '0'},

component_template=None,
)




open_end_2 = OpenToGround(
design,
name='open_end_2',
options={'orientation': '90',
 'pos_x': '1mm',
 'pos_y': '-2.25mm'},

component_template=None,
)




res_2 = RouteMeander(
design,
name='res_2',
options={'_actual_length': '12.000000000000005 '
                   'mm',
 'fillet': '50um',
 'hfss_wire_bonds': True,
 'lead': {'end_jogged_extension': '',
          'end_straight': '0um',
          'start_jogged_extension': '',
          'start_straight': '0mm',
          'start_straigt': '0um'},
 'meander': {'asymmetry': '-300um',
             'spacing': '150um'},
 'pin_inputs': {'end_pin': {'component': 'open_end_2',
                            'pin': 'open'},
                'start_pin': {'component': 'coupl_2',
                              'pin': 'second_end'}},
 'total_length': '12mm',
 'trace_gap': '6um',
 'trace_width': '10um'},

type='CPW',
)




coupl_qubit = CoupledLineTee(
design,
name='coupl_qubit',
options={'coupling_length': '650um',
 'coupling_space': '4um',
 'fillet': '50um',
 'orientation': '180',
 'pos_x': '-1.5mm',
 'pos_y': '0'},

component_template=None,
)




Readout_Res = RouteMeander(
design,
name='Readout_Res',
options={'_actual_length': '11.999999999999998 '
                   'mm',
 'fillet': '50um',
 'lead': {'end_jogged_extension': '',
          'end_straight': '0mm',
          'start_jogged_extension': '',
          'start_straight': '100um'},
 'pin_inputs': {'end_pin': {'component': 'coupl_qubit',
                            'pin': 'second_end'},
                'start_pin': {'component': 'Q1',
                              'pin': 'readout'}},
 'total_length': '12mm',
 'trace_gap': '6um',
 'trace_width': '10um'},

type='CPW',
)





            # WARNING
#options_connection_pads failed to have a value
Q1 = TransmonPocket(
design,
name='Q1',
options={'connection_pads': {'readout': {'cpw_extend': '100um',
                                 'cpw_gap': 'cpw_gap',
                                 'cpw_width': 'cpw_width',
                                 'loc_H': -1,
                                 'loc_W': -1,
                                 'pad_cpw_extent': '25um',
                                 'pad_cpw_shift': '5um',
                                 'pad_gap': '15um',
                                 'pad_height': '30um',
                                 'pad_width': '100um',
                                 'pocket_extent': '5um',
                                 'pocket_rise': '65um'}},
 'pad_width': '425 um',
 'pocket_height': '650 um',
 'pos_x': '-2.5 mm',
 'pos_y': '2.25 mm'}
)



gui.rebuild()
gui.autoscale()

# Keep the MetalGUI window open when this file is run as a standalone script
# (``python my_chip_design.py``). Without an event loop the process exits
# immediately and the window disappears.
#
# Guarded on __main__ so that importing this file -- or executing it inside a
# session that already runs a Qt loop (Jupyter/IPython with ``%gui qt``) --
# does not block the caller. ``gui.qApp`` may be None if no QApplication could
# be created (e.g. a headless machine), so check before calling into it.
if __name__ == "__main__" and gui.qApp is not None:
    gui.qApp.exec()
