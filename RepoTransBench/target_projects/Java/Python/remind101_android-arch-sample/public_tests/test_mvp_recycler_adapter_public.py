import unittest

class TestModel:
    def __init__(self, value):
        self.value = value

class TestPresenter:
    pass

class TestViewHolder:
    def __init__(self):
        self.bound = False
        self.unbound = False
        self.lastPresenter = None

    def bindPresenter(self, presenter):
        self.bound = True
        self.lastPresenter = presenter

    def unbindPresenter(self):
        self.unbound = True
        self.lastPresenter = None

class MvpRecyclerAdapter:
    def __init__(self):
        self.presenters = dict()

    def getPresenter(self, model):
        pid = self.getModelId(model)
        if pid not in self.presenters:
            self.presenters[pid] = self.createPresenter(model)
        return self.presenters[pid]

    def createPresenter(self, model):
        raise NotImplementedError

    def getModelId(self, model):
        raise NotImplementedError

    def getItem(self, position):
        raise NotImplementedError

    def onBindViewHolder(self, holder, position):
        holder.bindPresenter(self.getPresenter(self.getItem(position)))

    def onViewRecycled(self, holder):
        holder.unbindPresenter()

    def onFailedToRecycleView(self, holder):
        holder.unbindPresenter()
        return False

class TestAdapter(MvpRecyclerAdapter):
    def __init__(self, *items):
        super().__init__()
        self.items = items
        for m in self.items:
            self.presenters[self.getModelId(m)] = self.createPresenter(m)

    def createPresenter(self, model):
        return TestPresenter()

    def getModelId(self, model):
        return model.value

    def getItem(self, position):
        return self.items[position]

class TestMvpRecyclerAdapterPublic(unittest.TestCase):
    def testBindAndUnbindPresenterWithDifferentModelData(self):
        model = TestModel(100)
        adapter = TestAdapter(model)
        holder = TestViewHolder()
        adapter.onBindViewHolder(holder, 0)
        self.assertTrue(holder.bound)
        self.assertIsNotNone(holder.lastPresenter)
        adapter.onViewRecycled(holder)
        self.assertTrue(holder.unbound)
        self.assertIsNone(holder.lastPresenter)

    def testOnFailedToRecycleViewCallsUnbindWithDifferentModel(self):
        model = TestModel(997)
        adapter = TestAdapter(model)
        holder = TestViewHolder()
        result = adapter.onFailedToRecycleView(holder)
        self.assertTrue(holder.unbound)

if __name__ == "__main__":
    unittest.main()