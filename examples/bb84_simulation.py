# bb84_simulation.py
# import functions in src
import sys
sys.path.append('C:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84')  # Ensure src is in the PYTHONPATH
from src.quantum.qubit_operations import random_basis, prepare_single_qubit_circuit, measure_qubit_in_basis
from src.classical.key_validation import compare_bases, check_errors
from qiskit import Aer, execute
import random

def bb84_protocol(num_qubits):
    # Step 1: Alice generates her random bits and bases
    alice_bits = [random.choice([0, 1]) for _ in range(num_qubits)]
    alice_bases = random_basis(num_qubits)

    # Step 2: Alice prepares qubits based on her bits and bases and sends them to Bob
    alice_qubits = [prepare_single_qubit_circuit(bit, basis) for bit, basis in zip(alice_bits, alice_bases)]

    # Step 3: Bob generates his random bases and measures the received qubits
    bob_bases = random_basis(num_qubits)
    bob_measurements = []
    for qubit, basis in zip(alice_qubits, bob_bases):
        measured_qubit = measure_qubit_in_basis(qubit, basis)
        # Simulate the measurement
        backend = Aer.get_backend('qasm_simulator')
        result = execute(measured_qubit, backend, shots=1).result()
        counts = result.get_counts(measured_qubit)
        measured_bit = max(counts, key=counts.get)
        bob_measurements.append(int(measured_bit))

    # Step 4: Alice and Bob compare their bases
    matching_bases = compare_bases(alice_bases, bob_bases)

    # Step 5: Alice and Bob extract the key
    alice_key = [alice_bits[i] for i in matching_bases]
    bob_key = [bob_measurements[i] for i in matching_bases]

    # Optionally, check for errors in the key
    #error_free = check_errors(alice_key, bob_key, matching_bases)
    #if not error_free:
    #    print("Error detected in the key. Abort the protocol.")
    #    return None, None

    return alice_key, bob_key

# Number of qubits to be used for the key
num_qubits = 10

# Run the BB84 protocol simulation
alice_key, bob_key = bb84_protocol(num_qubits)

# Output the results
print("Alice's key: ", alice_key)
print("Bob's key:   ", bob_key)