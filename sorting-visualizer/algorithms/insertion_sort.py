def insertion_sort(arr):
    arr = arr.copy()
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        # Compare key with elements on the left
        while j >= 0:
            yield {
                "array": arr.copy(),
                "comparing": [j, i],
                "swapped": [],
                "sorted_idx": list(range(i))
            }

            if arr[j] > key:
                # Shift element to the right
                arr[j + 1] = arr[j]

                yield {
                    "array": arr.copy(),
                    "comparing": [],
                    "swapped": [j, j + 1],
                    "sorted_idx": list(range(i))
                }

                j -= 1
            else:
                break

        # Insert key into correct position
        arr[j + 1] = key

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