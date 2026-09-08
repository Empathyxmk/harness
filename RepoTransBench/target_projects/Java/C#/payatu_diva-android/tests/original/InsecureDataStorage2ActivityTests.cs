using System;
using System.Collections.Generic;
using Xunit;

namespace PayatuDivaAndroid.Tests.Original
{
    public class InsecureDataStorage2Activity
    {
        public class DB
        {
            public List<(string user, string password)> Users = new List<(string,string)>();
        }

        public DB Database { get; } = new DB();

        public void SaveCredentials(string user, string password)
        {
            Database.Users.Add((user, password));
        }
    }

    public class InsecureDataStorage2ActivityTests
    {
        private InsecureDataStorage2Activity activity;

        public InsecureDataStorage2ActivityTests()
        {
            activity = new InsecureDataStorage2Activity();
        }

        [Fact]
        public void Test_OnCreate_CreatesDBAndTable()
        {
            // In simulated C#, DB/table creation is automatic, nothing to throw
            var db = activity.Database;
            Assert.NotNull(db);
            Assert.Empty(db.Users);
        }

        [Fact]
        public void Test_SaveCredentials_InsertsUserData()
        {
            activity.SaveCredentials("dbuser", "dbpass");
            Assert.Single(activity.Database.Users);
            var tuple = activity.Database.Users[0];
            Assert.Equal("dbuser", tuple.user);
            Assert.Equal("dbpass", tuple.password);
        }
    }
}