using Xunit;

namespace PublicTests
{
    public class StoragePublicTests
    {
        class Storage
        {
            private readonly string dbName, username, password;
            public Storage(string dbName, string username, string password)
            { this.dbName = dbName; this.username = username; this.password = password; }
            public string DbName() => dbName;
            public string Username() => username;
            public string Password() => password;
            public override bool Equals(object o)
            {
                if (o is Storage s)
                    return dbName == s.dbName && username == s.username && password == s.password;
                return false;
            }
            public override int GetHashCode() =>
                dbName.GetHashCode() * 31 * 31 + username.GetHashCode() * 31 + password.GetHashCode();
            public override string ToString() => $"Storage-public {dbName} {username} {password}";
        }

        [Fact]
        public void TestConstructorAndGetters()
        {
            var storage = new Storage("xdb-pub", "uu-pub", "pp-pub");
            Assert.Equal("xdb-pub", storage.DbName());
            Assert.Equal("uu-pub", storage.Username());
            Assert.Equal("pp-pub", storage.Password());
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var s1 = new Storage("a-pub", "b-pub", "c-pub");
            var s2 = new Storage("a-pub", "b-pub", "c-pub");
            var s3 = new Storage("a2-pub", "b2-pub", "c2-pub");

            Assert.Equal(s1, s2);
            Assert.NotEqual(s1, s3);
            Assert.Equal(s1.GetHashCode(), s2.GetHashCode());
            Assert.NotEqual(s1.GetHashCode(), s3.GetHashCode());
        }

        [Fact]
        public void TestToString()
        {
            var storage = new Storage("xdb-pub", "uu-pub", "pp-pub");
            var str = storage.ToString();
            Assert.Contains("xdb-pub", str);
            Assert.Contains("uu-pub", str);
            Assert.Contains("pp-pub", str);
            Assert.Contains("Storage-public", str);
        }
    }
}