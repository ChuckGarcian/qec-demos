import stim
import os
from pathlib import Path

print ("\n---Display: Printing Stim Circuit First---")
path = Path(os.path.abspath (__file__))
src_dir = path.parent.parent.absolute ()
filename = "stim_circuit.stim"
filepath = os.path.join (src_dir, filename)

assert os.path.isfile (filepath)
circ_str = Path(filepath).read_text()

print ("\n---Display: Now Printing Diagram---")
circ = stim.Circuit(circ_str)
diagram_str = circ.diagram ()
print (diagram_str)



# detecter_sampler = circ.compile_detector_sampler ()
# print (detecter_sampler.sample (shots=10))