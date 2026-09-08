import pytest
import copy

# Simulate the Profile entity and its storage.
class DummyPrefs:
    def __init__(self):
        self.store = {}
    def edit(self):
        return self
    def putString(self, k, v):
        self.store[k] = v
        return self
    def putBoolean(self, k, v):
        self.store[k] = v
        return self
    def putInt(self, k, v):
        self.store[k] = v
        return self
    def apply(self):
        return True
    def getString(self, k, default=None):
        return self.store.get(k, default)
    def getBoolean(self, k, default=None):
        return self.store.get(k, default)
    def getInt(self, k, default=None):
        return self.store.get(k, default)

class PrivateInfo:
    def __init__(self, name='null', age=0):
        self.name = name
        self.age = age
    def getName(self):
        return self.name
    def getAge(self):
        return self.age

class Pet:
    def __init__(self, name, age, feed, color):
        self.name = name
        self.age = age
        self.feed = feed
        self.color = color
    def getName(self):
        return self.name
    def getAge(self):
        return self.age
    def isFeed(self):
        return self.feed
    def getColor(self):
        return self.color

class Preference_UserProfile:
    def __init__(self):
        self.preferences = DummyPrefs()
        self.nick = "skydoves!!!"
        self.login = False
        self.visits = 1
        self.userinfo = PrivateInfo()
        self.userpet = None
        self.keys = ['nickname', 'Login', 'visits', 'userinfo', 'userPet']
    @staticmethod
    def getInstance(context=None):
        return Preference_UserProfile()
    def clear(self):
        self.nick = "skydoves!!!"
        self.login = False
        self.visits = 1
        self.userinfo = PrivateInfo()
        self.userpet = None
        self.preferences = DummyPrefs()
    def nicknameKeyName(self): return "nickname"
    def LoginKeyName(self): return "Login"
    def visitsKeyName(self): return "visits"
    def userPetKeyName(self): return "userPet"
    def getEntityName(self): return "Preference_UserProfile"
    def getNickname(self):
        # getter function logic: append !!!
        return self.nick
    def getLogin(self):
        return self.login
    def getVisits(self):
        return self.visits
    def getUserinfo(self):
        return self.userinfo
    def getUserPet(self):
        return self.userpet
    def putNickname(self, v):
        # putter: "Hello, <v>!!!"
        self.nick = "Hello, " + v + "!!!"
        self.preferences.putString(self.nicknameKeyName(), v)
    def putLogin(self, v):
        self.login = v
        self.preferences.putBoolean(self.LoginKeyName(), v)
    def putVisits(self, v):
        self.visits = v + 1
        self.preferences.putInt(self.visitsKeyName(), v)
    def putUserinfo(self, info):
        self.userinfo = copy.deepcopy(info)
    def putUserPet(self, pet):
        self.userpet = copy.deepcopy(pet)
        # simulate gson serialization as string
        import json
        self.preferences.putString(self.userPetKeyName(), json.dumps({
            "name": pet.name, "age": pet.age, "feed": pet.feed, "color": pet.color,
        }))
    def getkeyNameList(self):
        return self.keys

@pytest.fixture(scope="function")
def profile():
    return Preference_UserProfile.getInstance()

def test_preference(profile):
    profile.clear()
    profile.preferences.putString(profile.nicknameKeyName(), "PreferenceRoom").apply()
    profile.preferences.putBoolean(profile.LoginKeyName(), True).apply()
    profile.preferences.putInt(profile.visitsKeyName(), 12).apply()
    assert profile.preferences.getString(profile.nicknameKeyName()) + "!!!" == profile.getNickname()
    assert profile.preferences.getBoolean(profile.LoginKeyName()) == profile.getLogin()
    assert profile.preferences.getInt(profile.visitsKeyName()) == profile.getVisits()

def test_default(profile):
    profile.clear()
    assert profile.getNickname() == "skydoves!!!"
    assert profile.getLogin() is False
    assert profile.getVisits() == 1
    assert profile.getUserinfo().getName() == "null"
    assert profile.getUserPet() is None

def test_put_preference(profile):
    profile.clear()
    profile.putNickname("PreferenceRoom")
    profile.putLogin(True)
    profile.putVisits(12)
    profile.putUserinfo(PrivateInfo("Jaewoong", 123))
    assert profile.getNickname() == "Hello, PreferenceRoom!!!"
    assert profile.getLogin() is True
    assert profile.getVisits() == 13
    assert profile.getUserinfo().getName() == "Jaewoong"
    assert profile.getUserinfo().getAge() == 123

def test_base_gson_converter(profile):
    import json
    WHITE = 0xFFFFFFFF
    pet = Pet("skydoves", 11, True, WHITE)
    profile.putUserPet(pet)
    s = profile.preferences.getString(profile.userPetKeyName())
    assert s is not None and len(s) > 0
    pet_dict = json.loads(s)
    assert pet_dict["name"] == "skydoves"
    assert pet_dict["age"] == 11
    assert pet_dict["feed"] is True
    assert pet_dict["color"] == WHITE
    gp = profile.getUserPet()
    assert gp.getName() == "skydoves"
    assert gp.getAge() == 11
    assert gp.isFeed() is True
    assert gp.getColor() == WHITE

def test_key_name_list(profile):
    assert len(profile.getkeyNameList()) == 5