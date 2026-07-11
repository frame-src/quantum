from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# IBM Runtime specific imports
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService

# Dependencies checks:
import sys

import qiskit
import qiskit_aer
import qiskit_ibm_runtime
import matplotlib.pyplot as plt


def dependencies_check():
    print("Python:", sys.version.split()[0])
    print("qiskit:", qiskit.__version__)
    print("qiskit-aer:", qiskit_aer.__version__)
    print("qiskit-ibm-runtime:", qiskit_ibm_runtime.__version__)
    if qiskit.__version__ < "0.50.0":
        raise ImportError("qiskit>=0.50.0 is required")
    if qiskit_aer.__version__ < "0.15.0":
        raise ImportError("qiskit-aer>=0.15.0 is required")
    if qiskit_ibm_runtime.__version__ < "0.15.0":
        raise ImportError("qiskit-ibm-runtime>=0.15.0 is required")
    return True

dependencies_check()

# Let's make a entangled State, called a Bell state
# First we create a quantum circuit with 2 qubit
bell = QuantumCircuit(2)
# We use an Hadamard gate (H) to put the first qubit into an equal superposition.
bell.h(0)
# Then we apply a CX (controlled-NOT) gate, which entangles the two states together.
bell.cx(0, 1)
# We can now measure the state of the two qubits
bell.measure_all()

# Let's draw the circuit
bell.draw("mpl")
# Now we have to run the circuit on a simulator
simulator = AerSimulator()
result = simulator.run(bell).result()

# print(result)
# We can now plot the result
plot_histogram(result.get_counts(bell))
plt.show()


# https://quantum.cloud.ibm.com/learning/en/courses/use-a-qc-today/build-and-run-your-first-quantum-program