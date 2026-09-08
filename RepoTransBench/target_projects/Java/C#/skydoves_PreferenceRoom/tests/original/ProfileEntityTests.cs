using System.Collections.Generic;
using Xunit;

namespace Skydoves.PreferenceRoom.OriginalTests
{
    // Simulated profile preference
    public class Preference_UserProfile
    {
        private static Preference_UserProfile _instance;
        private Dictionary<string, object> prefs = new();

        public static Preference_UserProfile GetInstance()
            => _instance ??= new Preference_UserProfile();

        public void Clear() => prefs.Clear();
        public void PutNickname(string nickname) => prefs["nickname"] = "Hello, " + nickname + "!!!";
        public void PutLogin(bool login) => prefs["login"] = login;
        public void PutVisits(int visits) => prefs["visits"] = visits + 1;
        public void PutUserinfo(PrivateInfo info) => prefs["userinfo"] = info;
        public void PutUserPet(Pet pet) => prefs["userPet"] = pet;
        public string GetNickname() => prefs.ContainsKey("nickname") ? (string)prefs["nickname"] : "skydoves!!!";
        public bool GetLogin() => prefs.ContainsKey("login") && (bool)prefs["login"];
        public int GetVisits() => prefs.ContainsKey("visits") ? (int)prefs["visits"] : 1;
        public PrivateInfo GetUserinfo() => prefs.ContainsKey("userinfo") ? (PrivateInfo)prefs["userinfo"] : new PrivateInfo("null", 0);
        public Pet GetUserPet() => prefs.ContainsKey("userPet") ? (Pet)prefs["userPet"] : null;
        public List<string> GetKeyNameList() => new() { "nickname", "login", "visits", "userinfo", "userPet" };

        public string NicknameKeyName() => "nickname";
        public string LoginKeyName() => "login";
        public string VisitsKeyName() => "visits";
        public string UserinfoKeyName() => "userinfo";
        public string UserPetKeyName() => "userPet";
        public string GetEntityName() => "UserProfile";
    }

    public class PrivateInfo
    {
        public string Name { get; }
        public int Age { get; }

        public PrivateInfo(string name, int age) { Name = name; Age = age; }
    }

    public class Pet
    {
        public string Name { get; }
        public int Age { get; }
        public bool IsFeed { get; }
        public int Color { get; }

        public Pet(string name, int age, bool isFeed, int color) { Name = name; Age = age; IsFeed = isFeed; Color = color; }
    }

    public class ProfileEntityTests
    {
        Preference_UserProfile profile;
        public ProfileEntityTests()
        {
            profile = Preference_UserProfile.GetInstance();
            profile.Clear();
        }

        [Fact]
        public void PreferenceTest()
        {
            profile.Clear();
            profile.PutNickname("PreferenceRoom");
            profile.PutLogin(true);
            profile.PutVisits(12);

            Assert.Equal("Hello, PreferenceRoom!!!", profile.GetNickname());
            Assert.True(profile.GetLogin());
            Assert.Equal(13, profile.GetVisits());
        }

        [Fact]
        public void DefaultTest()
        {
            profile.Clear();
            Assert.Equal("skydoves!!!", profile.GetNickname());
            Assert.False(profile.GetLogin());
            Assert.Equal(1, profile.GetVisits());
            Assert.Equal("null", profile.GetUserinfo().Name);
            Assert.Null(profile.GetUserPet());
        }

        [Fact]
        public void PutPreferenceTest()
        {
            profile.Clear();
            profile.PutNickname("PreferenceRoom");
            profile.PutLogin(true);
            profile.PutVisits(12);
            profile.PutUserinfo(new PrivateInfo("Jaewoong", 123));

            Assert.Equal("Hello, PreferenceRoom!!!", profile.GetNickname());
            Assert.True(profile.GetLogin());
            Assert.Equal(13, profile.GetVisits());
            Assert.Equal("Jaewoong", profile.GetUserinfo().Name);
            Assert.Equal(123, profile.GetUserinfo().Age);
        }

        [Fact]
        public void BaseGsonConverterTest()
        {
            var pet = new Pet("skydoves", 11, true, 0xFFFFFFFF);
            profile.PutUserPet(pet);

            var petFromPref = profile.GetUserPet();
            Assert.Equal("skydoves", petFromPref.Name);
            Assert.Equal(11, petFromPref.Age);
            Assert.True(petFromPref.IsFeed);
            Assert.Equal(0xFFFFFFFF, petFromPref.Color);
        }

        [Fact]
        public void KeyNameListTest()
        {
            Assert.Equal(5, profile.GetKeyNameList().Count);
        }
    }
}