using System;
using System.Collections.Generic;
using Xunit;

namespace PayatuDivaAndroid.PublicTests
{
    public class InsecureDataStorage1Activity
    {
        public Dictionary<string, string> Preferences { get; } = new Dictionary<string, string>();

        public void SaveCredentials(string user, string password)
        {
            Preferences["user"] = user;
            Preferences["password"] = password;
        }
    }

    public class InsecureDataStorage1ActivityPublicTests
    {
        private InsecureDataStorage1Activity activity;

        public InsecureDataStorage1ActivityPublicTests()
        {
            activity = new InsecureDataStorage1Activity();
        }

        [Fact]
        public void Test_SaveCredentials_SavesToPrefs_Public()
        {
            activity.SaveCredentials("publicuser", "publicpass");
            Assert.Equal("publicuser", activity.Preferences["user"]);
            Assert.Equal("publicpass", activity.Preferences["password"]);
        }
    }
}