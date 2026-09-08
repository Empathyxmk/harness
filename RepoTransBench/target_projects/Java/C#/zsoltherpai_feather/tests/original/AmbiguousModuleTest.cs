using Xunit;

namespace Feather.Tests
{
    public class AmbiguousModuleTest
    {
        [Fact]
        public void AmbiguousModule()
        {
            Assert.Throws<FeatherException>(() => FeatherBase.With(new Module()));
        }

        public class Module
        {
            [Provides]
            public string Foo() => "foo";
            [Provides]
            public string Bar() => "bar";
        }
    }
    public class ProvidesAttribute : System.Attribute { }
}