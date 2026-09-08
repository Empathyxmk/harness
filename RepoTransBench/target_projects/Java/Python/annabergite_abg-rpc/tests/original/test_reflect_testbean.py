class ReflectTestBean:
    def __init__(self):
        self.directUserAge = 18
        self.volatileUserAge = 26

    def getDirectUserAge(self, userId):
        return self.directUserAge

    def setDirectUserAge(self, userId, directUserAge):
        self.directUserAge = directUserAge

def test_reflect_testbean_methods():
    bean = ReflectTestBean()
    assert bean.getDirectUserAge(0) == 18
    bean.setDirectUserAge(0, 25)
    assert bean.getDirectUserAge(1) == 25