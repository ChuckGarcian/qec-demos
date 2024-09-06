# Title: repetition_code.py
# Author: Chuck Garcia

def gen_gate_from_single (gate_str: str, ancilla_idx: int):
  """ Return STIM gate acting on one qubit
  """
  return "{} {}".format(gate_str, str(ancilla_idx))


def gen_gate_from_list (gate_str: str, qubit_list: list[str])->str :  
  return gate_str + ' '+ ' '.join(qubit_list) + " \n"


def gen_gate_from_range (gate_str: str, start: int, stop: int)-> str :
  """ Returns a string for a STIM circuit
  
  Returns a stim string, gate specified by 'gate_str' acting on qubits 'start'
  through 'stop'. Start and stop are integers representing the range of indices 
  to apply the gate to.
  """
  
  for i in range (start, stop + 1):
      gen_gate_from_single (gate_str, i)
  
  return gate_str + " \n"

class repetition:
  
  def __init__(self, n, k, d) -> None:
    '''
    Arguments: 
      n: Number of total bits per codeword
      k: Number of encoded bits
      d: Code distance
    '''
    
    self.n = n
    self.k = k
    self.d = d
    self.ancilla_idx = d
    self.circ_list = []  
    self.ancilla_idx = d
    
    print ("\n---Gen Repetition Stim: Starting---")
    print ("Parameters:\n\tn: {}\n\tk: {}\n\td: {}\n\tancilla_idx:{}".format (n,k,d, self.ancilla_idx))
    
  def initialize (self) -> None:
    stim_str = gen_gate_from_range ("R", 0, self.k - 1)    
    self.circ_list.append (stim_str)


  def stabilize (self) -> None:
    qubit_cx_pairs = []
    
    # Get data-ancilla pairings
    for data_idx in range (0, self.d):
      qubit_cx_pairs.extend ((str(data_idx), str(self.ancilla_idx)))

    stim_str = gen_gate_from_list ("CX", qubit_cx_pairs)
    self.circ_list.append (stim_str)
    
  def terminate (self) -> None:
    stim_str = gen_gate_from_range ("R", 0, self.ancilla_idx) # Restore All
    self.circ_list.append (stim_str)
    
    stim_str = gen_gate_from_single ("M", self.ancilla_idx)
    self.circ_list.append (stim_str)
  
  def write_to_stim (self, filepath) -> None:
    with open (filepath, 'w') as file:
      circuit_string = ''.join (self.circ_list)
      print ("\n---Done Creating Stim: Printing Now---")
      print (circuit_string)
      file.write (circuit_string)

def main ():
  n = 1 # Physical Qubit
  k = 4 # Logical Qubit 
  d = 3 # Distance 

  filepath = "repetition_code.stim"
  
  # -- Initialize Qubits --
  circ = repetition (n, k, d)

  # -- Apply CNOT --
  circ.stabilize ()

  # -- Terminate and Measure --
  circ.terminate ()
  
  # -- Dump circuit to Stim file --
  circ.write_to_stim (filepath)


if __name__ == "__main__":
  main ()  

