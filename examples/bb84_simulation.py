# bb84_simulation.py
# FILEPATH: /c:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84/examples/bb84_simulation.py
# Standard library imports
import numpy as np
import matplotlib.pyplot as plt
import random
import sys

# Third party imports
from qiskit import Aer, IBMQ, execute
from qiskit_ibm_provider import IBMProvider

# Local application imports
sys.path.append("C:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84") #Path to src folder
from src.quantum.qubit_operations import random_basis, prepare_single_qubit_circuit, measure_qubit_in_basis # import functions in src
from src.quantum.quantum_channels import simulate_noise_measurement, introduce_errors, evesdropper
from src.classical.key_validation import compare_bases, check_errors

def bb84_protocol(num_qubits, backend =  Aer.get_backend('qasm_simulator'), noise_measurement = 0, evesdrop = 0, error_rate = 0):
    """
    Simulate the BB84 protocol for quantum key distribution. The user can choose backend, noise, evesdropper and error rate. 

    Args:
        num_qubits (int): The number of qubits to be used for the key.
        backend (str): The backend to be used for the simulation.
        noise_measurement (bool): Whether to simulate noise on the measurement.
        evesdrop (bool): Whether to simulate an eavesdropper.
        error_rate (float): The probability (between 0/1) of an error being introduced to the system before recipient measurement.

    Returns:
        list: Alice's key.
        list: Bob's key.
    
    """
    # Step 1: Alice generates her random bits and bases
    alice_bits = [random.choice([0, 1]) for _ in range(num_qubits)]
    alice_bases = random_basis(num_qubits)

    # Step 2: Alice prepares qubits based on her bits and bases and sends them to Bob
    alice_qubits = [prepare_single_qubit_circuit(bit, basis) for bit, basis in zip(alice_bits, alice_bases)]

    # Step 3: Bob generates his random bases and measures the received qubits
    bob_bases = random_basis(num_qubits)
    bob_measurements = []
    eve_measurements = []
    for qubit, basis in zip(alice_qubits, bob_bases):
        
        if evesdrop == 1: # Eavesdropper
            qubit, eve_bit  = evesdropper(qubit)
            eve_measurements.append(eve_bit)

        if error_rate > 0:
            qubit = introduce_errors(qubit, error_rate)

        measured_qubit = measure_qubit_in_basis(qubit, basis)

        if noise_measurement == 1:
            counts = simulate_noise_measurement(measured_qubit, backend)
        else:
            result = execute(measured_qubit, backend, shots =1).result()
            counts = result.get_counts()

        measured_bit = max(counts, key=counts.get) 
        bob_measurements.append(int(measured_bit))

    # Step 4: Alice and Bob compare their bases
    matching_bases = compare_bases(alice_bases, bob_bases)
    print("Matching bases: ", matching_bases)

    # Step 5: Alice and Bob extract the key
    alice_key = [alice_bits[i] for i in matching_bases]
    bob_key = [bob_measurements[i] for i in matching_bases]

    # Optionally, check for errors in the key
    error_free = check_errors(alice_key, bob_key, [0,1,2]) #Check first 3 bits
    if not error_free:
        print("Error detected in the key. Abort the protocol.")
    if error_free:
        print("No errors detected in the key.")

    return alice_key, bob_key

# Access the IBM Quantum systems
#IBMProvider.save_account('API_Key', overwrite = True)
#provider = IBMProvider()
#print("Stored account: ", provider.active_account())
#backend = provider.get_backend('ibmq_qasm_simulator') # IBM Quantum Experience backend
backend = Aer.get_backend('qasm_simulator') # Aer Simulator backend

# Number of qubits to be used for the key
num_qubits = 10

# Run the BB84 protocol simulation
alice_key, bob_key = bb84_protocol(num_qubits,backend,0,1,0.1)

# Output the results
print("Alice's key: ", alice_key)
print("Bob's key:   ", bob_key)