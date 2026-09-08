def sliding_window(arr, n, wndw):
    # Match public C logic: return the median of the sliding medians
    import statistics
    medians = []
    for i in range(n - wndw + 1):
        window = arr[i:i+wndw]
        medians.append(int(statistics.median(window)))
    return int(statistics.median(medians))

def test_sliding_window_edge_public():
    arr1 = [40,41,39,45,44]
    assert sliding_window(arr1, 5, 3) == 41

    arr2 = [33,33,33,33]
    assert sliding_window(arr2, 4, 2) == 33

    arr3 = [100,101,102,103,104]
    assert sliding_window(arr3, 5, 5) == 102

    arr4 = [10,20,30]
    assert sliding_window(arr4, 3, 2) == 20

    arr5 = [55,56,57,58,59,60]
    assert sliding_window(arr5, 6, 1) == 57

    print("Public sliding_window edge tests OK")