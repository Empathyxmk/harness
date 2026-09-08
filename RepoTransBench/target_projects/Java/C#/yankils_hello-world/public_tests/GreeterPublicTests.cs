using Xunit;
using YankilsHelloWorld;

namespace YankilsHelloWorld.PublicTests
{
    public class GreeterPublicTests
    {
        [Fact]
        public void TestGreetAnotherName()
        {
            var greeter = new Greeter();
            var result = greeter.Greet("Alice");
            Assert.Equal("Hello, Alice!", result);
        }

        [Fact]
        public void TestGreetWithDifferentName()
        {
            var greeter = new Greeter();
            var result = greeter.Greet("Charlie");
            Assert.Equal("Hello, Charlie!", result);
        }

        [Fact]
        public void TestGreetWithEmptyString()
        {
            var greeter = new Greeter();
            var result = greeter.Greet("");
            Assert.Equal("Hello, !", result);
        }

        [Fact]
        public void TestGreetWithSpecialCharacters()
        {
            var greeter = new Greeter();
            var result = greeter.Greet("@User#123");
            Assert.Equal("Hello, @User#123!", result);
        }
    }
}