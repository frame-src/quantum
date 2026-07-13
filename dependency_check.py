# Dependencies checks:
import sys

import qiskit
import qiskit_aer
import qiskit_ibm_runtime

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