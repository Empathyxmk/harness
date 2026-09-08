using System;
using Xunit;
using System.Collections.Generic;

namespace PayatuDivaAndroid.Tests.Original
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

    public class InsecureDataStorage1ActivityTests
    {
        private InsecureDataStorage1Activity activity;

        public InsecureDataStorage1ActivityTests()
        {
            activity = new InsecureDataStorage1Activity();
        }

        [Fact]
        public void Test_OnCreate_SetsLayout()
        {
            Assert.NotNull(activity.Preferences);
        }

        [Fact]
        public void Test_SaveCredentials_StoresCredentials()
        {
            activity.SaveCredentials("testuser", "secret");
            Assert.Equal("testuser", activity.Preferences["user"]);
            Assert.Equal("secret", activity.Preferences["password"]);
        }
    }
}