# FILEPATH: /c:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84/src/quantum/quantum_channels.py
import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer, IBMQ
from qiskit.visualization import plot_histogram
from qiskit.providers.aer.noise import NoiseModel
import matplotlib.pyplot as plt

def simulate_noise_measurement(qc):
    """Apply a noise model to a quantum circuit return counts"""
    provider = IBMQ.load_account()
    backend = provider.get_backend('ibmq_16_melbourne')
    noise_model = NoiseModel.from_backend(backend)
    
    # Get coupling map from backend
    coupling_map = backend.configuration().coupling_map

    # Get basis gates from noise model
    basis_gates = noise_model.basis_gates

    # Perform a noise simulation
    result = execute(qc, Aer.get_backend('qasm_simulator'),
                     noise_model=noise_model,
                     coupling_map=coupling_map,
                     basis_gates=basis_gates).result()
    counts = result.get_counts()
    plot_histogram(counts)
    plt.show()
    return counts

def eavesdrop(qc, qubit_index = 0):
    """Simulate an eavesdropper measuring a qubit."""
    eavesdropper_basis = random.choice(['X', 'Z'])
    if eavesdropper_basis == 'X':
        qc.h(qubit_index)
    qc.measure(qubit_index, 0)
    # After measurement apply Hadamard again if in X to "erase" the action if you want to ignore the eavesdropper effect
    if eavesdropper_basis == 'X':
        qc.h(qubit_index)
    return qc

def introduce_errors(qc, error_rate):
    """Introduce random errors into a quantum circuit."""
    for qubit_index in range(qc.num_qubits):
        if random.random() < error_rate:
            # Apply a random error (bit-flip, phase-flip, etc.)
            qc.x(qubit_index)
            pass
    return qc