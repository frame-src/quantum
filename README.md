The fundamental element of quantum computing is the quantum circuit. 

A simple quantum circuit is a collection of qubits
and a list of instructions that act on those qubits.

This is a computational routine that can be run, one shot at a time, on a quantum processing unit (QPU).
A circuit will act on a predefined amount of quantum data with unitary operations, measurements and resets
, a quantum circuit can contain operations on classical data, including real-time computations and control-flow constructs, which are executed by the controller of the QPU.


Circuits are a low level of abstraction when building up quantum programs.
Such as the primitives of quantum computation, which accumulate data from many shots of quantum-circuit execution,
along with advanced error-mitigation techniques and measurement optimizations,
into well-typed classical data and error statistics.

In Qiskit, circuits can be defined in one of two regimes:

an abstract circuit, which is defined in terms of virtual qubits and arbitrary high-level operations, like encapsulated algorithms and user-defined gates.
a physical circuit, which is defined in terms of the hardware qubits of one particular backend, and contains only operations that this backend natively supports. You might also see this concept referred to as an ISA circuit.




