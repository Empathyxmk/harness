using Xunit;
using Vatri.Ecommerce.Cache;
using Moq;
using System.Collections.Generic;
using System;

namespace OriginalTests
{
    public class RedisCacheTest
    {
        private RedisCache _cache;

        public class MockObject
        {
            public int id = 0;
            public MockObject(int i) { id = i; }
        }

        public RedisCacheTest()
        {
            _cache = new RedisCache();
        }

        [Fact]
        public void TestGetList()
        {
            var list = _cache.GetList<MockObject>("item", typeof(MockObject));
            foreach (var o in list)
            {
                Assert.NotNull(o);
            }
            Assert.True(true);
        }

        [Fact]
        public void TestGetItem()
        {
            var o = (MockObject)_cache.GetItem("item", typeof(MockObject));
            Assert.NotNull(o);
        }

        [Fact]
        public void TestAddObjectToList()
        {
            var list = _cache.AddItemToList("item", new MockObject(1));
            Assert.Equal(2, ((ICollection<object>)list).Count);
        }

        [Fact]
        public void TestRemoveObjectFromList()
        {
            var list = _cache.RemoveItemFromList("item", new MockObject(1));
            Assert.Equal(1, ((ICollection<object>)list).Count);
        }

        [Fact]
        public void TestAddingObjectToCache()
        {
            var res = (MockObject)_cache.SetItem("new_item", new MockObject(1));
            Assert.Equal(1, res.id);
        }
    }
}