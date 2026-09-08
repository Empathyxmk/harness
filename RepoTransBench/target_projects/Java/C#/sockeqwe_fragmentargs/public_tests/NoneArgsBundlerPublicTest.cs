using Xunit;

namespace ProjectName.PublicTests.Bundler
{
    public class NoneArgsBundler
    {
        private static readonly NoneArgsBundler _instance = new NoneArgsBundler();

        public static NoneArgsBundler Get() => _instance;

        public object? Put(string key, object value, Bundle bundle) => null;

        public object? Get(string key, Bundle bundle) => null;
    }

    public class Bundle { }

    public class NoneArgsBundlerPublicTest
    {
        [Fact]
        public void PublicTestInstanceSingleton()
        {
            var a = NoneArgsBundler.Get();
            var b = NoneArgsBundler.Get();
            Assert.True(object.ReferenceEquals(a, b));
        }

        [Fact]
        public void PublicTestPutNullAlways()
        {
            Assert.Null(NoneArgsBundler.Get().Put("publicKey", "hello", new Bundle()));
        }

        [Fact]
        public void PublicTestGetNullAlways()
        {
            Assert.Null(NoneArgsBundler.Get().Get("anotherKey", new Bundle()));
        }
    }
}