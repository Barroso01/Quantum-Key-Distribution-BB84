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


def check_errors(a_results, b_results, matching_bases):
    """
    Check for errors or eavesdropping by comparing the results obtained by Alice and Bob.

    Args:
        a_results (list): List of qubit values obtained by Alice.
        b_results (list): List of qubit values obtained by Bob.
        matching_bases (list): List of indices where Alice and Bob used the same basis.

    Returns:
        bool: True if no errors or eavesdropping detected, False otherwise.
    """
    for i in matching_bases:
        if a_results[i] != b_results[i]:
            return False
    return True
