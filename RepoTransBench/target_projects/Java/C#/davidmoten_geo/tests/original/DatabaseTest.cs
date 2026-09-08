using System;
using System.Data;
using System.Data.SQLite;
using Xunit;
using System.IO;
using System.Reflection;
using System.Linq;

namespace DavidMoten.Geo.Tests
{
    public class DatabaseTest
    {
        [Fact]
        public void TestCreateTableInsertAndQuery()
        {
            // Use SQLite in-memory for demonstration, actual JDBC/H2 translation would require refactoring
            using var conn = new SQLiteConnection("Data Source=:memory:");
            conn.Open();
            using (var cmd = new SQLiteCommand("CREATE TABLE report (time INTEGER, lat REAL, lon REAL, name TEXT, geohash1 TEXT, geohash2 TEXT, geohash3 TEXT, geohash4 TEXT, geohash5 TEXT, geohash6 TEXT, geohash7 TEXT, geohash8 TEXT, geohash9 TEXT, geohash10 TEXT, geohash11 TEXT, geohash12 TEXT)", conn))
            {
                cmd.ExecuteNonQuery();
            }
            var now = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            using (var cmd = new SQLiteCommand(
                "INSERT INTO report(time,lat,lon,name,geohash1,geohash2,geohash3,geohash4,geohash5,geohash6,geohash7,geohash8,geohash9,geohash10,geohash11,geohash12) VALUES(@time,@lat,@lon,@name,@g1,@g2,@g3,@g4,@g5,@g6,@g7,@g8,@g9,@g10,@g11,@g12)", conn))
            {
                cmd.Parameters.AddWithValue("@time", now);
                cmd.Parameters.AddWithValue("@lat", -10);
                cmd.Parameters.AddWithValue("@lon", 150);
                cmd.Parameters.AddWithValue("@name", "A");
                for (int j = 1; j <= 12; j++)
                {
                    cmd.Parameters.AddWithValue($"@g{j}", new string('a', j));
                }
                cmd.ExecuteNonQuery();
            }
            // Select back
            using (var cmd = new SQLiteCommand("SELECT name,lat,lon FROM report WHERE time >= @from AND time < @to", conn))
            {
                cmd.Parameters.AddWithValue("@from", now - 1000);
                cmd.Parameters.AddWithValue("@to", now + 1000);
                using var reader = cmd.ExecuteReader();
                int count = 0;
                while (reader.Read())
                {
                    Assert.Equal("A", reader.GetString(0));
                    Assert.Equal(-10, reader.GetDouble(1), 5);
                    Assert.Equal(150, reader.GetDouble(2), 5);
                    count++;
                }
                Assert.True(count > 0);
            }
        }
    }
}