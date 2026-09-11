def selection_sort(arr):
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):

            yield {
                "array": arr.copy(),
                "comparing": [j, min_idx],
                "swapped": [],
                "sorted_idx": list(range(i))
            }

            if arr[j] < arr[min_idx]:
                min_idx = j
                yield {
                    "array": arr.copy(),
                    "comparing": [min_idx],
                    "swapped": [],
                    "sorted_idx": list(range(i))
                }

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

            yield {
                "array": arr.copy(),
                "comparing": [],
                "swapped": [i, min_idx],
                "sorted_idx": list(range(i))
            }
        yield {
            "array": arr.copy(),
            "comparing": [],
            "swapped": [],
            "sorted_idx": list(range(i + 1))
        }

    yield {
        "array": arr.copy(),
        "comparing": [],
        "swapped": [],
        "sorted_idx": list(range(n))
    }