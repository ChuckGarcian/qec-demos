from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, quantum_info, transpile
from qiskit.quantum_info import Pauli
from qiskit_aer import AerSimulator
from qiskit.circuit.library import StatePreparation

import numpy as np
import math

# Author: Chuck Garcia, UT Austin

def perform_kronecker_reduction(mat_list: list) -> np.array:
    """ Reduces the list of matrices into a single matrix by performing kronecker products
    """
    kron_res = None

    for mat, _ in mat_list: 
        if kron_res is None:
            kron_res = mat
        else:
            kron_res = np.kron(mat, kron_res)  

    return kron_res

class StabilizerChecksHelper:
    """  Class to help prepare logical qubit state from given stabilizer checks
    Author: Chuck Garcia
    """
    def __init__(self):
        pass
    
    @staticmethod
    def get_stabilizer_projector (num_qubits: int, stabilizers: list) -> np.array:
        """ Returns projector matrix which projects onto the common +1 eigenspace 
        of the given list of stabilizer checks using the formula P = ∏ᵢ (I + Sᵢ)/2
        """
        I = np.eye (2**num_qubits)
        result = None
        
        for stabilizer in stabilizers:
            if result is None:
              result = I + stabilizer
            else:
              result = result.dot((I + stabilizer))        
        return result 

    @staticmethod
    def get_stabilizer_matrix(pauli_string: str) -> np.array:
        """ Returns tensor pauli product generated from 'pauli_string'.
            Example: 'XX' -> np.kron(x_gate, x_gate)
        """
        
        Z_gate = np.array([[1, 0], [0, -1]])
        X_gate = np.array([[0, 1], [1, 0]])
        I_gate = np.eye(2)

        stabilizer_gates = []

        # Construct list of pauli gates from given Pauli string
        for pauli_gate in pauli_string:
            if pauli_gate == 'X':
                stabilizer_gates.append((X_gate, "x_gate"))
                
            elif pauli_gate == 'Z':
                stabilizer_gates.append((Z_gate, "z_gate"))
                
            else:
                stabilizer_gates.append((I_gate, "I_gate"))
        
        result = perform_kronecker_reduction(stabilizer_gates)
        return result

    @staticmethod
    def normalize(v):
        norm = np.linalg.norm(v)
        if norm == 0: 
            return v
        return v / norm

    @staticmethod        
    def stabilizer_measurements_from_str (pauli_str_list, qr_pair, cr_pair):
        """ Returns stabilizer extraction circuit corresponding to the given list of paili strings
        (stabilizer as a pauli product)
        Args:
            qr_pair: Tuple containing the quantum registers (Data Register, Parity register)
            cr_pair: Tuple containing the classical registers (Data classical, Parity classical)
        """
        dr, pr = qr_pair
        
        stabilizer_extraction = QuantumCircuit (dr, pr, cr_pair[0], cr_pair[1])
        
        # Add stabilizer checks
        for parity_idx, pauli_str in enumerate(pauli_str_list):
            for data_idx, x in enumerate(pauli_str):    
                if x == 'X':
                    stabilizer_extraction.cx (dr[data_idx], pr[parity_idx])
                elif x == 'Z':
                    stabilizer_extraction.h(dr[data_idx])
                    stabilizer_extraction.cx (dr[data_idx], pr[parity_idx])
                    stabilizer_extraction.h(dr[data_idx])
                elif x != 'I':
                    assert 1 == 0, "Incorrect pauli string passed!!!!"
        
        return stabilizer_extraction

    @staticmethod
    def get_logical_codec (stabilizer_checks: list, n: int):
        """ Returns the encoder instr and inverse encoder instr associated 
        with the given stabilizer checks.
        
        Returned data types are qiskit instructions. Encoder prepares logical 
        state zero. 'inverse encoder' inverts the logical state back to original
        state (i.e. inverts entanglement for measurement)

        Args:
            stabilizer_checks: List of pauli string corresponding to stabilizer checks
            n: Integer representing number of data qubits
        """
        
        # Validate pauli strings into np.array representations
        stabilizer_matrices = []
        
        for mat in stabilizer_checks: 
            stabilizer_matrices.append(StabilizerChecksHelper.get_stabilizer_matrix(mat))

        # Generate projector and project input state onto eigenspace of all stabilizers            
        projector = StabilizerChecksHelper.get_stabilizer_projector (n, stabilizer_matrices)
        ket0000 = np.zeros (2**n)
        ket0000[0] = 1
        res = projector.dot(ket0000)
        
        # Finally use qiskit to get instructions which prepare/unprepare state
        sv = quantum_info.Statevector(res)
        encoder = StatePreparation(sv, normalize=True)
        inverse_decoder = StatePreparation(sv, normalize=True, inverse=True)
        
        return encoder, inverse_decoder

    @staticmethod
    def get_dirac (state_vector):
        """ Returns the state vector in Dirac notation.
        """
        n = int(np.log2(len(state_vector))) 
        dirac_notation = ""
        
        for i, amplitude in enumerate(state_vector):
            if np.abs(amplitude) > 1e-10:  # Ignore very small amplitudes
                binary_state = format(i, f'0{n}b')
                dirac_notation += f"{amplitude:.2f}|{binary_state}> + "
        
        return dirac_notation.rstrip(' + ')

class StabilizerCodesManager:
    """ Generates qiskit stabilizer circuit on input of all the stabilizers 
    specifying the code. 
        
        Example: 4 qubit code: S = {'XXXX', 'ZZZZ'} |--> Qiskit Circuit
    """
    def __init__(self, stabilizer_checks: list, n: int):
        """
        Args:
            stabilizer_checks: Stabilizer group S
            n: Integer, the number of data qubits
        """
        self.stabilizer_checks = stabilizer_checks
        self.n = n
        self._setup_circuit()

    def _setup_circuit(self):
        """Initialize and setup the basic circuit structure"""
        helper = StabilizerChecksHelper()
        
        # Generate logical state codecs
        self.enc_instr, self.dec_instr = helper.get_logical_codec(self.stabilizer_checks, self.n)
        
        # Define quantum and classical registers
        self.data_qreg = QuantumRegister(self.n, name='Data Qreg')
        self.parity_qreg = QuantumRegister(len(self.stabilizer_checks), name='Parity Qreg')
        self.data_creg = ClassicalRegister(self.n, name='Data Creg')
        self.parity_creg = ClassicalRegister(len (stabilizer_checks), name='Parity Creg')
        
        self.qc = QuantumCircuit(self.data_qreg, self.parity_qreg, self.data_creg, self.parity_creg)
        self.qc.append(self.enc_instr, self.data_qreg)
        self.qc.barrier(label="Encoding")

    def insert_error(self, error_type: str, qubit_idx: int):
        """Insert error gate at specified position"""
        if error_type.lower() == 'z':
            self.qc.z(self.data_qreg[qubit_idx])
        elif error_type.lower() == 'x':
            self.qc.x(self.data_qreg[qubit_idx])
        self.qc.barrier(label=f"{error_type.upper()} Error")
    
    def build_circuit(self):
        """Complete the circuit with extraction and decoding"""
        helper = StabilizerChecksHelper()
        
        # Stabilizer Extraction Circuit
        extract_circ = helper.stabilizer_measurements_from_str(
            self.stabilizer_checks,
            (self.data_qreg, self.parity_qreg), 
            (self.data_creg, self.parity_creg)
        )
        
        # Compose and complete circuit
        final_circ = self.qc.compose(extract_circ)
        final_circ.barrier(label="Extraction")
        final_circ.measure(self.parity_qreg, self.parity_creg)
        final_circ.barrier(label="Parity Measurement")
        
        final_circ.append(self.dec_instr, self.data_qreg)
        final_circ.barrier(label='Invert Encoding')
        final_circ.measure(self.data_qreg, self.data_creg)
        
        return final_circ

    def run_circuit(self, circuit, shots=1000):
        """Run the circuit simulation"""
        simulator = AerSimulator()
        transpiled_circ = transpile(circuit, simulator)
        result = simulator.run(transpiled_circ, shots=shots).result()
        return result.get_counts()
        


        
def example_ZZZZ_XXXX ():
    #Test: S = {ZZZZ, XXXX}, Pauli stabilizer checks
    manager = StabilizerCodesManager(stabilizer_checks=['XXXX', 'ZZZZ'], n=4)

    manager.insert_error('z', 2)
    
    circuit = manager.build_circuit()
    counts = manager.run_circuit(circuit)
    
    print(circuit)
    print(counts)

def create_stabilizer_str(indices, check_type, num_qubits):
    stabilizer = ['I'] * num_qubits
    
    for idx in indices:
        stabilizer[idx] = check_type
    
    return ''.join(stabilizer)

# Example usage
indices = (6, 7)
check_type = 'X'
num_qubits = 9

# print(create_stabilizer_str(indices, check_type, num_qubits))  # Output: IXXIIX

def example_9_rotated_surface ():
    n = 9
    stabilizer_checks = [
                
        'IXXIIIIII',  # Tile 9: X-type  -> 1, 2
        'ZIIZIIIII',  # Tile 10: Z-type -> 0, 3
        'XXIXXIIII',  # Tile 11: X-type -> 0,1,3,4
        'IZZIZZIII',  # Tile 12: Z-type -> 1,2,4,5
        'IIIZZIZZI',  # Tile 13: Z-type -> 3,4,6,7
        'IIIIXXIXX',  # Tile 14: X-type -> 4,5,7,8
        'IIIIIZIIZ'   # Tile 15: Z-type -> 5,8
        'IIIIIIXXI'   # Tile 16: X-type -> 6, 7
    ]

    # Initialize manager with n=9 qubits for the white circles (0-8)
    manager = StabilizerCodesManager(stabilizer_checks=stabilizer_checks, n=9)

    # manager.insert_error('x', 3)

    circuit = manager.build_circuit()
    counts = manager.run_circuit(circuit)
    print (circuit)
    circuit.draw ('mpl')    

if __name__ == "__main__":
    n = 9
    stabilizer_checks = [            
    'IXXIIIIII',  # Tile 9: X-type  -> 1, 2
    'ZIIZIIIII',  # Tile 10: Z-type -> 0, 3
    'XXIXXIIII',  # Tile 11: X-type -> 0,1,3,4
    'IZZIZZIII',  # Tile 12: Z-type -> 1,2,4,5
    'IIIZZIZZI',  # Tile 13: Z-type -> 3,4,6,7
    'IIIIXXIXX',  # Tile 14: X-type -> 4,5,7,8
    'IIIIIZIIZ',   # Tile 15: Z-type -> 5,8
    'IIIIIIXXI',   # Tile 16: X-type -> 6, 7
    ]

    # Initialize manager with n=9 qubits for the white circles (0-8)
    manager = StabilizerCodesManager(stabilizer_checks=stabilizer_checks, n=9)

    # manager.insert_error('x', 3)

    circuit = manager.build_circuit()
    counts = manager.run_circuit(circuit)    
    print (circuit)
    # example_ZZZZ_XXXX ()
    # example_9_rotated_surface ()
