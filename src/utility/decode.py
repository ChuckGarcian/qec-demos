# Title: run.py
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import repetition_code


# Description: Decode and Plot Logical Error 
# Note: Credit to this article: https://quantum-for-the-confused.medium.com/how-to-build-a-3-qubit-repetition-code-from-scratch-in-5-simple-steps-using-stim-750befd0d738

import stim
from pathlib import Path
import pymatching

def benchmark_decoder_perf (depolar_prob=.1, flip_prob=.1, shots=100_000, distance=3):
  # Create Circuit
  circ = repetition_code.repetition (depolar_prob=depolar_prob, flip_prob=flip_prob, distance=distance).get_stim_circ ()

  # Generate an Error Model 
  dem = circ.detector_error_model (decompose_errors=True)
  
  # Get Samples
  """
  Detection Events: Number of times Detector flagged an error
  Observable Flips: Number of times observable was flipped
  """  
  sampler = circ.compile_detector_sampler()
  detection_events, observable_flips = sampler.sample (shots, separate_observables=True)

  # Generate Decoder from Error Model and make Predictions
  """
  We feed the decoder the detection events. If I understand correctly, it will then 
  try to match that to where in the circuit the error occurred. This is why the 
  error model is it important as it helps the decoder make decisions.
  """
  decoder = pymatching.Matching.from_detector_error_model (dem)
  predictions = decoder.decode_batch(detection_events)
  
  # Count Number of Logical Errors
  """
  We count the number of times reality (`observable_flips` and the
  decoder disagree).
  """
  nb_logical_errors = sum (bool (pred) !=obs_flip for pred, obs_flip in zip (predictions, observable_flips))
  logical_error_percent = (nb_logical_errors[0] / shots)

  return logical_error_percent

# Compute LER 
shots = 10_000
noise_levels = [0.1, 0.2, 0.3, 0.4, 0.5]
distance = [3, 5, 7]
ler = []
plt.figure(Path(__file__).name)

# Get LER for each Distance
for d in distance:
  xs = []
  ys = []
  
  # Compute LER
  for noise in noise_levels:
    ys.append (benchmark_decoder_perf (depolar_prob=noise, shots=shots, distance=d))
    xs.append (noise)

  plt.plot  (xs, ys, label="d={}".format(d))
plt.loglog ()
plt.xlabel ("Noise Level")
plt.ylabel ("Percentage of Logical Errors")

plt.legend ()
plt.show ()


