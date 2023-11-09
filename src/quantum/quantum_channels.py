# quantum_channels.py
# FILEPATH: /c:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84/src/quantum/quantum_channels.py

# Standard library imports
import random
import sys
import matplotlib.pyplot as plt

# Third party imports
from qiskit import execute, Aer, IBMQ
from qiskit.providers.aer.noise import NoiseModel
from qiskit.visualization import plot_histogram

# Local application imports
sys.path.append("C:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84") #Path to src folder
from src.quantum.qubit_operations import prepare_single_qubit_circuit # import functions in src

def simulate_noise_measurement(qc, backend):
    """
    Simulates noise on a quantum circuit (qc) using a noise model from a backend. Returns counts of the simulation
     
    Args:
        qc (QuantumCircuit): The quantum circuit to which the measurement will be added.
        backend (str): The backend to be used for the simulation.

    Returns:
        counts (dict): The counts of the simulation. Example {'0': 1 , '1': 0 }

    """
    noise_model = NoiseModel.from_backend(backend) # Get noise model from backend
    coupling_map = backend.configuration().coupling_map   # Get coupling map from backend
    basis_gates = noise_model.basis_gates # Get basis gates from noise model

    # Perform a noise simulation
    result = execute(qc, backend , shots=1,
                     noise_model=noise_model,
                     coupling_map=coupling_map,
                     basis_gates=basis_gates).result() # Simulate measurement
    counts = result.get_counts()

    return counts

def evesdropper(qc):
    """
    Simulate an eavesdropper measuring incoming qubit in random basis, storing its value and returning a new quibit in the measured state. 
    
    Args: 
        qc (QuantumCircuit): The quantum circuit to which the measurement will be added.

    Returns:
        qc_eve (QuantumCircuit): The quantum circuit with the added measurement.
        eve_bit (int): The value of the measured qubit.
    """
    eavesdropper_basis = random.choice(['X', 'Z']) # Random basis for measurement
    if eavesdropper_basis == 'X':
        qc.h(0) # If basis is X, apply Hadamard gate before measurment
    qc.measure(0, 0)
    result = execute(qc, Aer.get_backend('qasm_simulator'), shots =1).result() # Simulate measurement
    eve_bit = int(max(result.get_counts(), key=result.get_counts().get)) # Get the value of the measured qubit
    qc_eve = prepare_single_qubit_circuit(eve_bit, eavesdropper_basis) # Prepare a new qubit in the measured state
   
    return qc_eve, eve_bit

def introduce_errors(qc, error_rate):
    """Introduce random errors into a quantum circuit.
    
    Args:
        qc (QuantumCircuit): The quantum circuit to which the measurement will be added.
        error_rate (float): The probability (between 0/1) of an error being introduced to the system before recipient measurement.

    Returns:
        qc (QuantumCircuit): The quantum circuit with the added measurement.
    """
    for qubit_index in range(qc.num_qubits):
        if random.random() < error_rate:
            qc.x(qubit_index) # Apply a random error (bit-flip, phase-flip, etc.)
            pass
    return qc