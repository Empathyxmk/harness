using Xunit;
using System.Data.SQLite;

namespace DavidMoten.Geo.PublicTests
{
    public class DatabasePublicTest
    {
        [Fact]
        public void TestCreateTableAndInsertSelectDifferentData()
        {
            using var conn = new SQLiteConnection("Data Source=:memory:");
            conn.Open();
            using (var cmd = new SQLiteCommand("CREATE TABLE foo (id INTEGER PRIMARY KEY, bar TEXT)", conn))
            {
                cmd.ExecuteNonQuery();
                cmd.CommandText = "INSERT INTO foo (bar) VALUES ('PublicFoo')";
                cmd.ExecuteNonQuery();
            }
            using (var ps = new SQLiteCommand("SELECT bar FROM foo WHERE id = 1", conn))
            using (var reader = ps.ExecuteReader())
            {
                Assert.True(reader.Read());
                Assert.Equal("PublicFoo", reader.GetString(0));
            }
        }

        [Fact]
        public void TestInsertAndCountRowsDifferent()
        {
            using var conn = new SQLiteConnection("Data Source=:memory:");
            conn.Open();
            using (var cmd = new SQLiteCommand("CREATE TABLE baz (id INTEGER PRIMARY KEY, value INTEGER)", conn))
            {
                cmd.ExecuteNonQuery();
                for (int i = 100; i < 105; i++)
                {
                    cmd.CommandText = $"INSERT INTO baz (value) VALUES ({i})";
                    cmd.ExecuteNonQuery();
                }
            }
            using (var ps = new SQLiteCommand("SELECT COUNT(*) FROM baz", conn))
            using (var reader = ps.ExecuteReader())
            {
                Assert.True(reader.Read());
                Assert.Equal(5, reader.GetInt32(0));
            }
        }
    }
}