using Xunit;

namespace Feather.Tests
{
    public class NamedDependencyTest
    {
        [Fact]
        public void NamedInstanceWithModule()
        {
            var feather = FeatherBase.With(new HelloWorldModule());
            Assert.Equal("Hello!", feather.Instance(Key.Of(typeof(string), "hello")));
            Assert.Equal("Hi!", feather.Instance(Key.Of(typeof(string), "hi")));
        }

        public class HelloWorldModule
        {
            [Provides, Named("hello")]
            public string Hello() => "Hello!";
            [Provides, Named("hi")]
            public string Hi() => "Hi!";
        }
    }

    public class NamedAttribute : System.Attribute
    {
        public string Value { get; }
        public NamedAttribute(string value) => Value = value;
    }
    public class ProvidesAttribute : System.Attribute { }
}