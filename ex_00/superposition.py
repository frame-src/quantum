from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit import transpile

# IBM Runtime specific imports
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService

# Dependencies checks:
import sys

import qiskit
import qiskit_aer
import qiskit_ibm_runtime
import matplotlib.pyplot as plt


circ = QuantumCircuit(1)
# H gate on qubit 0, putting this qubit in a superposition of |0> + |1>.
circ.h(0)
circ.measure_all()
circ.draw(output = 'mpl')

simulator = AerSimulator()

# circ = transpile(circ, simulator)
result = simulator.run(circ, shots=500).result()
counts = result.get_counts()
probs = {k: v/sum(counts.values()) for k, v in counts.items()}
plot_histogram(probs)
plt.show()
