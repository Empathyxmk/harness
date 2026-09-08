using System;
using Xunit;
using CaoymJjvm.Lang;

namespace CaoymJjvm.PublicTests
{
    public class JvmFieldMethodPublicTest
    {
        [Fact]
        public void TestAccessDifferentPrimitiveFields()
        {
            var intField = new JvmField("score", "I", 7, false);
            var boolField = new JvmField("visible", "Z", true, false);

            Assert.Equal(7, intField.Value);
            Assert.True((bool)boolField.Value);

            intField.Value = 42;
            Assert.Equal(42, intField.Value);

            boolField.Value = false;
            Assert.False((bool)boolField.Value);
        }

        [Fact]
        public void TestStringFieldDifferentValue()
        {
            var strField = new JvmField("owner", "Ljava/lang/String;", "robot", false);
            Assert.Equal("robot", strField.Value);

            strField.Value = "android";
            Assert.Equal("android", strField.Value);
        }
    }
}