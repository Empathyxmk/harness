using Xunit;
using Vatri.Ecommerce.Cache;
using Moq;
using System;

namespace PublicTests
{
    public class RedisCachePublicTest
    {
        [Fact]
        public void TestSetAndGetDifferentKeyValue()
        {
            var cache = new RedisCache();
            var key = "publicKey";
            var value = "publicValue";

            Assert.True((bool)cache.Set(key, value));
            var retrieved = cache.Get(key, typeof(string));
            Assert.Null(retrieved);

            var missingKeyResult = cache.Get("missingKey", typeof(string));
            Assert.Null(missingKeyResult);
        }

        [Fact]
        public void TestDeleteKey()
        {
            var cache = new RedisCache();
            Assert.True(cache.Delete("deletePublic"));
            Assert.True(cache.Delete("doesNotExist"));
        }
    }
}