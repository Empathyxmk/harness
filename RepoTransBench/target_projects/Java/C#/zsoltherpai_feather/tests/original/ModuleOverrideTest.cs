using Xunit;

namespace Feather.Tests
{
    public class ModuleOverrideTest
    {
        [Fact]
        public void DependencyOverridenByModule()
        {
            var feather = FeatherBase.With(new PlainStubOverrideModule());
            Assert.Equal(typeof(PlainStub), feather.Instance(typeof(Plain)).GetType());
        }

        [Fact]
        public void ModuleOverwrittenBySubClass()
        {
            Assert.Equal("foo", FeatherBase.With(new FooModule()).Instance(typeof(string)));
            Assert.Equal("bar", FeatherBase.With(new FooOverrideModule()).Instance(typeof(string)));
        }

        public class Plain { }

        public class PlainStub : Plain { }

        public class PlainStubOverrideModule
        {
            [Provides]
            public Plain Plain(PlainStub plainStub) => plainStub;
        }

        public class FooModule
        {
            [Provides]
            public string Foo() => "foo";
        }

        public class FooOverrideModule : FooModule
        {
            [Provides]
            public override string Foo() => "bar";
        }
    }

    public class ProvidesAttribute : System.Attribute { }
}