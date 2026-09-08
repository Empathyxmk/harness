using Xunit;

namespace Feather.Tests
{
    public class SingletonTest
    {
        [Fact]
        public void NonSingleton()
        {
            var feather = FeatherBase.With();
            Assert.NotEqual(
                feather.Instance(typeof(Plain)),
                feather.Instance(typeof(Plain))
            );
        }

        [Fact]
        public void Singleton()
        {
            var feather = FeatherBase.With();
            Assert.Equal(
                feather.Instance(typeof(SingletonObj)),
                feather.Instance(typeof(SingletonObj))
            );
        }

        [Fact]
        public void SingletonThroughProvider()
        {
            var feather = FeatherBase.With();
            var provider = feather.Provider(typeof(SingletonObj));
            Assert.Equal(provider.Get(), provider.Get());
        }

        public class Plain { }

        [System.AttributeUsage(System.AttributeTargets.Class)]
        public class SingletonAttribute : System.Attribute { }

        [Singleton]
        public class SingletonObj { }
    }
}