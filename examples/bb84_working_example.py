# bb84_simulation.py
# FILEPATH: /c:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84/examples/bb84_simulation.py
# Standard library imports
import numpy as np
import matplotlib.pyplot as plt
import sys

# Third party imports
from qiskit import Aer
from qiskit_ibm_provider import IBMProvider

# Local application imports
sys.path.append("C:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84") #Path to src folder
from src.utils.bb84_protocol import bb84_protocol
from src.classical.error_correction import cascade_correct
from src.classical.key_validation import check_errors
from src.utils.xor_encryption import encrypt, decrypt

if __name__ == "__main__":

    # Define Backend
    #IBMProvider.save_account('API_Key', overwrite = True) # Access the IBM Quantum systems
    #provider = IBMProvider()
    #print("Stored account: ", provider.active_account())
    #backend = provider.get_backend('ibmq_qasm_simulator') # IBM Quantum Experience backend
    backend = Aer.get_backend('qasm_simulator') # Aer Simulator backend

    # Parameters
    num_qubits = 25
    noise_measurement = 0 
    eve = 0
    error_rate = 0.1

    # Run the BB84 protocol simulation
    alice_key, bob_key, eve_key = bb84_protocol(num_qubits, backend, noise_measurement, eve, error_rate) 

    # Output the results
    print("Alice's key: ", alice_key)
    print("Bob's key:   ", bob_key)
    check_errors(alice_key, bob_key, list(range(len(alice_key))))
    print("Eve's key:   ", eve_key)

    # Error correction
    bob_key_corrected = cascade_correct(alice_key, bob_key)
    print("Bob's corrected key: ", bob_key_corrected)
    check_errors(alice_key, bob_key_corrected, list(range(len(alice_key))))

    # Comunication Model 
    alice_message = "A super secret message"
    print("Alice's message: ", alice_message)
    alice_encrypted = encrypt(alice_message, str(alice_key))
    print("Alice's encrypted message: ", alice_encrypted)

    bob_decrypted = decrypt(alice_encrypted, str(bob_key_corrected))
    print("Bob's decrypted message: ", bob_decrypted)
