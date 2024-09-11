
# Sunday, 9.8.24

Suppose we have three data qubits. I still don't understand why the information the three are lost when we measure the ancilla qubits.

d: Code distance, is the number of errors/changes that need to be made on one code word to transform it into another

Generally when an error occurs we can view it as rotating a code word into an orthogonal space 

### Error Syndrome

An error syndrom is the result of concatenating all stabilizer checks into a single string. We can then interpret/decode the syndrome to determine what error occured and potentially how to correct it.


### AHA Moment - What Redundancy does in QEC

Problem:

Recall the state of qubit lays within a space called a *hilbert space*. I believe this is essentially just a vector space, maybe with some added constraints and restrictions. For a single qubit with basis states |0> and |1>, the hilbert space $H$ can be thought of as being the 2 dimensional spaced described by the span $H = span (|0>, |1>)$. [1]

Unitary operations on the state, transform the state such that it moves within the hilbert space. In quantum error correction, an error can transform a qubit such that a bit flip or phase flip can occur.

Solution:

To fix this issue, we can use redundancy qubits that expand the hilbert space into a higher dimension. For instance, for a single qubit, we can encode it using two reduancy qubits that span a four dimensional hilbert space: $H = span (|00>, |01>, |10>, |11>)$

----

Suppose we have a qubit that we want to make robust against $X$ gate errors, (a bit flip). We logically represent one qubit by Just like how a single qubit is represented as a superposition of the eigenstates of $Z$,  (i.e. computational basis states), we can write any arbitrary single qubit state as superposition of the eigen states (basis states) states of a pauli operator $P = X_1X_2X_3$. 



## AHA Moment - How to determine the number of Ancillas for any arbitrary stean code?

In stabilizer code [[n, k, d]], we take k qubits and encode them into k logical error corrected qubits. Because there are n physical bits, this means we have n - k redundancy qubits. The n-k redundancy qubits are entangled together with the k input qubits.

So, we must have m = n - k stabilizer measurements on these n - k redundancy qubits. Hence we need m total ancilla. [1 pg 11]



# References

- [1]: Quantum Error Correction: An Introductory Guide.

--------------------------------------------------------------------------------

# Wednesday, 9.11.24

### Code Concatination

Code concatenation is the process of embedding the output of one code into another code. 

In shores code, the bit flips are embedded to create the codewords of phaseflips