# src/classical/error_correction.py
# Standard library imports
import random

def calculate_parity(bits):
    return sum(bits) % 2

def shuffle_bits(bits):
    indices = list(range(len(bits)))
    random.shuffle(indices)
    return [bits[i] for i in indices], indices

def unshuffle_bits(shuffled_bits, indices):
    unshuffled_bits = [0] * len(shuffled_bits)
    for i, idx in enumerate(indices):
        unshuffled_bits[idx] = shuffled_bits[i]
    return unshuffled_bits

def verify_errors(alice_bits, bob_bits, corrected_indices):
    # Verify the corrected bits by checking the parity of blocks containing these bits
    for index in corrected_indices:
        block_start = max(0, index - 1)  # Check the bit itself and at least one neighbor
        block_end = min(len(bob_bits) - 1, index + 1)
        parity_alice = calculate_parity(alice_bits[block_start:block_end+1])
        parity_bob = calculate_parity(bob_bits[block_start:block_end+1])
        if parity_alice != parity_bob:
            return False  # Mismatch found, error verification failed
    return True  # All corrected bits verified

def perform_bisection(alice_bits, bob_bits, indices, start, end, corrected_indices):
    """
    One of bob_bits gets corrected a single call and returns True, otherwise returns False.
    The list of corrected indices is passed as a set to avoid correcting the same bit twice.
    The correction is a bit flip to restore parity between Alice and Bob's bits at start == end conditioned index.
    Args:
        alice_bits (list): Alice's bits.
        bob_bits (list): Bob's bits.
        indices (list): The indices of Bob's bits in the original order.
        start (int): The start index of the current bisection.
        end (int): The end index of the current bisection.
        corrected_indices (set): The set of indices that have already been corrected.
    Returns:
        bool: Whether an error was corrected.
    """
    if start == end: # Base case
        if indices[start] in corrected_indices:
            print("error found twice")
            return False
        bob_bits[start] = 1 - bob_bits[start]  # Flip the bit in Bob's shuffled bits
        corrected_indices.add(indices[start])   # Add the original index to the set of corrected indices
        print("corrected indeces: ", corrected_indices)
        return True
    mid = (start + end) // 2
    error_corrected = False
    # Use list comprehension to calculate parities using the correct indices
    parity_alice_left = sum(alice_bits[indices[i]] for i in range(start, mid+1)) % 2
    parity_bob_left = sum(bob_bits[i] for i in range(start, mid+1)) % 2
    if parity_alice_left != parity_bob_left:
        error_corrected |= perform_bisection(alice_bits, bob_bits, indices, start, mid, corrected_indices)
    parity_alice_right = sum(alice_bits[indices[i]] for i in range(mid + 1, end+1)) % 2
    parity_bob_right = sum(bob_bits[i] for i in range(mid + 1, end+1)) % 2
    if parity_alice_right != parity_bob_right:
        error_corrected |= perform_bisection(alice_bits, bob_bits, indices, mid + 1, end, corrected_indices)
    return error_corrected

def cascade_correct(alice_bits, bob_bits, max_iterations=50):
    corrected_indices = set()
    iterations = 0
    no_correction_counter = 0

    while iterations < max_iterations:
        iterations += 1
        shuffled_bob_bits, current_shuffle_indices = shuffle_bits(bob_bits)
        # current_shuffle_indices[i] is the original index of the bit now at position i

        error_corrected = perform_bisection(
            alice_bits,
            shuffled_bob_bits,
            current_shuffle_indices,  # Pass the current shuffled indices
            0,
            len(shuffled_bob_bits) - 1,
            corrected_indices
        )

        # Use the inverse of the current shuffle to put bits back in original order
        for i, orig_index in enumerate(current_shuffle_indices):
            bob_bits[orig_index] = shuffled_bob_bits[i]

        if error_corrected:
            if not verify_errors(alice_bits, bob_bits, corrected_indices):
                raise ValueError("Error verification failed, corrected bits do not match.")
            no_correction_counter = 0  # Reset counter if a correction was made
        else:
            no_correction_counter += 1  # Increment counter if no correction was made

        if no_correction_counter > 200:
            # If no errors were corrected in 200 consecutive iterations, stop the algorithm
            break

    return bob_bits

# Correct usage example, provided alice_bits and bob_bits are defined:
# corrected_bob_bits = cascade_correct(alice_bits, bob_bits)