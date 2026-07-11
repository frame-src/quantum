from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

def balanced_oracle(f: QuantumCircuit):
    # This function implements a balanced oracle for a given quantum circuit
    # A balanced oracle is a function that returns 1 for half of the inputs and 0 for the other half
    # The oracle is implemented as a quantum circuit that performs a NOT operation on the second qubit
    # if the first qubit is 1
    f.cx(0, 1)
    return f

def constant_oracle(f: QuantumCircuit):
    # The oracle is implemented as a quantum circuit that performs a NOT operation on the second qubit
    # if the first qubit is 1
    f.x(1)
    return f

# First we'll define a quantum circuit that implements a query gate 
# for one of the four functions f1, f2, f3, f4 from one bit to one bit.
def deutsch_function(case: int):
    # This function generates a quantum circuit for one of the 4 functions
    # from one bit to one bit

    if case not in [1, 2, 3, 4]:
        raise ValueError("`case` must be 1, 2, 3, or 4.")

    f = QuantumCircuit(2)
    if case in [2, 3]:
        f = balanced_oracle(f)
    if case in [1, 4]:
        f = constant_oracle(f)
    return f


def compile_circuit(function: QuantumCircuit):

    n = function.num_qubits - 1
    circ = QuantumCircuit(n + 1, n)

    circ.x(n)
    circ.h(range(n + 1))

    circ.barrier()
    circ.compose(function, inplace=True)
    circ.barrier()

    circ.h(range(n))
    circ.measure(range(n), range(n))

    return circ


def deutsch_algorithm(function: QuantumCircuit):
    # Determine if a one-bit function is constant or balanced.

    circ = compile_circuit(function)

    result = AerSimulator().run(circ, shots=500, memory=True).result()
    counts = result.get_counts()
    print(counts)
    measurements = result.get_memory()
    if measurements[0] == "0":
        return "constant"
    return "balanced"

# deutsch_function(3).draw(output="mpl")
compile_circuit(deutsch_function(3)).draw(output="mpl")
plt.show()

f = deutsch_function(4)
print(deutsch_algorithm(f))