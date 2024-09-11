
# Questions about QIS

## Probability Computation

Suppose $|\psi>$ is a state vector of 1 qubit. 
Why is he probability of quantum state  Probability $P(|0>) = |\alpha_0>|^2$ can be also calculate by taking the the product of the psi and its conjugate?

## What Exactly does a tensoring operation do?

# Questions About Stim


## Why are there two objects we are detecting in stim getting_started part 5. it shows "DETECTOR(1, 0) rec[-8] rec[-16]"

I would have thought we just have one detector per ancilla.

Answer: AHA-Moment: I think I finnaly understand. If one looks at the stim output text in part 5 we see that DETECTOR instructions that have two targets are inside the repeat loop. It seems like they are referencing the same ancilla qubit but just in two different iterations of the loop. 

For example:
```
  stim.Circuit('''
      R 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
      TICK
      DEPOLARIZE1(0.04) 0 2 4 6 8 10 12 14 16
      CX 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
      TICK
      CX 2 1 4 3 6 5 8 7 10 9 12 11 14 13 16 15
      TICK
      X_ERROR(0.01) 1 3 5 7 9 11 13 15
      MR 1 3 5 7 9 11 13 15
      DETECTOR(1, 0) rec[-8]
      DETECTOR(3, 0) rec[-7]
      DETECTOR(5, 0) rec[-6]
      DETECTOR(7, 0) rec[-5]
      DETECTOR(9, 0) rec[-4]
      DETECTOR(11, 0) rec[-3]
      DETECTOR(13, 0) rec[-2]
      DETECTOR(15, 0) rec[-1]
      REPEAT 24 {
          TICK
          DEPOLARIZE1(0.04) 0 2 4 6 8 10 12 14 16
          CX 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
          TICK
          CX 2 1 4 3 6 5 8 7 10 9 12 11 14 13 16 15
          TICK
          X_ERROR(0.01) 1 3 5 7 9 11 13 15
          MR 1 3 5 7 9 11 13 15
          SHIFT_COORDS(0, 1)
          DETECTOR(1, 0) rec[-8] rec[-16]
          DETECTOR(3, 0) rec[-7] rec[-15]
          DETECTOR(5, 0) rec[-6] rec[-14]
          DETECTOR(7, 0) rec[-5] rec[-13]
          DETECTOR(9, 0) rec[-4] rec[-12]
          DETECTOR(11, 0) rec[-3] rec[-11]
          DETECTOR(13, 0) rec[-2] rec[-10]
          DETECTOR(15, 0) rec[-1] rec[-9]
      }
      X_ERROR(0.01) 0 2 4 6 8 10 12 14 16
      M 0 2 4 6 8 10 12 14 16
      DETECTOR(1, 1) rec[-8] rec[-9] rec[-17]
      DETECTOR(3, 1) rec[-7] rec[-8] rec[-16]
      DETECTOR(5, 1) rec[-6] rec[-7] rec[-15]
      DETECTOR(7, 1) rec[-5] rec[-6] rec[-14]
      DETECTOR(9, 1) rec[-4] rec[-5] rec[-13]
      DETECTOR(11, 1) rec[-3] rec[-4] rec[-12]
      DETECTOR(13, 1) rec[-2] rec[-3] rec[-11]
      DETECTOR(15, 1) rec[-1] rec[-2] rec[-10]
      OBSERVABLE_INCLUDE(0) rec[-1]
  ''')
```

Here we see that DETECTOR () rec[-8] rect[-16] refers to the measurement MR 1. 
We do it this way so we can assert the measurement of 1 is consistent across iterations. If it is not then an error has occurred.

## How does d relate to n and k?

In stim 'getting_started' doc, for the repetition code example, the author create the circuit only by specifying the fact it is a repetition code and the code distance d=9. How does stim know to create?

## What is the parameter in Detector (0, 3)

In the getting_started.ipynb, and gates.md in docs, I see the detector instruction being used like 'DETECTOR(0, 3)'. In other words, they pass a list of values. What does that mean?

Answer: They are qubits coords according to gates.md

## What is a 'stabilizer measurement'

In a logical qubit logical state space is distributed over data qubits.

According to "QEC: An Introductory Guide", we perform a *parity check*, by performing "Perform the measurement of the $Z_1Z_2$ stabilizers. What does this mean?


## How many Ancilla?

Given a stean code [n, k, d] how does one know the number of ancilla bits used?

For instance, ina [[3, 1, 3]] repetition code, there are 3 data qubits and 2 ancilla qubits. How did they get 2 ancilla?


Answer: I think it is based off the given parity check. I.e. the parity checks or the number of stabilizer measurements determine the number of ancillas