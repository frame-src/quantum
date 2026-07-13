import math
import os

from qiskit import QuantumCircuit, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

os.makedirs("results", exist_ok=True)

# To apply Grover algorithm, we need to generate a random n-bit string;
# We need to put all the qubits on a superposition state. 
# To do so --> we apply an H gate to each qubit as we know.
# The Oracle does a simple things: It takes the target string and flips the phase of the state corresponding to the target.
# It basically put a minus sign in front of the target amplitude.

#Phase Query Gates

MAX_SHOTS = 500


def create_circuit_oracle(n, target):
    qc = QuantumCircuit(n)

    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(i)

    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(i)

    return qc


def create_circuit_diffuser(n):
    diff = QuantumCircuit(n)
    diff.h(range(n))
    diff.x(range(n))
    diff.h(n-1)
    diff.mcx(list(range(n-1)), n-1)
    diff.h(n-1)
    diff.x(range(n))
    diff.h(range(n))

    return diff


def grover(n, target):
    iterations = max(1, math.floor(math.pi / 4 * math.sqrt(2**n)))

    cr = ClassicalRegister(n, "result")
    qc = QuantumCircuit(n)
    qc.add_register(cr)
    # hadamart gate for superposition.
    for i in range(n):
        qc.h(i)
    qc.barrier()

    oracle = create_circuit_oracle(n, target)
    oracle_gate = oracle.to_gate()
    oracle_gate.name = f"Oracle {target}"
    diffuser = create_circuit_diffuser(n)
    diff_gate = diffuser.to_gate()
    diff_gate.name = f"Diffuser {target}"

    # let's add oracle and amp to the circuit, putting a barrier for readability
    for _ in range(iterations):
        qc.append(oracle_gate, range(n))
        qc.append(diff_gate, range(n))
        qc.barrier()

    qc.measure(range(n), range(n))
    return qc, iterations

def run_simulation(n, target):
    qc, iterations = grover(n, target)
    print("___________________________________________________________________________________________")
    print(f"Target      : {target}      |     Number ofQubits      : {n}      |  Iterations  : {iterations}")
    print("___________________________________________________________________________________________")


    simulator = AerSimulator()
    counts = simulator.run(
        transpile(qc, simulator),
        shots=MAX_SHOTS
    ).result().get_counts()

    top = max(counts, key=counts.get)
    probability = (counts[top] / MAX_SHOTS) * 100
    if top == target:
        print(f"Result      : |{top}⟩ -> (Found) ({probability:.1f}%)")

    else:
        print(f"Result      : |{top}⟩ -> (Not Found)")

    qc.draw("mpl")
    plt.title(f"Grover Circuit |{target}⟩")
    plt.savefig(f"results/grover_circuit_{target}.png")
    plt.show()

    plot_histogram(counts)
    plt.title(f"Grover Results |{target}⟩")
    plt.savefig(f"results/grover_histogram_{target}.png")
    plt.show()

    return counts

if __name__ == "__main__":
    print("Running Grover's Search Algorithm")
    examples = [
        (3, "001"),
        (3, "011"),
        (3, "101"),
        (3, "111"),
        (2, "10"),
        (4, "1010"),
    ]
    print(f"\n******************* GROVER SEARCH ALGORITHM *****************")

    for n, target in examples:
        if n == 2:
            print(f"___________________________________________________________________________________________\
                \nSkipping {n}-qubit because case (not supported)\n\
___________________________________________________________________________________________")
            continue
        run_simulation(n, target)