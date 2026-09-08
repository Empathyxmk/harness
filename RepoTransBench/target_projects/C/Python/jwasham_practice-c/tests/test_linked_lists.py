import pytest

class ForwardList:
    def __init__(self):
        self.list = []

    def size(self):
        return len(self.list)

    def push_front(self, val):
        self.list.insert(0, val)

    def empty(self):
        return int(len(self.list) == 0)

    def front(self):
        return self.list[0]

    def back(self):
        return self.list[-1]

    def pop_front(self):
        self.list.pop(0)

    def push_back(self, val):
        self.list.append(val)

    def pop_back(self):
        self.list.pop()

    def value_at(self, index):
        return self.list[index]

    def insert(self, index, val):
        self.list.insert(index, val)

    def erase(self, index):
        self.list.pop(index)

    def value_n_from_end(self, n):
        return self.list[-n]

    def reverse(self):
        self.list.reverse()

    def remove(self, val):
        self.list.remove(val)

def test_size():
    tester = ForwardList()
    assert tester.size() == 0
    tester.push_front(12)
    assert tester.size() == 1

def test_push_front():
    tester = ForwardList()
    assert tester.size() == 0
    tester.push_front(6)
    assert tester.size() == 1
    tester.push_front(11)
    tester.push_front(45)
    assert tester.size() == 3

def test_empty():
    tester = ForwardList()
    assert tester.empty() == 1
    tester.push_front(63)
    assert tester.empty() == 0
    tester.push_front(3)
    assert tester.empty() == 0

def test_front():
    tester = ForwardList()
    tester.push_front(121)
    assert tester.front() == 121
    tester.push_front(44)
    assert tester.front() == 44

def test_back():
    tester = ForwardList()
    tester.push_front(121)
    assert tester.back() == 121
    tester.push_front(44)
    assert tester.back() == 121

def test_pop_front():
    tester = ForwardList()
    tester.push_front(50)
    tester.push_front(100)
    assert tester.front() == 100
    tester.pop_front()
    assert tester.front() == 50

def test_push_back():
    tester = ForwardList()
    tester.push_front(99)
    tester.push_front(13)
    assert tester.back() == 99
    tester.push_back(500)
    assert tester.back() == 500

def test_pop_back():
    tester = ForwardList()
    tester.push_back(16)
    tester.push_back(84)
    assert tester.back() == 84
    tester.pop_back()
    assert tester.back() == 16
    assert tester.size() == 1
    tester.push_back(100)
    tester.push_back(200)
    assert tester.size() == 3
    tester.pop_back()
    assert tester.back() == 100
    assert tester.size() == 2
    tester.pop_back()
    tester.pop_back()
    assert tester.empty()

def test_value_at():
    tester = ForwardList()
    tester.push_back(1)
    tester.push_back(2)
    tester.push_back(3)
    assert tester.value_at(0) == 1
    assert tester.value_at(1) == 2
    assert tester.value_at(2) == 3

def test_insert():
    tester = ForwardList()
    tester.insert(0, 5)
    assert tester.size() == 1
    assert tester.value_at(0) == 5
    tester.insert(0, 3)
    assert tester.value_at(0) == 3
    assert tester.value_at(1) == 5
    tester.insert(1, 4)
    assert tester.value_at(0) == 3
    assert tester.value_at(1) == 4
    assert tester.value_at(2) == 5
    tester.push_front(20)
    tester.push_front(10)
    tester.insert(2, 2)
    assert tester.value_at(2) == 2
    assert tester.value_at(3) == 3

def test_erase():
    tester = ForwardList()
    tester.push_front(5)
    tester.erase(0)
    assert tester.size() == 0
    tester.push_back(1)
    tester.push_back(2)
    tester.erase(0)
    assert tester.value_at(0) == 2
    tester.push_back(3)
    tester.erase(1)
    assert tester.value_at(0) == 2
    tester.push_back(3)
    tester.push_back(4)
    tester.erase(2)
    assert tester.value_at(1) == 3

def test_value_n_from_end():
    tester = ForwardList()
    tester.push_back(123)
    tester.push_back(623)
    tester.push_back(987)
    tester.push_back(629)
    tester.push_back(812)
    tester.push_back(238)
    assert tester.value_n_from_end(4) == 987
    assert tester.value_n_from_end(2) == 812
    assert tester.value_n_from_end(6) == 123
    # single item list
    tester2 = ForwardList()
    tester2.push_back(999)
    assert tester2.value_n_from_end(1) == 999

def test_reverse():
    tester = ForwardList()
    tester.push_back(2)
    tester.push_back(3)
    tester.push_back(5)
    tester.push_back(8)
    tester.push_back(11)
    tester.reverse()
    assert tester.value_at(0) == 11
    assert tester.value_at(1) == 8
    assert tester.value_at(2) == 5
    assert tester.value_at(3) == 3
    assert tester.value_at(4) == 2

def test_reverse_single():
    tester = ForwardList()
    tester.push_back(2)
    tester.reverse()
    assert tester.value_at(0) == 2

def test_reverse_empty():
    tester = ForwardList()
    tester.reverse()

def test_remove():
    tester = ForwardList()
    tester.push_back(2)
    tester.push_back(4)
    tester.push_back(6)
    tester.remove(6)
    assert tester.size() == 2
    assert tester.value_at(0) == 2
    assert tester.value_at(1) == 4
    assert tester.back() == 4
    tester.remove(2)
    assert tester.size() == 1
    assert tester.value_at(0) == 4
    tester.remove(4)
    assert tester.size() == 0