using Xunit;

namespace HelloDesignPattern.Tests
{
    public class SplitHelloWorldTest
    {
        [Fact]
        public void TestToStringWithAnonymousClasses()
        {
            var interjection = new CustomInterjection();
            var obj = new CustomObject();
            var split = new SplitHelloWorld(interjection, obj);
            var result = split.ToString();
            Assert.Contains("Hello", result);
            Assert.Contains("World", result);
        }

        private class CustomInterjection : SplitHelloWorld.IHelloWorldInterjection
        {
            public string Interjection() => "Hello";
        }

        private class CustomObject : SplitHelloWorld.IHelloWorldObject
        {
            public string Object() => "World";
        }
    }
}