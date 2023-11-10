# bb84_performance_test.py
# FILEPATH: /c:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84/tests/bb84_performance_test.py
# Standard library imports
import numpy as np
import matplotlib.pyplot as plt
import sys
import time

# Third party imports
from qiskit import Aer
from qiskit_ibm_provider import IBMProvider

# Local application imports
sys.path.append("C:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84") #Path to src folder
from src.utils.bb84_protocol import bb84_protocol

# Main function to run the BB84 protocol and calculate efficiency
def test_bb84_efficiency(num_qubits, backend, noise_measurement, eve, error_rate):
    """
    Run the BB84 protocol and calculate efficiency indicators.

    Args:
        num_qubits (int): The number of qubits to be used for the key.
        backend (str): The backend to be used for the simulation.
        noise_measurement (bool): Whether to simulate noise on the measurement.
        evesdrop (bool): Whether to simulate an eavesdropper.
        error_rate (float): The probability (between 0/1) of an error being introduced to the system before recipient measurement.

    Returns:
        float: Key Generation Rate.
        float: Quantum Bit Error Rate.
        int: Number of error bits.
        float: Total time.
        int: Length of the key.
    """

    # Start timing
    start_time = time.time()
    alice_key, bob_key, _ = bb84_protocol(num_qubits, backend, noise_measurement, eve, error_rate) 
    end_time = time.time()
    #print('Alice key: ', alice_key, '\nBob key: ', bob_key, '\nEve key: ', eve_key)

    # Efficiency indicators
    len_key = len(alice_key)
    error_bits = sum(alice_key[i] != bob_key[i] for i in range(len(bob_key)))
    total_time = end_time-start_time

    # Calculate efficiency indicators

    kgr = len_key/total_time #Key Generation Rate
    qber = error_bits/len_key #Quantum Bit Error Rate

    return kgr, qber, error_bits, total_time, len_key

# Run the efficiency test
if __name__ == "__main__":
    # Parameters
    backend = Aer.get_backend('qasm_simulator') # Aer Simulator backend
    num_qubits = 100
    noise_measurement = 0 
    eve = 0
    error_rate = 0.1

    # Initialize
    kgrs, qbers, key_lengths, errs, ts = ([] for _ in range(5))

    for i in range(1):
        kgr, qber, err, t, l = test_bb84_efficiency(num_qubits, backend, noise_measurement, eve, error_rate)
        kgrs.append(kgr)
        qbers.append(qber)
        key_lengths.append(l)
        errs.append(err)
        ts.append(t)
    
    print("With the Backend: ", backend, ", Noise:", noise_measurement, ", Evesdrop:", eve, ", Error rate:", error_rate, ", Qubits:", num_qubits, "; configurations. The test gives the following results:")
    print(f"BB48-Run Time: {np.mean(ts)} seconds, Key Length: {np.mean(key_lengths)} Error bits: {np.mean(err)}")
    print(f"KGR: {np.mean(kgrs)} bits/sec, QBER: {np.mean(qbers)} errorbits / keybits")