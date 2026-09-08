import unittest

class DummyModel:
    def __init__(self, id):
        self.id = id

class DummyPresenter:
    pass

class DummyViewHolder:
    def __init__(self, itemView):
        self.itemView = itemView
        self.presenter = None
        self.wasBound = False
        self.wasUnbound = False

    def bindPresenter(self, presenter):
        self.presenter = presenter
        self.wasBound = True

    def unbindPresenter(self):
        self.presenter = None
        self.wasUnbound = True

class MvpRecyclerAdapter:
    def __init__(self):
        self.presenters = dict()
    def getPresenter(self, model):
        pid = self.getModelId(model)
        if pid not in self.presenters:
            self.presenters[pid] = self.createPresenter(model)
        return self.presenters[pid]
    def getModelId(self, model):
        raise NotImplementedError
    def createPresenter(self, model):
        raise NotImplementedError
    def getItem(self, position):
        raise NotImplementedError
    def getItemCount(self):
        raise NotImplementedError
    def onBindViewHolder(self, holder, position):
        holder.bindPresenter(self.getPresenter(self.getItem(position)))
    def onViewRecycled(self, holder):
        holder.unbindPresenter()
    def onFailedToRecycleView(self, holder):
        holder.unbindPresenter()
        return False

class DummyAdapter(MvpRecyclerAdapter):
    def __init__(self):
        super().__init__()
        self.models = [DummyModel(1), DummyModel(2)]
        for m in self.models:
            self.presenters[self.getModelId(m)] = self.createPresenter(m)
    def createPresenter(self, model):
        return DummyPresenter()
    def getModelId(self, model):
        return model.id
    def getItem(self, position):
        return self.models[position]
    def getItemCount(self):
        return len(self.models)

class TestMvpRecyclerAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = DummyAdapter()

    def testGetPresenterReturnsCorrectPresenter(self):
        m = DummyModel(1)
        p = self.adapter.getPresenter(m)
        self.assertIsNotNone(p)

    def testOnBindViewHolderBindsPresenter(self):
        holder = DummyViewHolder(object())
        self.adapter.onBindViewHolder(holder, 0)
        self.assertTrue(holder.wasBound)

    def testOnViewRecycledUnbindsPresenter(self):
        holder = DummyViewHolder(object())
        self.adapter.onViewRecycled(holder)
        self.assertTrue(holder.wasUnbound)

    def testOnFailedToRecycleViewUnbindsPresenter(self):
        holder = DummyViewHolder(object())
        returned = self.adapter.onFailedToRecycleView(holder)
        self.assertTrue(holder.wasUnbound)
        self.assertFalse(returned)

if __name__ == "__main__":
    unittest.main()