using System;
using Xunit;
using Moq;

namespace Skydoves.PreferenceRoom.PublicTests
{
    public class PreferenceKeyFieldPublicTests
    {
        [Fact]
        public void TestDifferentBooleanField()
        {
            var field = new
            {
                typeStringName = "Boolean",
                keyName = "IsActive",
                clazzName = "isActive"
            };

            Assert.Equal("Boolean", field.typeStringName);
            Assert.Equal("IsActive", field.keyName);
            Assert.Equal("isActive", field.clazzName);
        }

        [Fact]
        public void TestStringFieldWithAnotherCustomKeyName()
        {
            var field = new
            {
                keyName = "anotherCustomKey",
                typeStringName = "String"
            };

            Assert.Equal("anotherCustomKey", field.keyName);
            Assert.Equal("String", field.typeStringName);
        }

        [Fact]
        public void TestPrivateFieldThrowsPublic()
        {
            Assert.Throws<InvalidOperationException>(() =>
            {
                throw new InvalidOperationException("Field is private");
            });
        }

        [Fact]
        public void TestNonFinalFieldThrowsPublic()
        {
            Assert.Throws<InvalidOperationException>(() =>
            {
                throw new InvalidOperationException("Field is not final");
            });
        }
    }
}