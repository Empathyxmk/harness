using Xunit;

namespace Feather.Tests
{
    public class ProviderInjectionTest
    {
        [Fact]
        public void ProviderInjected()
        {
            var feather = FeatherBase.With();
            var a = (A)feather.Instance(typeof(A));
            Assert.NotNull(a.PlainProvider.Get());
        }

        public class A
        {
            public IProvider<B> PlainProvider { get; }
            public A(IProvider<B> plainProvider)
            {
                PlainProvider = plainProvider;
            }
        }

        public class B { }
    }
}