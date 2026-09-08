using Xunit;
using Remind101ArchExample.Models;

namespace Remind101ArchExample.Tests.Original.Models
{
    public class CounterTests
    {
        [Fact]
        public void TestCounterDefaultConstructorAndValue()
        {
            var counter = new Counter();
            Assert.Equal(0, counter.GetId());
            Assert.Equal(0, counter.GetValue());
        }

        [Fact]
        public void TestCounterSetAndGetId()
        {
            var counter = new Counter();
            counter.SetId(123);
            Assert.Equal(123, counter.GetId());
        }

        [Fact]
        public void TestCounterSetAndGetValue()
        {
            var counter = new Counter();
            counter.SetValue(10);
            Assert.Equal(10, counter.GetValue());
        }
    }
}