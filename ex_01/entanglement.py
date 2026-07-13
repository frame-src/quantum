from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

import matplotlib.pyplot as plt


# Let's make a entangled State, called a Bell state, using 2 qubits
# We use an Hadamard gate (H) to put the first qubit into an equal superposition.
# Then we apply a CX (controlled-NOT) gate, which entangles the two states together.
# As last step we measure the state of the two qubits

bell = QuantumCircuit(2)
bell.h(0)

bell.cx(0, 1)
bell.measure_all()

bell.draw("mpl")

simulator = AerSimulator()
result = simulator.run(bell, shots=500).result()

# plot the result
plot_histogram(result.get_counts(bell))
plt.show()


# https://quantum.cloud.ibm.com/learning/en/courses/use-a-qc-today/build-and-run-your-first-quantum-program