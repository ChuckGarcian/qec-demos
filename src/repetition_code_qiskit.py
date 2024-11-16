from qiskit import (
    QuantumCircuit,
    QuantumRegister,
    ClassicalRegister,
    transpile,
    Aer,
    execute
)
from qiskit.tools.visualization import plot_histogram
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt


class RepetitionCode:
    def __init__(self, distance=3, init_data_val: int = 0, Z_type: bool = False):
        """Repetition code which corrects (distance - 1) / 2 errors.

        Args:
            distance: Code distance; Total number of parity qubits is distance - 1.
            init_data_val: Initial data qubit value
        """
        self.logical_count = distance    # Using this as total qubit count for now
        self.parity_count = distance - 1  # Todo: Determine parameterization
        self.__Z_type = Z_type

        self.logical = QuantumRegister(self.logical_count, name="data_qubits")
        self.parity = QuantumRegister(self.parity_count, name="parity_qubits")
        self.syndrome = ClassicalRegister(self.parity_count, name="syndrome_measurement")
        self.logical_mz = ClassicalRegister(self.logical_count, name="data_measurement")

        self.circ = QuantumCircuit(
            self.logical,
            self.parity,
            self.syndrome,
            self.logical_mz
        )
        
        if init_data_val:
            self.circ.x(0)
    
    def entangle(self) -> None:
        """Entangle data qubits with redundancy qubits."""
        
        for idx in range(1, self.logical_count):
            self.circ.cx(0, self.logical[idx])            
        
        if self.__Z_type:
           self.circ.h (self.logical)
        
        self.circ.barrier(label="Encode")
   
    def reverse_entangle(self) -> None:
        """Reverse entangled data qubits with redundancy qubits (End of circuit)."""
    
                
        if self.__Z_type:
           self.circ.h (self.logical)
        
        for idx in range(1, self.logical_count):
            self.circ.cx(0, self.logical[idx])            
            
        self.circ.barrier(label="Disentangle")

    def measure_logical(self) -> None:
        """Measure logical qubits to classical register."""
        self.circ.measure(self.logical, self.logical_mz)
        self.circ.barrier(label="Measure Logical")        

    def measure_syndrome(self) -> None:
            """Insert syndrome extraction logic for detecting errors.
            
            The syndrome is measured and stored in classical bit registers.
            
            Args:
                X_type: If True, detect X errors; if False, detect Z errors.
            """

            if self.__Z_type:
                self.circ.h (self.logical)
            
            # Collect parity information
            for idx in range(0, len(self.parity)):
                # Control qubits for parity check
                p1 = self.logical[idx]      # Zi     
                p2 = self.logical[idx + 1]  # Zi+1
                
                # Perform parity check with control Z's
                self.circ.cx([p1, p2], self.parity[idx])

            if self.__Z_type:
                self.circ.h (self.logical)                                        

            # Extract Syndrome -- Measure parity
            self.circ.barrier(label="Syndrome Extraction")        
            self.circ.measure(self.parity, self.syndrome)
    
    def decode_and_correct_error(self) -> None:
        """Correct error at the given qubit index."""
        
        from qiskit.circuit.library import XGate, ZGate 
        
        if self.__Z_type:   
            error_correction = ZGate()            
        else:
            error_correction = XGate()

        # {01} -> IIX
        with self.circ.if_test((self.syndrome, 1)):
            self.circ.append (error_correction, [0])
        
        # {10} -> XII
        with self.circ.if_test((self.syndrome, 2)):
            self.circ.append (error_correction, [2])
        
        # {11} -> IXI
        with self.circ.if_test((self.syndrome, 3)):
            self.circ.append (error_correction, [1])
        
        self.circ.barrier(label="Decode and Correct")

    def inject_error(self, p: float = 0.5) -> None:
        """Inject Error gate error with probability p.
        
        Args:
            p: probability of incorrect application
        """
        np.random.seed(49)  # Reproducibility
        
        error_type_func = self.circ.z if self.__Z_type else self.circ.x
        
        # Apply random errors on data qubits
        for idx in range(len(self.logical)):            
            error = np.random.choice([0, 1], p=[1 - p, p]) 
            
            if error:
                error_type_func(self.logical[idx])    
            
        self.circ.barrier(label="Inject {}".format(
            "Z Error" if self.__Z_type else "X Error"
        ))        
            
    def run_circuit(self):
        """Execute the quantum circuit and return counts."""
        simulator = AerSimulator()
        circ = transpile(self.circ, simulator)                
        result = simulator.run(circ).result()
        return result.get_counts()
        
    def get_logical_and_syndrome_strings(self, results):
        """Extract logical and syndrome strings from results."""
        outcome = list(results.int_outcomes().keys())[0]     
        binary = bin(outcome)[2:].zfill(self.parity_count + self.logical_count)
        
        syndrome_results = binary[0:self.logical_count]
        logical_results = binary[self.logical_count:]
        
        return syndrome_results, logical_results        

    def get_circuit (self) -> QuantumCircuit:
        return self.circ
    
    def plot_circuit(self) -> None:
        """Display the circuit diagram."""
        self.circ.draw(output="mpl")
        plt.show()

    def __str__(self):
        """Return circuit string representation."""
        return str(self.circ)


def decode(syndrome: str) -> int:
    """Decode syndrome measurement to error location."""
    decode_map = {
        "00": 0,
        "01": 1,
        "10": 3,   
        "11": 2,
    }        
    return decode_map[syndrome]

def repetition_bit_flip(error_injection_circuit=None):
    """Run bit flip error correction circuit."""
    # Build Circuit    
    circuit = RepetitionCode()
    circuit.entangle()
    circuit.inject_error()
    circuit.measure_syndrome()
    circuit.decode_and_correct_error()
    circuit.reverse_entangle()
    circuit.measure_logical()
    
    # Run Circuit 
    results = circuit.run_circuit()

    # Plot results
    circuit.plot_circuit()    
    plot_histogram(results)
    plt.show()

def repetition_phase_flip(error_injection_circuit=None):
    """Run phase flip error correction circuit."""

    # Build Circuit    
    circuit = RepetitionCode(Z_type=True)
    circuit.entangle()
    circuit.inject_error()
    circuit.measure_syndrome()
    circuit.decode_and_correct_error()
    circuit.reverse_entangle()
    circuit.measure_logical()
    
    # Run Circuit 
    results = circuit.run_circuit()

    # Plot results
    circuit.plot_circuit()    
    plot_histogram(results)
    plt.show()
if __name__ == "__main__":
    # repetition_bit_flip()
    repetition_phase_flip()