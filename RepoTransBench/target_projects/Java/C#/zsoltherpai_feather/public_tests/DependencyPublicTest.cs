using System;
using Xunit;

namespace Feather.PublicTests
{
    public class DependencyPublicTest
    {
        [Fact]
        public void DependencyInstancePublic()
        {
            var feather = FeatherBase.With();
            Assert.NotNull(feather.Instance(typeof(PublicPlain)));
        }

        [Fact]
        public void ProviderPublic()
        {
            var feather = FeatherBase.With();
            var plainProvider = feather.Provider(typeof(PublicPlain));
            Assert.NotNull(plainProvider.Get());
        }

        [Fact]
        public void UnknownPublic()
        {
            var feather = FeatherBase.With();
            Assert.Throws<FeatherException>(() => feather.Instance(typeof(AnotherUnknown)));
        }

        public class PublicPlain { }

        public class AnotherUnknown
        {
            public AnotherUnknown(int diffConstructor) { }
        }
    }
}