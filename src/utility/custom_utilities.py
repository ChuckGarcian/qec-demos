from utility.utilities import Qubit
from typing import Optional

class debug_print:
    """ Debug Printing Utility
    """
    def __init__ (self, verbosity: str):
        import os
        os.environ["CG_VERBOSE"] = verbosity
    

    def dprint(self, obj, *args, verbosity=2, **kwargs):
        """
        Print is conditional on the passed verbosity level being less than or equal 
        to the environment variable 'CG_VERBOSE'. Default verbosity is 2.
        Can handle both strings and other objects.
        """
        import os
        cg_verbose = int(os.environ.get("CG_VERBOSE", "2"))
        
        if verbosity <= cg_verbose:
            if isinstance(obj, str):
                print(obj.format(*args, **kwargs))
            else:
                print(obj, *args, **kwargs)

class StimCircuitUtility:
    """ Custom Stim Utility Functions
    """
    def __init__ (self, distance: int):
        import stim
        self.initialized = True
        self.distance = distance
        self.stim     = stim.Circuit ()
        
    def gen_gate_from_single (self, gate_str: str, ancilla_idx: int) -> None: 
        """ Add Single Qubit STIM gate
        """
        self.stim.append (gate_str, [ancilla_idx])

    def gen_gate_from_list (self, gate_str: str, qubit_list: list[Qubit]) -> None:  
        """ Add Multi Qubit STIM Gate
        """
        indices = []
        
        for qbit in qubit_list:
            indices.append (qbit.idx)
            print (qbit.idx)    
        

        print (indices)
        self.stim.append (gate_str, indices)

    def write_to_stim (self, filepath: Optional[str] = "stim_circuit.stim") -> None:
        with open (filepath, 'w') as file:
            print ("\n---Wrote Stim To File {}---".format (filepath))
            circuit_string = self.stim.__str__()
            file.write (circuit_string)

    def gen_gate_from_range (self, gate_str: str, start: int, stop: int)-> str :
        """ Returns a string for a STIM circuit
        
        Returns a stim string, gate specified by 'gate_str' acting on qubits 'start'
        through 'stop'. Start and stop are integers representing the range of indices 
        to apply the gate to.
        """
        pass
        return    
        for i in range (start, stop + 1):    
            gate_str = self.gen_gate_from_single (gate_str, i)
        
        return gate_str 
