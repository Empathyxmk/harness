using System;
using System.Reflection;
using Xunit;

namespace Orhanobut.Tracklytics.PublicTests
{
    public class AttributeAnnotationPublicTest
    {
        [Attribute(Value = "pubKey", DefaultValue = "pubDefault", IsSuper = true)]
        public void PublicMethod([Attribute("pubParam")] string param) { }

        [Fact]
        public void TestAttributeAnnotationPublicPresent()
        {
            var method = GetType().GetMethod("PublicMethod", new[] { typeof(string) });
            Assert.True(method.IsDefined(typeof(AttributeAttribute), false));
            var attr = method.GetCustomAttribute<AttributeAttribute>();
            Assert.Equal("pubKey", attr.Value);
            Assert.Equal("pubDefault", attr.DefaultValue);
            Assert.True(attr.IsSuper);
        }

        [Fact]
        public void TestParameterAnnotationPublicPresent()
        {
            var method = GetType().GetMethod("PublicMethod", new[] { typeof(string) });
            var attr = (AttributeAttribute)method.GetParameters()[0].GetCustomAttributes(typeof(AttributeAttribute), false)[0];
            Assert.Equal("pubParam", attr.Value);
        }
    }
}