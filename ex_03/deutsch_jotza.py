from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import numpy as np


# def add_cx(qc, bit_string):
#     print("Bist string: ")
#     print(bit_string)
#     for qubit, bit in enumerate(reversed(bit_string)):
#         if bit == "1":
#             qc.x(qubit)
#     return qc

def balanced_oracle(qc: QuantumCircuit, num_qubits: int):
    # This function implements a balanced oracle for a given quantum circuit
    # A balanced oracle is a function that returns 1 for half of the inputs and 0 for the other half
    # The oracle is implemented as a quantum circuit that performs a NOT operation on the second qubit
    # if the first qubit is 1

    #------- simple balanced func -----
    qc.cx(0, num_qubits)
    qc.cx(1, num_qubits)
    
    #------- random balanced func -----
    # Choose half the possible input strings    
    # on_states = np.random.choice(
    #     range(2**num_qubits),  # numbers to sample from
    #     2**num_qubits // 2,  # number of samples
    #     replace=False,  # makes sure states are only sampled once
    # )
    # for state in on_states:
    #     qc.barrier()  # Barriers are added to help visualize how the functions are created.
    #     qc = add_cx(qc, f"{state:0b}")
    #     qc.mcx(list(range(num_qubits)), num_qubits)
    #     qc = add_cx(qc, f"{state:0b}")
    # qc.barrier()
    
    #------another random balanced func ------
    # import random
    # controls = random.sample(range(num_qubits - 1),
    #                          random.randint(1, num_qubits))
    # print(controls)
    # for c in controls:
    #     qc.cx(c, num_qubits)

    return qc

def constant_oracle(qc: QuantumCircuit):
    # The oracle is implemented as a quantum circuit that performs a NOT operation on the second qubit
    # if the first qubit is 1
    # f.x(1)
    return qc


def dj_query(num_qubits):
    # Create a circuit implementing a query gate with a random function
    # satisfying the promise for the Deutsch-Jozsa problem.

    qc = QuantumCircuit(num_qubits + 1)
    if np.random.randint(0, 2):
        # Flip output qubit (ANCILLA) with 50% chance
        qc.x(num_qubits)
    if np.random.randint(0, 2):
        # return constant circuit with 50% chance
        print("calling constant oracle")
        return constant_oracle(qc)

    print("calling balanced oracle")
    qc = balanced_oracle(qc, num_qubits)
    return qc


def compile_circuit(function: QuantumCircuit):

    n = function.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)

    qc.x(n)
    qc.h(range(n + 1))

    qc.barrier()
    qc.compose(function, inplace=True)
    qc.barrier()

    qc.h(range(n))
    qc.measure(range(n), range(n))

    return qc


def dj_algorithm(function: QuantumCircuit):
    # Determine if a function is constant or balanced.

    qc = compile_circuit(function)
    qc.draw("mpl")
    result = AerSimulator().run(qc, shots=1, memory=True).result()
    measurements = result.get_memory()
    if "1" in measurements[0]:
        return "balanced"
    return "constant"


# deutsch_function(3).draw(output="mpl")
qc = dj_query(3)
result = dj_algorithm(qc)
print(result)
plt.show()

# f = deutsch_function(4)
# print(deutsch_algorithm(f))