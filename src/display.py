import stim
from pathlib import Path

print ("---Display: Printing Stim Circuit First---")
circ_str = Path("repetition_code.stim").read_text()
print (circ_str)

print ("---Display: Now Printing Diagram---")
circ = stim.Circuit(circ_str)
diagram_str = circ.diagram ()
print (diagram_str)
