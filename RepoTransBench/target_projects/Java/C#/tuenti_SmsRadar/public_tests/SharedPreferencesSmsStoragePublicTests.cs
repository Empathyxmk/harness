using System;
using Xunit;
using Tuenti.SmsRadar;

namespace Tuenti.SmsRadar.Tests.Public
{
    public class SharedPreferencesSmsStoragePublicTests
    {
        private SharedPreferencesSmsStorage storage;

        public SharedPreferencesSmsStoragePublicTests()
        {
            storage = new SharedPreferencesSmsStorage();
            storage.ClearPreferences();
        }

        [Fact]
        public void TestPutAndGetValue()
        {
            storage.PutString("animal", "dog");
            Assert.Equal("dog", storage.GetString("animal", ""));
        }

        [Fact]
        public void TestOverwriteValue()
        {
            storage.PutString("language", "Python");
            storage.PutString("language", "Go");
            Assert.Equal("Go", storage.GetString("language", ""));
        }

        [Fact]
        public void TestGetDefaultIfNotPresent()
        {
            Assert.Equal("default", storage.GetString("missing-key", "default"));
        }
    }
}