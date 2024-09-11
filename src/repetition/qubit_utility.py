# Code is written by: https://github.com/jasonchadwick/stim_surface_code/blob/main/stim_surface_code/patch.py
class Qubit():
    """A single physical qubit on a device.
    """
    def __init__(self, idx: int, coords: tuple[int, int]) -> None:
        """Initialize.
        
        Args:
            idx: Index of the qubit.
            coords: Coordinates of the qubit on the device.
        """
        self.idx: int = idx
        self.coords: tuple[int, int] = coords

    def __repr__(self) -> str:
        return f'{self.idx}, Coords: {self.coords}'

class DataQubit(Qubit):
    """Data qubit used to store logical information.
    """
    pass

class MeasureQubit(Qubit):
    """Ancilla qubit used to perform stabilizer measurements.
    """
    def __init__(self, idx: int, coords: tuple[int, int], data_qubits: list[DataQubit | None], basis: str) -> None:
        """Initialize.
        
        Args:
            idx: Index of the qubit.
            coords: Coordinates of the qubit on the device.
            data_qubits: List of data qubits that this qubit measures.
        """
        super().__init__(idx, coords)
        self.data_qubits = data_qubits
        self.basis = basis

    def __repr__(self):
        return f'{self.idx}, Coords: {self.coords}, Basis: {self.basis}, Data Qubits: {self.data_qubits}'

