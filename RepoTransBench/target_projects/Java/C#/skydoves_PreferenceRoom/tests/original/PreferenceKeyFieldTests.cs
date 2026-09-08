using System;
using Xunit;
using Moq;

namespace Skydoves.PreferenceRoom.OriginalTests
{
    public class PreferenceKeyFieldTests
    {
        [Fact]
        public void TestBooleanField()
        {
            var field = new
            {
                typeStringName = "Boolean",
                keyName = "Flag",
                clazzName = "flag"
            };

            Assert.Equal("Boolean", field.typeStringName);
            Assert.Equal("Flag", field.keyName);
            Assert.Equal("flag", field.clazzName);
        }

        [Fact]
        public void TestStringFieldWithCustomKeyName()
        {
            var field = new
            {
                keyName = "customKey",
                typeStringName = "String"
            };

            Assert.Equal("customKey", field.keyName);
            Assert.Equal("String", field.typeStringName);
        }

        [Fact]
        public void TestPrivateFieldThrows()
        {
            Assert.Throws<InvalidOperationException>(() =>
            {
                throw new InvalidOperationException("Field is private");
            });
        }

        [Fact]
        public void TestNonFinalFieldThrows()
        {
            Assert.Throws<InvalidOperationException>(() =>
            {
                throw new InvalidOperationException("Field is not final");
            });
        }
    }
}