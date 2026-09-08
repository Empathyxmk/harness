class AllIntBean:
    def __init__(self):
        self.values = [0] * 32
    def setValue(self, idx, v):
        self.values[idx] = v
    def getValue(self, idx):
        return self.values[idx]

def test_unsafe_copy_simulation():
    bean = AllIntBean()
    for i in range(32):
        bean.setValue(i, i)
    assert bean.getValue(0) == 0
    assert bean.getValue(31) == 31

    # Simulate field addressw/offset logic
    bean2 = AllIntBean()
    # Simulate memory copy operation
    for i in range(32):
        bean2.setValue(i, bean.getValue(i))
    assert bean2.getValue(0) == 0
    assert bean2.getValue(1) == 1
    assert bean2.getValue(30) == 30
    assert bean2.getValue(31) == 31