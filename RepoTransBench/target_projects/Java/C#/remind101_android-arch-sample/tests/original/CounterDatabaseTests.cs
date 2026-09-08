using System.Collections.Generic;
using Xunit;
using Remind101ArchExample.Models;

namespace Remind101ArchExample.Tests.Original
{
    public class CounterDatabaseTests
    {
        private CounterDatabase database;

        public CounterDatabaseTests()
        {
            database = CounterDatabase.GetInstance();
            // Reset for test isolation (presume a method to reset exists or is faked for .NET)
            database.Reset();
        }

        [Fact]
        public void TestGetInstanceSingleton()
        {
            var db2 = CounterDatabase.GetInstance();
            Assert.Same(database, db2);
        }

        [Fact]
        public void TestSaveAndGetCounter()
        {
            var counter = new Counter();
            counter.SetValue(15);
            database.SaveCounter(counter);

            var result = database.GetCounter(counter.GetId());
            Assert.NotNull(result);
            Assert.Equal(counter.GetId(), result.GetId());
            Assert.Equal(15, result.GetValue());
        }

        [Fact]
        public void TestGetCounterNotFound()
        {
            var c = database.GetCounter(-1);
            Assert.Null(c);
        }

        [Fact]
        public void TestGetAllCounters()
        {
            var counter1 = new Counter();
            counter1.SetValue(5);
            database.SaveCounter(counter1);

            var counter2 = new Counter();
            counter2.SetValue(11);
            database.SaveCounter(counter2);

            var list = database.GetAllCounters();
            Assert.True(list.Count >= 2);
            Assert.All(list, c => Assert.True(c.GetId() > 0));
        }
    }
}