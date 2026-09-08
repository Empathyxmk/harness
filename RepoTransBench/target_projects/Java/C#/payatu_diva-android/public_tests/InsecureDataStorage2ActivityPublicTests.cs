using System;
using System.Collections.Generic;
using Xunit;

namespace PayatuDivaAndroid.PublicTests
{
    public class InsecureDataStorage2Activity
    {
        public class DB
        {
            public List<(string user, string password)> Users = new List<(string, string)>();
        }

        public DB Database { get; } = new DB();

        public void SaveCredentials(string user, string password)
        {
            Database.Users.Add((user, password));
        }
    }

    public class InsecureDataStorage2ActivityPublicTests
    {
        private InsecureDataStorage2Activity activity;

        public InsecureDataStorage2ActivityPublicTests()
        {
            activity = new InsecureDataStorage2Activity();
        }

        [Fact]
        public void Test_OnCreate_CreatesDBAndTable_Public()
        {
            var db = activity.Database;
            Assert.NotNull(db);
            Assert.Empty(db.Users);
        }

        [Fact]
        public void Test_SaveCredentials_InsertsUserData_Public()
        {
            activity.SaveCredentials("anotheruser", "anotherpass");
            Assert.Single(activity.Database.Users);
            var tuple = activity.Database.Users[0];
            Assert.Equal("anotheruser", tuple.user);
            Assert.Equal("anotherpass", tuple.password);
        }
    }
}