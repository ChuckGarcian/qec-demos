import stim
from pathlib import Path

print ("\n---Display: Printing Stim Circuit First---")
circ_str = Path("repetition_code.stim").read_text()
print (circ_str)

print ("\n---Display: Now Printing Diagram---")
circ = stim.Circuit(circ_str)
diagram_str = circ.diagram ()
print (diagram_str)

print ("\n---Display: Sampling---")


# detecter_sampler = circ.compile_detector_sampler ()
# print (detecter_sampler.sample (shots=10))