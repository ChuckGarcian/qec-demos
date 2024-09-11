# Title: repetition_code.py
# Author: Chuck Garcia

import numpy as np
import stim

def gen_gate_from_single (gate_str: str, ancilla_idx: int) ->str : 
  """ Return STIM gate acting on one qubit
  """
  return "{} {}".format(gate_str, str(ancilla_idx))


def gen_gate_from_list (gate_str: str, qubit_list: list[str])->str :  
  qubit_list = map(str, qubit_list)
  return gate_str + ' '+ ' '.join(qubit_list) 

def gen_gate_from_range (gate_str: str, start: int, stop: int)-> str :
  """ Returns a string for a STIM circuit
  
  Returns a stim string, gate specified by 'gate_str' acting on qubits 'start'
  through 'stop'. Start and stop are integers representing the range of indices 
  to apply the gate to.
  """
  
  for i in range (start, stop + 1):    
      gate_str = gen_gate_from_single (gate_str, i)
  
  return gate_str 

class repetition:
  
  def __init__(self, depolar_prob=.1, flip_prob=.1, distance = 2) -> None:
    ''' Distance d Repetition Code
    Arguments: 
      n: Number of total bits per codeword
      k: Number of encoded bits
      d: Code distance
    '''
    self.n = distance
    self.k = 1
    self.m = self.n - self.k
    self.filepath = "repetition_code.stim"

    self.data_qubits  = np.arange (0, self.n)
    self.ancilla_qubits = np.arange (self.m) + self.n
    self.circ_list     = []  
    
    self.initialize (depolar_prob, flip_prob, distance)    
    # print ("\n---Gen Repetition Stim: Starting---")
    # print ("Parameters:\n\tn: {}\n\tk: {}\n\tm: {}\n\tdata_qubits: {}\n\tancilla_qubits: {}".format (self.n,self.k,self.m, self.data_qubits, self.ancilla_qubits))

  def tick (self):
    self.circ_list.append ("TICK")  
  
  def initialize (self, depolar_prob=.1, flip_prob=.1, distance = 2) -> None:
    # -- Initialize Qubits --
    stim_str = gen_gate_from_range ("R", 0, self.n)
    self.circ_list.append (stim_str)
    self.tick()

    # Apply Noise
    self.add_depolar (p=depolar_prob)

    # -- Apply CNOT --
    self.stabilize ()

    # -- Terminate and Measure --
    # self.add_gate_error (self.ancilla_qubits, p=flip_prob)
    # self.add_gate_error (self.data_qubits, p=flip_prob)
    self.terminate ()

  def add_depolar (self, p) -> None:
    stim_str = gen_gate_from_list ("DEPOLARIZE1({})".format (p), self.data_qubits)
    self.circ_list.append (stim_str)
  
  def add_gate_error (self, qubit_list, gate="X", p=.01):
    stim_str = gen_gate_from_list ("{}_ERROR({})".format (gate, str(p)), qubit_list)
    self.circ_list.append (stim_str)
    
  
  def stabilize (self) -> None:
    data_idx = 0
    
    # Get data-ancilla pairings
    for ancilla_idx in self.ancilla_qubits:
      stim_str = gen_gate_from_list ("CX", [data_idx, ancilla_idx])
      stim_str2 = gen_gate_from_list ("CX", [data_idx + 1, ancilla_idx])
      self.circ_list.append (stim_str)
      self.circ_list.append (stim_str2)
      data_idx += 1
    
    
  def terminate (self) -> None:
    self.tick()
    # Measure Data
    stim_str = gen_gate_from_list ("M", self.data_qubits)
    self.circ_list.append (stim_str)    
    
    # Measure Logical Observable
    self.circ_list.append ("OBSERVABLE_INCLUDE(0) rec[-1]")    
    
    # Add Data Detectors
    detections = []
    for i in range (2, self.data_qubits.size + 1): 
      detections.append("DETECTOR rec[-{}]".format (i))
    self.circ_list.extend (detections)
    
    # Measure Ancilla
    stim_str = gen_gate_from_list ("MR", self.ancilla_qubits)
    self.circ_list.append (stim_str)
    
    # Finally Add Ancilla Detectors
    detections = []
    for i in range (1, self.ancilla_qubits.size+1): 
      detections.append("DETECTOR rec[-{}]".format (i))
    self.circ_list.extend (detections)
    
  def get_str (self):
    return '\n'.join (self.circ_list)
  
  def get_stim_circ (self):
    return stim.Circuit(self.get_str ())

  def write_to_stim (self) -> None:
    with open (self.filepath, 'w') as file:
      circuit_string = '\n'.join (self.circ_list)
      print ("\n---Done Creating Stim: Printing Now---")
      print (circuit_string)
      file.write (circuit_string)

def main (depolar_prob=.1, flip_prob=.1, distance = 2):
  circ = repetition (depolar_prob=.1, flip_prob=.1, distance = 2)
  circ.write_to_stim ()
  

if __name__ == "__main__":
  main ()  

