# qubit_operations.py
# FILEPATH: /c:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84/src/quantum/qubit_operations.py
# Standard library imports
import random

# Third party imports
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ
from qiskit.visualization import plot_histogram

def random_basis(length):
    """Generate a random basis sequence of 'X' and 'Z'."""
    return ''.join(random.choice(['X', 'Z']) for _ in range(length))

def prepare_single_qubit_circuit(qubit_value, basis):
    """
    Prepare a single-qubit circuit in the specified state and basis.
    
    Args:
        qubit_value (int): The desired qubit value (0 or 1).
        basis (str): The basis for the qubit ('Z' or 'X').
    
    Returns:
        QuantumCircuit: The prepared single-qubit circuit.
    
    Raises:
        ValueError: If qubit_value is not 0 or 1, or if basis is not 'Z' or 'X'.
    """
    if qubit_value not in [0, 1]:
        raise ValueError("qubit_value must be 0 or 1.")
    if basis not in ['Z', 'X']:
        raise ValueError("basis must be 'Z' or 'X'.")

    qc = QuantumCircuit(1, 1)
    if qubit_value == 1:
        qc.x(0)
    if basis == 'X':
        qc.h(0)

    return qc

def measure_qubit_in_basis(qc, basis):
    """
    Add a measurement to the quantum circuit in the specified basis.
    
    Args:
        qc (QuantumCircuit): The quantum circuit to which the measurement will be added.
        basis (str): The basis for the measurement ('Z' or 'X').
    
    Returns:
        QuantumCircuit: The quantum circuit with the added measurement.
    
    Raises:
        ValueError: If basis is not 'Z' or 'X'.
    """
    if basis not in ['Z', 'X']:
        raise ValueError("basis must be 'Z' or 'X'.")

    if basis == 'X':
        qc.h(0)
    qc.measure(0, 0) # 0 is the index of the qubit, 0 is the index of the classical bit
    return qc