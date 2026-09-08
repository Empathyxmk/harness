using System;
using System.Collections;
using System.Collections.Generic;
using Xunit;

namespace ProjectName.Tests.Original.Bundler
{
    public interface IParcelable { }
    public interface IParcel { }

    public class CastedArrayListArgsBundler
    {
        public void Put<T>(string key, object value, FakeBundle bundle)
        {
            if (!(value is List<IParcelable> arrList))
                throw new InvalidCastException();

            bundle.ArrayList = arrList;
        }

        public List<T> Get<T>(string key, FakeBundle bundle) where T : IParcelable
        {
            return (List<T>)bundle.ArrayList!;
        }
    }

    public class DummyParcelable : IParcelable { }
    public class FakeBundle
    {
        public IList? ArrayList;
        public void PutParcelableArrayList(string key, IList value) { ArrayList = value; }
        public IList GetParcelableArrayList(string key) { return ArrayList!; }
    }

    public class CastedArrayListArgsBundlerTest
    {
        [Fact]
        public void TestPutThrowsIfNotArrayList()
        {
            var bundler = new CastedArrayListArgsBundler();
            var list = new DummyParcelable[] { new DummyParcelable(), new DummyParcelable() };
            Assert.Throws<InvalidCastException>(() =>
            {
                bundler.Put<DummyParcelable>("key", list, new FakeBundle());
            });
        }

        [Fact]
        public void TestPutAndGetWithArrayList()
        {
            var bundler = new CastedArrayListArgsBundler();
            var arrList = new List<IParcelable> { new DummyParcelable(), new DummyParcelable() };
            var bundle = new FakeBundle();
            bundler.Put<IParcelable>("key", arrList, bundle);

            var result = bundler.Get<IParcelable>("key", bundle);
            Assert.Equal(arrList, result);
        }
    }
}