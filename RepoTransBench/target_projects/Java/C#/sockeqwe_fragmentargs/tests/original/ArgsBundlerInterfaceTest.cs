using Xunit;

namespace ProjectName.Tests.Original.Bundler
{
    public interface IArgsBundler<T>
    {
        void Put(string key, T value, Bundle bundle);
        V Get<V>(string key, Bundle bundle) where V : T;
    }

    public class Bundle
    {
        public void PutParcelableArrayList(string key, object? value) { /* just placeholder */ }
    }

    public class ArgsBundlerInterfaceTest
    {
        class StringArgsBundler : IArgsBundler<string>
        {
            public void Put(string key, string value, Bundle bundle)
            {
                bundle.PutParcelableArrayList(key, null); // only to exercise interface
            }

            public V Get<V>(string key, Bundle bundle) where V : string
            {
                return default!;
            }
        }

        [Fact]
        public void TestCustomImplementation()
        {
            var bundler = new StringArgsBundler();
            bundler.Put("foo", "bar", new Bundle());
            bundler.Get<string>("foo", new Bundle());
        }
    }
}