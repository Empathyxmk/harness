using System;
using System.Reflection;
using Xunit;

namespace Orhanobut.Tracklytics.Tests
{
    public class AttributeAnnotationTest
    {
        [Attribute("val", DefaultValue = "def", IsSuper = true)]
        private void DummyMethod() { }

        [Fact]
        public void TestAttributeValues()
        {
            var method = GetType().GetMethod("DummyMethod", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
            var attr = method.GetCustomAttribute<AttributeAttribute>();
            Assert.NotNull(attr);
            Assert.Equal("val", attr.Value);
            Assert.Equal("def", attr.DefaultValue);
            Assert.True(attr.IsSuper);
        }

        [Attribute("key")]
        private void DummySimple() { }

        [Fact]
        public void TestAttributeDefaultIsSuperAndDefaultValue()
        {
            var method = GetType().GetMethod("DummySimple", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
            var attr = method.GetCustomAttribute<AttributeAttribute>();
            Assert.NotNull(attr);
            Assert.Equal("key", attr.Value);
            Assert.Equal("", attr.DefaultValue);
            Assert.False(attr.IsSuper);
        }
    }
}