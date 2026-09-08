using Xunit;

namespace ProjectName.Tests.Original.Bundler
{
    public class NoneArgsBundler
    {
        private static readonly NoneArgsBundler _instance = new NoneArgsBundler();

        public static NoneArgsBundler Get() => _instance;

        public object? Put(string key, object value, Bundle bundle) => null;

        public object? Get(string key, Bundle bundle) => null;
    }

    public class Bundle { }

    public class NoneArgsBundlerTest
    {
        [Fact]
        public void TestGetInstanceReturnsSingleton()
        {
            var a = NoneArgsBundler.Get();
            var b = NoneArgsBundler.Get();
            Assert.True(object.ReferenceEquals(a, b));
        }

        [Fact]
        public void TestPutReturnsNull()
        {
            Assert.Null(NoneArgsBundler.Get().Put("key", 123, new Bundle()));
        }

        [Fact]
        public void TestGetReturnsNull()
        {
            Assert.Null(NoneArgsBundler.Get().Get("key", new Bundle()));
        }
    }
}