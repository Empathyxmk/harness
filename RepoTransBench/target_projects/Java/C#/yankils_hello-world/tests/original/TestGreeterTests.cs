using Xunit;
using YankilsHelloWorld;

namespace YankilsHelloWorld.Tests.Original
{
    public class TestGreeterTests
    {
        [Fact]
        public void TestGreetNormal()
        {
            var greeter = new Greeter();
            var result = greeter.Greet("World");
            Assert.Equal("Hello, World!", result);
        }

        [Fact]
        public void TestGreetEmpty()
        {
            var greeter = new Greeter();
            var result = greeter.Greet("");
            Assert.Equal("Hello, !", result);
        }

        [Fact]
        public void TestGreetWhitespace()
        {
            var greeter = new Greeter();
            var result = greeter.Greet("   ");
            Assert.Equal("Hello,    !", result);
        }

        [Fact]
        public void TestGreetNull()
        {
            var greeter = new Greeter();
            var result = greeter.Greet(null);
            Assert.Equal("Hello, null!", result);
        }

        [Fact]
        public void TestGreetCustomName()
        {
            var greeter = new Greeter();
            var result = greeter.Greet("Alice");
            Assert.Equal("Hello, Alice!", result);
        }
    }
}