# Title: shore.py
# Author: Chuck Garcia
# Description: Naive Implementation of shore code in stim

import stim
from utility.custom_utilities import StimCircuitUtility, debug_print
from utility.utilities import DataQubit, MeasureQubit
from typing import Optional

class Shore (StimCircuitUtility):
  """ (9, 3, 1) Shore Code Implementation
  """
  
  def __init__ (self, verbosity: Optional[str] = "0", distance: Optional[int] = 9):
    super().__init__ (distance)
    
    # Stabilizers (Hard Coded for now)
    num_z = 6
    num_x = 2    
    
    # Initialize Code Parameters
    self.data_qubits    = self._init_data (distance)
    self.ancilla_qubits = self._init_ancillas (self.data_qubits, num_z, num_x)
    
    # Debug Prints
    self.dprint = debug_print (str(verbosity)).dprint
    self.dprint(type(self.ancilla_qubits))
    self.dprint ("Ancillas: {}".format(self.ancilla_qubits))
    
  
  def _init_data (self, distance: int) -> DataQubit:
    """ Initializes Qubit Set.
      
    Arguments:
      distance: Code distance. Really this is just the number of data qubits. 
    """
    result = [DataQubit (idx=i, coords=(0, i)) for i in range(distance)]
  
    return result


  def _init_ancillas (self, targets: list[DataQubit], num_z: int, num_x: int) -> MeasureQubit:
    """ Initialize and return list of Ancilla Qubits
    
    Arguments:
      targets: List of Data qubits the ancilla are measuring
      num_z: Number of total Z stabilizers. For example, [[9,1,3]] shore code 
             has 6 Z stabilizers and 2 X Stabilizer measurements
      num_x: Number of total X stabilizer
    """
    result = []
    idx    = len (targets) # First Ancilla, After last DataQubit
    
    # Init Z Stabilizers
    for data_idx in range (num_z):
      coords  = (0, idx)
      Z_pairs = targets[data_idx], targets[data_idx + 1]  #Z1Z2, Z2_Z3 ...
      basis   = "Z"

      result.append(MeasureQubit (idx, coords, Z_pairs, basis))
      idx     = idx + 1

    # Init X Stabilizer
    for data_idx in range (num_x):

      coords  = (0, idx)  
      X_pairs = [targets[data_idx + i] for i in range(num_z)]
      basis   = "X"

      result.append (MeasureQubit (idx, coords, X_pairs, basis))
      idx     = idx + 1

    return result

  def reset_circ (self) -> None:
    """ Reset all data and ancilla qubits 
    """
    assert self.initialized, ValueError ("Error: Not yet Initialized")
    
    self.gen_gate_from_list ("R", self.data_qubits)
    self.gen_gate_from_list ("R", self.ancilla_qubits)
        

  def setup_circ (before_cycle_depolar: Optional[float] = .01, gate_error: Optional[float] = .01):
    """ Places Qubits onto Stim Circuit, with the given error rates.
    Arguments:
      before_cycle_depolar: Depolarization added at the start of a cycle
      gate_error: Gate flip error rate prior to measurements
    """
    
    pass
  
  def print_circ (self):
    print ("--Printing Stim Circuit---")
    print (self.stim.diagram ())

  def get_stim (self):
    return self.stim
    

def main ():
  shore = Shore (verbosity=2)
  shore.reset_circ ()
  shore.setup_circ ()
  shore.print_circ ()
  shore.write_to_stim  ()
  # circ = shore.get_stim ()
  
  print ("Hello world!")

main ()


