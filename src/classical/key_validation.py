# key_validation.py
# FILEPATH: /c:/Users/6QV78LA_1909/OneDrive/Documents/Visual Studio/Quantum-Key-Distribution-BB84/src/classical/key_validation

def compare_bases(a_bases, b_bases):
    """
    Compare the bases used by Alice and Bob to encode and decode the qubits.

    Args:
        a_bases (list): List of bases used by Alice.
        b_bases (list): List of bases used by Bob.

    Returns:
        list: List of indices where Alice and Bob used the same basis.
    """
    matching_bases = []
    for i in range(len(a_bases)):
        if a_bases[i] == b_bases[i]:
            matching_bases.append(i)
    return matching_bases

def check_errors(a_key, b_key, check_bits):
    """
    Check for errors or eavesdropping by comparing the results obtained by Alice and Bob.
    Prints indices where errors were detected.

    Args:
        a_key (list): List of qubit values obtained by Alice.
        b_key (list): List of qubit values obtained by Bob.
        check_bits (list): List of keys indeces to check errors .

    Returns:
        bool: True if no errors or eavesdropping detected, False otherwise.
        list: List of indices where Alice and Bob had different results.
    """
    errors_inx = []
    for i in check_bits:
        if a_key[i] != b_key[i]:
            errors_inx.append(i)

    print("Errors in indeces: ", errors_inx)

    if len(errors_inx) > 0:
            return errors_inx, False
    return errors_inx, True