using Xunit;

namespace Feather.Tests
{
    public class PojoProvidedThroughModuleTest
    {
        [Fact]
        public void PojoNotProvided()
        {
            var feather = FeatherBase.With();
            Assert.Throws<FeatherException>(() => feather.Instance(typeof(Pojo)));
        }

        [Fact]
        public void PojoProvided()
        {
            var feather = FeatherBase.With(new Module());
            Assert.NotNull(feather.Instance(typeof(Pojo)));
        }

        public class Module
        {
            [Provides]
            public Pojo Pojo() => new Pojo("foo");
        }

        public class Pojo
        {
            private readonly string foo;
            public Pojo(string foo) { this.foo = foo; }
        }
    }

    public class ProvidesAttribute : System.Attribute { }
}