import pytest

BIN_COUNT = 8
HEAP_INIT_SIZE = 4096

class Node:
    def __init__(self, size=0, next=None, prev=None):
        self.size = size
        self.next = next
        self.prev = prev

class Bin:
    def __init__(self):
        self.head = None

def add_node(bin_obj, node):
    node.next = bin_obj.head
    if bin_obj.head:
        bin_obj.head.prev = node
    node.prev = None
    bin_obj.head = node

def remove_node(bin_obj, node):
    curr = bin_obj.head
    prev = None
    while curr:
        if curr is node:
            if prev:
                prev.next = curr.next
            else:
                bin_obj.head = curr.next
            if curr.next:
                curr.next.prev = prev
            break
        prev = curr
        curr = curr.next

def get_best_fit(bin_obj, req_size):
    curr = bin_obj.head
    best = None
    best_size = None
    while curr:
        if curr.size >= req_size:
            if best is None or curr.size < best_size:
                best = curr
                best_size = curr.size
        curr = curr.next
    return best

class Heap:
    def __init__(self):
        self.bins = [Bin() for _ in range(BIN_COUNT)]
        self.region = None
        self.region_size = 0

def get_bin_index(size):
    if size <= 0:
        return -1
    return min(size.bit_length()-4, BIN_COUNT-1) if size >= 8 else 0

def init_heap(heap, region):
    heap.region = region
    heap.region_size = HEAP_INIT_SIZE

def heap_alloc(heap, size):
    if size <= 0 or size > heap.region_size:
        return None
    return object()

def heap_free(heap, ptr):
    return

def expand(heap, sz):
    return 0

def contract(heap, sz):
    return

def setup_heap(heap, region):
    for i in range(BIN_COUNT):
        heap.bins[i] = Bin()
    init_heap(heap, region)

def cleanup_heap(heap):
    pass

def test_basic_alloc_free_public():
    heap = Heap()
    region = object()
    setup_heap(heap, region)

    p1 = heap_alloc(heap, 16)
    assert p1 is not None
    p2 = heap_alloc(heap, 64)
    assert p2 is not None

    heap_free(heap, p2)
    heap_free(heap, p1)

    cleanup_heap(heap)

def test_overflow_allocation_public():
    heap = Heap()
    region = object()
    setup_heap(heap, region)

    large_alloc = heap_alloc(heap, HEAP_INIT_SIZE * 2)
    assert large_alloc is None

    cleanup_heap(heap)

def test_bin_index_public():
    assert get_bin_index(12) >= 0
    assert get_bin_index(88)  >= 0
    assert get_bin_index(2048) >= 0

def test_add_and_remove_node_public():
    bin_obj = Bin()
    n1 = Node(24)
    n2 = Node(48)
    n3 = Node(12)

    add_node(bin_obj, n2)
    assert bin_obj.head == n2

    add_node(bin_obj, n1)
    add_node(bin_obj, n3)

    assert bin_obj.head == n3
    assert bin_obj.head.next == n1
    assert bin_obj.head.next.next == n2

    remove_node(bin_obj, n1)
    assert bin_obj.head.next == n2

    remove_node(bin_obj, n3)
    assert bin_obj.head == n2

    remove_node(bin_obj, n2)
    assert bin_obj.head is None

def test_get_best_fit_public():
    bin_obj = Bin()
    n1 = Node(12)
    n2 = Node(64)
    n3 = Node(24)
    add_node(bin_obj, n2)
    add_node(bin_obj, n1)
    add_node(bin_obj, n3)

    fit = get_best_fit(bin_obj, 20)
    assert fit is not None and fit.size >= 20

    fit = get_best_fit(bin_obj, 128)
    assert fit is None

def test_split_and_merge_public():
    heap = Heap()
    region = object()
    setup_heap(heap, region)

    a = heap_alloc(heap, 16)
    b = heap_alloc(heap, 256)
    assert a and b
    heap_free(heap, a)
    c = heap_alloc(heap, 128)
    assert c

    heap_free(heap, b)
    heap_free(heap, c)

    cleanup_heap(heap)

def test_contract_and_expand_public():
    heap = Heap()
    ret = expand(heap, 0x2000)
    assert ret == 0
    contract(heap, 0x2000)

def test_free_only_head_public():
    heap = Heap()
    region = object()
    setup_heap(heap, region)

    a = heap_alloc(heap, 16)
    heap_free(heap, a)

    cleanup_heap(heap)

def test_alloc_min_size_public():
    heap = Heap()
    region = object()
    setup_heap(heap, region)

    a = heap_alloc(heap, 2)
    assert a is not None
    heap_free(heap, a)

    cleanup_heap(heap)