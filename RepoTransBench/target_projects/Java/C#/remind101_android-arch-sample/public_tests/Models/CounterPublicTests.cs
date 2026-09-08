using Xunit;
using Remind101ArchExample.Models;

namespace Remind101ArchExample.PublicTests.Models
{
    public class CounterPublicTests
    {
        [Fact]
        public void TestCounterIncrementPublic()
        {
            var counter = new Counter();
            var oldValue = counter.GetValue();
            counter.Increment();
            Assert.Equal(oldValue + 1, counter.GetValue());
        }

        [Fact]
        public void TestCounterDecrementPublic()
        {
            var counter = new Counter();
            counter.SetValue(78);
            counter.Decrement();
            Assert.Equal(77, counter.GetValue());
        }

        [Fact]
        public void TestCounterSetValueAndGetIdPublic()
        {
            var counter = new Counter();
            counter.SetValue(1234);
            Assert.Equal(1234, counter.GetValue());
            Assert.True(counter.GetId() > 0);
        }
    }
}