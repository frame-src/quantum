from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import numpy as np
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import MCXGate

NUM_QUBITS = 3
# def add_cx(qc, bit_string):
#     print("Bist string: ")
#     print(bit_string)
#     for qubit, bit in enumerate(reversed(bit_string)):
#         if bit == "1":
#             qc.x(qubit)
#     return qc
ORACLE_IS = 'BALANCED'

def balanced_oracle():
    # This function implements a balanced oracle for a given quantum circuit
    # A balanced oracle is a function that returns 1 for half of the inputs and 0 for the other half
    # The oracle is implemented as a quantum circuit that performs a NOT operation on the second qubit
    # if the first qubit is 1
    qc = QuantumCircuit(NUM_QUBITS + 1)

    #------- simple balanced func -----
    # for i in range(NUM_QUBITS):
    #     qc.cx(i, NUM_QUBITS)
    
    #------- random balanced func -----
    # Choose half the possible input strings    
    # on_states = np.random.choice(
    #     range(2**NUM_QUBITS),  # numbers to sample from
    #     2**NUM_QUBITS // 2,  # number of samples
    #     replace=False,  # makes sure states are only sampled once
    # )
    # def add_cx(qc_dj, bit_string):
    #     for qubit, bit in enumerate(reversed(bit_string)):
    #         if bit == "1":
    #             qc_dj.x(qubit)
    #     return qc_dj

    # for state in on_states:
    #     qc.barrier()  # Barriers are added to help visualize how the functions are created.
    #     qc = add_cx(qc, f"{state:0b}")
    #     qc.mcx(list(range(NUM_QUBITS)), NUM_QUBITS)
    #     qc = add_cx(qc, f"{state:0b}")
    # qc.barrier()
    
    #------another random balanced func ------
    # import random
    # controls = random.sample(range(NUM_QUBITS - 1),
    #                          random.randint(1, NUM_QUBITS))
    # print(controls)
    # for c in controls:
    #     qc.cx(c, NUM_QUBITS)

    return qc

def constant_oracle():
    # The oracle is implemented as a quantum circuit that performs a NOT operation on the second qubit
    # if the first qubit is 1
    # f.x(1)
    qc = QuantumCircuit(NUM_QUBITS + 1)
    return qc


def dj_query(num_qubits):
    # Create a circuit implementing a query gate with a random function
    # satisfying the promise for the Deutsch-Jozsa problem.

    qc = QuantumCircuit(num_qubits + 1)
    if np.random.randint(0, 2):
        # Flip output qubit (ANCILLA) with 50% chance
        qc.x(num_qubits)
    if ORACLE_IS == 'CONSTANT':
        oracle = constant_oracle()
    else:
        oracle = balanced_oracle()
    qc.compose(oracle, inplace=True)
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
    result = AerSimulator().run(qc, shots=500, memory=True).result()
    counts = result.get_counts(qc)
    plot_histogram(counts)
    print(counts)
    measured = max(counts, key=counts.get)
    print(measured)
    answer = ""
    for zero in measured:
        if zero != "0":
            answer = "1"
        else:
            answer = "0"
    print("CONSTANT") if answer == "0" else print("BALANCED")
    return qc


# deutsch_function(3).draw(output="mpl")
qc = dj_query(NUM_QUBITS)
result = dj_algorithm(qc)
print(result)
plt.show()

# f = deutsch_function(4)
# print(deutsch_algorithm(f))