"""
This file contains the required Algorithms
with extra properities to calaculate 
comparisons , swaps , fields and returns
and more proper variable names to the project
"""

# O(n^2) - repeatedly swaps adjacent out-of-order pairs each pass
def bubble_sort(requests:list , field):
    n = len(requests)
    comparisons = 0
    swaps = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if requests[j][field] > requests[j + 1][field]:
                requests[j], requests[j + 1] = requests[j + 1], requests[j]
                swaps += 1
    return requests, comparisons, swaps , field


# O(n^2) - finds the min of the unsorted part and swaps it into place
def selection_sort(requests:list , field):
    n = len(requests)
    comparisons = 0
    swaps = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if requests[j][field] < requests[min_idx][field]:
                min_idx = j
        if min_idx != i:
            requests[i], requests[min_idx] = requests[min_idx], requests[i]
            swaps += 1
    return requests, comparisons, swaps , field


# O(n^2) worst case, faster on nearly-sorted data - shifts elements
# right to insert each key into its correct position
def insertion_sort(requests:list , field):
    n = len(requests)
    comparisons = 0
    shifts = 0
    for i in range(1, n):
        key = requests[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if requests[j][field] > key[field]:
                requests[j + 1] = requests[j]
                shifts += 1
                j -= 1
            else:
                break
        requests[j + 1] = key
    return requests, comparisons, shifts , field


# O(n) - checks records one by one, works on unsorted data
def sequential_search(requests:list, target_id , field):
    comparisons = 0
    # enumerate() gives (index, record) together so we don't need a separate counter
    for i, record in enumerate(requests): # i = index, record = the item itself
        comparisons += 1
        if record[field] == target_id:
            return {"found": True, "index": i, "comparisons": comparisons}
    return {"found": False, "index": -1, "comparisons": comparisons}


# O(log n) - requires sorted data; returns insert_position when not found
def binary_search(requests:list, target_id , field):
    low = 0
    high = len(requests) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if requests[mid][field] == target_id:
            return {"found": True, "index": mid, "comparisons": comparisons}
        elif requests[mid][field] < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return {"found": False, "insert_position": low, "comparisons": comparisons}
