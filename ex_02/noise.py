import os
import sys

import qiskit_ibm_runtime
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import matplotlib.pyplot as plt


circ = QuantumCircuit(2)

circ.h(0)
circ.cx(0, 1)
circ.measure_all()

simulator = AerSimulator()
result = simulator.run(bell).result()

print(circ)
plot_histogram(result.get_counts(circ))
plt.show()


try:
    service = QiskitRuntimeService(channel='ibm_quantum_platform')
except Exception as e:
    print(f"\nFailed to load IBM Quantum account: {e}")
    print("Run save_account first. See setup instructions at the top of this file.")
    sys.exit(1)


backend = service.least_busy(
    operational=True,
    simulator=False,
    min_num_qubits=2
)
real_circuit = transpile(circ, backend)

try:
    sampler = Sampler(backend)
    job = sampler.run([real_circuit], shots=500)

    result = job.result()
    counts = result[0].data.c.get_counts()

except Exception as e:
    print(f"\nJob failed: {e}")
    sys.exit(1)


fig, axes = plt.subplots(1, 2, figsize=(12, 4))

plot_histogram(counts, ax=axes[0], title=f"{backend.name}")
plt.show()