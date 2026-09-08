using System.Collections.Generic;
using Xunit;
using Remind101ArchExample.Models;

namespace Remind101ArchExample.PublicTests
{
    public class CounterDatabasePublicTests
    {
        private CounterDatabase database;

        public CounterDatabasePublicTests()
        {
            database = CounterDatabase.GetInstance();
            database.Reset();
        }

        [Fact]
        public void TestGetInstanceReturnsSameDatabase()
        {
            var db2 = CounterDatabase.GetInstance();
            Assert.Same(database, db2);
        }

        [Fact]
        public void TestSaveAndGetCounterWithDifferentValue()
        {
            var counter = new Counter();
            counter.SetValue(37);
            database.SaveCounter(counter);

            var result = database.GetCounter(counter.GetId());
            Assert.NotNull(result);
            Assert.Equal(counter.GetId(), result.GetId());
            Assert.Equal(37, result.GetValue());
        }

        [Fact]
        public void TestGetCounterWithAbsentId()
        {
            var c = database.GetCounter(-42);
            Assert.Null(c);
        }

        [Fact]
        public void TestGetAllCountersShouldContainMultipleWithDifferentValues()
        {
            var counter1 = new Counter();
            counter1.SetValue(23);
            database.SaveCounter(counter1);

            var counter2 = new Counter();
            counter2.SetValue(99);
            database.SaveCounter(counter2);

            var list = database.GetAllCounters();
            Assert.True(list.Count >= 2);
            Assert.All(list, c => Assert.True(c.GetId() > 0));
        }
    }
}