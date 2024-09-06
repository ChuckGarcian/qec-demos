def gen_gate_from_list (gate_str: str, qubit_list: list[str])->str :  
  return gate_str + ' '+ ' '.join(qubit_list) + " \n"

def gen_gate_from_range (gate_str: str, start: int, stop: int)-> str :
  """ Returns a string for a STIM circuit
  
  Returns a stim string, gate specified by 'gate_str' acting on qubits 'start'
  through 'stop'. Start and stop are integers representing the range of indices 
  to apply the gate to.
  """
  
  for i in range (start, stop + 1):
      gate_str = gate_str + ' {}'.format (i)  
  
  return gate_str + " \n"



def create_stim_repition_code (filepath, n, k, d):
  ancilla_idx = d
  print ("---Gen Repetition Stim: Starting---")
  print ("Parameters:\n\tn: {}\n\tk: {}\n\td: {}\n\tancilla_idx:{}".format (n,k,d, ancilla_idx))
  

  circuit = []  

  # -- Initialize Qubits --
  stim_str = gen_gate_from_range ("R", 0, k - 1)
  circuit.append (stim_str)
  
  # -- Apply Cnot --
  qubit_cx_pairs = []
  
  # Get data-ancilla pairings
  for data_idx in range (0, d):
    qubit_cx_pairs.extend ((str(data_idx), str(ancilla_idx)))

  stim_str = gen_gate_from_list ("CX", qubit_cx_pairs)
  circuit.append (stim_str)
  
  # -- Terminate and Measure --
  gen_gate_from_list ()
  
  stim_str = gen_gate_from_range ("M", ancilla_idx)
  circuit.append (stim_str)
  

  # Dump circuit to Stim file
  with open (filepath, 'w') as file:
    circuit_string = ''.join (circuit)
    print ("---Done Creating Stim: Printing Now---")
    print (circuit_string)
    file.write (circuit_string)

'''
n: Number of total bits per codeword
k: Number of encoded bits
d: Code distance
'''
n = 1 # Physical Qubit
k = 4 # Logical Qubit 
d = 3 # Distance 

if __name__ == "__main__":
  filepath = "repetition_code.stim"
  create_stim_repition_code (filepath, n, k, d)

