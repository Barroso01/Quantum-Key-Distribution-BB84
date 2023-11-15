# error_correction_tests.py
# FILEPATH: /c:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84/tests/error_correction_tests.py

# Standard library imports
import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import random

# Local application imports
sys.path.append("C:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84") #Path to src folder
from src.classical.error_correction import cascade_correct
from src.classical.key_validation import check_errors

# Main function to test the cascade correction function
def test_cascade(a_key, b_key, number_errors):
    """
    Test the cascade correction function.

    Args:
        a_key (list): Alice's key.
        b_key (list): Bob's key.
        number_errors (int): The number of errors b_key has compared to a_key

    Returns:
        int: The efficiency of the error correction.
        int: The error correction rate. errors/second
    """

    # Correct the key
    time_start = time.time()
    b_key = cascade_correct(a_key, b_key, max_iterations=50)
    time_end = time.time()

    # Calculate efficiency indicators
    errors_inx,_ = check_errors(a_key, b_key, list(range(len(a_key))))
    print("Number or new errors: ", len(errors_inx))
    efficiency = (number_errors - len(errors_inx))/number_errors # Efficiency
    if time_end - time_start == 0: # Error correction rate
        error_correction_rate = 0
    else:
        error_correction_rate =  (number_errors - len(errors_inx))/(time_end - time_start)

    return efficiency, error_correction_rate

# Test the cascade correction function
if __name__ == "__main__":
    # Parameters
    k_len=100
    number_errors = 10 # Number of errors in Bob's key
    index_errors = random.sample(range(k_len), number_errors)

    key_1 = np.random.randint(2, size=k_len) # Initialize Alice's key
    key_2 = key_1.copy() # Initialize Bob's key
    for i in index_errors: #Random Errors
        key_2[i] = 1 - key_2[i] #Bob's key (with errors)

    check_errors(key_1, key_2, list(range(len(key_1)))) # Check errors before correction

    eff, err = test_cascade(key_1, key_2, number_errors) # Test the cascade correction function
    print("Efficiency: ", eff)
    print("Error correction rate: ", err, " errors/second")

    pass