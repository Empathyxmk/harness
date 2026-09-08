import pytest
import math
from src.finminexcept_tabu import finminexceptTabu

def test_finminexcepttabu_basic():
    graph = [
        [0, 5, 2],
        [5, 0, 1],
        [2, 1, 0]
    ]
    k = 1
    tabu = []
    val, idx = finminexceptTabu(graph[k-1], tabu)
    assert val == 2
    assert idx == 3

    k = 1
    tabu = [3]
    val, idx = finminexceptTabu(graph[k-1], tabu)
    assert val == 5
    assert idx == 2

    k = 2
    tabu = [1]
    val, idx = finminexceptTabu(graph[k-1], tabu)
    assert val == 1
    assert idx == 3

def test_finminexcepttabu_all_tabu():
    graph = [
        [0, 5, 2],
        [5, 0, 1],
        [2, 1, 0]
    ]
    k = 1
    tabu = [2, 3]
    val, idx = finminexceptTabu(graph[k-1], tabu)
    assert val == math.inf
    assert idx == 0

def test_finminexcepttabu_no_edges():
    graph = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    k = 1
    tabu = []
    val, idx = finminexceptTabu(graph[k-1], tabu)
    assert val == math.inf
    assert idx == 0

def test_finminexcepttabu_self_loop_ignored():
    graph = [
        [1, 5, 2],
        [5, 0, 1],
        [2, 1, 0]
    ]
    k = 1
    tabu = []
    val, idx = finminexceptTabu(graph[k-1], tabu)
    assert val == 2
    assert idx == 3

def test_finminexcepttabu_all_inf_or_zero():
    graph = [
        [math.inf, 0, math.inf],
        [0, math.inf, 0],
        [math.inf, 0, math.inf]
    ]
    k = 1
    tabu = []
    val, idx = finminexceptTabu(graph[k-1], tabu)
    assert val == math.inf
    assert idx == 0