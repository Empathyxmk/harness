using Xunit;

namespace Feather.Tests
{
    public class FieldInjectionTest
    {
        [Fact]
        public void FieldsInjected()
        {
            var feather = FeatherBase.With();
            var target = new Target();
            feather.InjectFields(target);
            Assert.NotNull(target.A);
        }

        public class Target
        {
            public A? A { get; set; }
        }

        public class A { }
    }
}