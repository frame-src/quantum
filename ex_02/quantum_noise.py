import sys
from os import getenv

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.visualization import plot_histogram

import matplotlib.pyplot as plt
from dotenv import load_dotenv

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
# IBM Runtime specific imports 
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService


def run_circuit_and_get_counts(circuit, backend, shots=1000):
    """
    Runs a quantum circuit on a specified backend and returns the measurement counts.

    Args:
        circuit (QuantumCircuit): The quantum circuit to run.
        backend: The Qiskit backend (real device or simulator).
        shots (int): The number of shots to run the circuit.

    Returns:
        dict: A dictionary of measurement counts.
    """
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    sampler = Sampler(mode=backend)

    job = sampler.run([isa_circuit], shots=shots)
    result = job.result()

    return result[0].data.meas.get_counts()


circ = QuantumCircuit(2)
circ.h(0)
circ.cx(0, 1)
circ.measure_all()

print(circ)

def service_login():
    load_dotenv()
    try:
        QiskitRuntimeService.save_account(
            token=getenv('IBM_QUANTUM_API_KEY'),
            channel="ibm_quantum_platform",
            overwrite=True,
            set_as_default=True)
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
        service = QiskitRuntimeService()
        # Load saved credentials


    except Exception as e:
        print(f"\nFailed to load IBM Quantum account: {e}")
        sys.exit(1)
    return service

service = service_login()
backend = service.least_busy(
    operational=True,
    simulator=False,
    min_num_qubits=127
)
print(backend.name)

bell = transpile(circ, backend)
counts = run_circuit_and_get_counts(bell, backend, shots=500)
plot_histogram(counts, title=f"{backend.name}")
plt.show()

# https://quantum.cloud.ibm.com/learning/en/courses/use-a-qc-today/build-and-run-your-first-quantum-program