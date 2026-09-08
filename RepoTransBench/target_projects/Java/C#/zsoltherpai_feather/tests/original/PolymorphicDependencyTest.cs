using Xunit;

namespace Feather.Tests
{
    public class PolymorphicDependencyTest
    {
        [Fact]
        public void MultipleImplementations()
        {
            var feather = FeatherBase.With(new Module());
            Assert.Equal(typeof(FooA), feather.Instance(Key.Of(typeof(IFoo), "A")).GetType());
            Assert.Equal(typeof(FooB), feather.Instance(Key.Of(typeof(IFoo), "B")).GetType());
        }

        public class Module
        {
            [Provides, Named("A")]
            public IFoo AFoo(FooA fooA) => fooA;
            [Provides, Named("B")]
            public IFoo BFoo(FooB fooB) => fooB;
        }

        public interface IFoo { }

        public class FooA : IFoo
        {
            public FooA() { }
        }
        public class FooB : IFoo
        {
            public FooB() { }
        }
    }
    public class ProvidesAttribute : System.Attribute { }
    public class NamedAttribute : System.Attribute
    {
        public string Value { get; }
        public NamedAttribute(string value) => Value = value;
    }
}