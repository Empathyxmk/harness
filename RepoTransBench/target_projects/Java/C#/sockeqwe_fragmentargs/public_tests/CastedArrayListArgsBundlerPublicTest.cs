using System.Collections.Generic;
using Xunit;

namespace ProjectName.PublicTests.Bundler
{
    public interface IParcelable { }
    public interface IParcel { }

    public class CastedArrayListArgsBundler
    {
        public void Put<T>(string key, object value, Bundle bundle)
        {
            if (!(value is List<MyParcelablePublic> arrList))
                throw new System.InvalidCastException();

            bundle.ArrayList = arrList;
        }

        public List<T> Get<T>(string key, Bundle bundle) where T : IParcelable
        {
            return (List<T>)bundle.ArrayList!;
        }
    }

    public class MyParcelablePublic : IParcelable
    {
        public string Str { get; }
        public MyParcelablePublic(string str) { Str = str; }

        public override bool Equals(object? obj)
        {
            if (obj is MyParcelablePublic other)
                return this.Str == other.Str;
            return false;
        }

        public override int GetHashCode() => Str.GetHashCode();
    }

    public class Bundle
    {
        public object? ArrayList;
        public void PutParcelableArrayList(string key, object value) { ArrayList = value; }
        public object GetParcelableArrayList(string key) { return ArrayList!; }
        public void PutString(string key, string value) { }
        public string? GetString(string key) => null;
    }

    public class CastedArrayListArgsBundlerPublicTest
    {
        [Fact]
        public void TestCastedArrayListArgsBundlerWithParcelable_PublicVariant()
        {
            var bundler = new CastedArrayListArgsBundler();
            var data = new List<MyParcelablePublic>
            {
                new MyParcelablePublic("dragonfruit"),
                new MyParcelablePublic("peach"),
                new MyParcelablePublic("plum")
            };
            var bundle = new Bundle();
            bundler.Put<MyParcelablePublic>("UniqueFruitKey", data, bundle);

            var restored = (List<MyParcelablePublic>)bundler.Get<MyParcelablePublic>("UniqueFruitKey", bundle);

            Assert.Equal(data, restored);
        }
    }
}