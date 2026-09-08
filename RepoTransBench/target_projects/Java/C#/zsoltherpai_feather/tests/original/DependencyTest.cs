using System;
using Xunit;

namespace Feather.Tests
{
    public class DependencyTest
    {
        [Fact]
        public void DependencyInstance()
        {
            var feather = FeatherBase.With();
            Assert.NotNull(feather.Instance(typeof(Plain)));
        }

        [Fact]
        public void Provider()
        {
            var feather = FeatherBase.With();
            var plainProvider = feather.Provider(typeof(Plain));
            Assert.NotNull(plainProvider.Get());
        }

        [Fact]
        public void Unknown()
        {
            var feather = FeatherBase.With();
            Assert.Throws<FeatherException>(() => feather.Instance(typeof(Unknown)));
        }

        public class Plain { }

        public class Unknown
        {
            public Unknown(string noSuitableConstructor) { }
        }
    }
}