def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        for j in range(n - i - 1):
            # 1. Announces a comparison BEFORE checking it
            yield {"array": arr.copy(), "comparing": [j, j+1], "swapped": [], "sorted_idx": list(range(n-i, n))}

            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                # 2. Announces the swap AFTER it happens
                yield {"array": arr.copy(), "comparing": [], "swapped": [j, j+1], "sorted_idx": list(range(n-i, n))}

    # final state: everything sorted
    yield {"array": arr.copy(), "comparing": [], "swapped": [], "sorted_idx": list(range(n))}