using Xunit;

namespace OriginalTests
{
    public class StorageTests
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
            public override string ToString() => $"Storage {dbName} {username} {password}";
        }

        [Fact]
        public void TestConstructorAndGetters()
        {
            var storage = new Storage("xdb", "uu", "pp");
            Assert.Equal("xdb", storage.DbName());
            Assert.Equal("uu", storage.Username());
            Assert.Equal("pp", storage.Password());
        }

        [Fact]
        public void TestEqualsAndHashCode()
        {
            var s1 = new Storage("a", "b", "c");
            var s2 = new Storage("a", "b", "c");
            var s3 = new Storage("a2", "b2", "c2");

            Assert.Equal(s1, s2);
            Assert.NotEqual(s1, s3);
            Assert.Equal(s1.GetHashCode(), s2.GetHashCode());
            Assert.NotEqual(s1.GetHashCode(), s3.GetHashCode());
        }

        [Fact]
        public void TestToString()
        {
            var storage = new Storage("xdb", "uu", "pp");
            var str = storage.ToString();
            Assert.Contains("xdb", str);
            Assert.Contains("uu", str);
            Assert.Contains("pp", str);
        }
    }
}