using System;
using Xunit;
using System.Collections.Generic;

namespace Props2Js.Tests.Original
{
    public class PropertyConverterTest
    {
        [Fact]
        public void TestConvertToJson_withString()
        {
            var p = new Dictionary<string, string> { { "name", "value" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""name"":""value""", json);
        }

        [Fact]
        public void TestConvertToJson_withInt()
        {
            var p = new Dictionary<string, string> { { "intValue", "123" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""intValue"":123", json);
        }

        [Fact]
        public void TestConvertToJson_withFloat()
        {
            var p = new Dictionary<string, string> { { "floatValue", "12.34" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""floatValue"":12.34", json);
        }

        [Fact]
        public void TestConvertToJson_withBooleanTrue()
        {
            var p = new Dictionary<string, string> { { "flag", "true" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""flag"":true", json);
        }

        [Fact]
        public void TestConvertToJson_withBooleanFalse()
        {
            var p = new Dictionary<string, string> { { "flag", "false" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""flag"":false", json);
        }

        [Fact]
        public void TestConvertToJsonP()
        {
            var p = new Dictionary<string, string> { { "a", "1" } };
            string outVal = PropertyConverter.ConvertToJsonP(p, "cb");
            Assert.StartsWith("cb(", outVal);
            Assert.EndsWith(");", outVal.Trim());
        }

        [Fact]
        public void TestConvertToJavaScript_var()
        {
            var p = new Dictionary<string, string> { { "foo", "bar" } };
            string js = PropertyConverter.ConvertToJavaScript(p, "testVar");
            Assert.StartsWith("var testVar=", js);
            Assert.EndsWith(";", js.Trim());
        }

        [Fact]
        public void TestConvertToJavaScript_assignment()
        {
            var p = new Dictionary<string, string> { { "foo", "bar" } };
            string js = PropertyConverter.ConvertToJavaScript(p, "object.property");
            Assert.DoesNotContain("var ", js);
            Assert.StartsWith("object.property=", js);
            Assert.EndsWith(";", js.Trim());
        }

        [Fact]
        public void TestConvertToJson_withMixedTypes()
        {
            var p = new Dictionary<string, string>
            {
                { "string", "text" },
                { "int", "42" },
                { "float", "2.718" },
                { "trueBool", "true" },
                { "falseBool", "false" }
            };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""string"":""text""", json);
            Assert.Contains(@"""int"":42", json);
            Assert.Contains(@"""float"":2.718", json);
            Assert.Contains(@"""trueBool"":true", json);
            Assert.Contains(@"""falseBool"":false", json);
        }

        [Fact]
        public void TestConvertToJson_handlesEmptyProperties()
        {
            var p = new Dictionary<string, string>();
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Equal("{}", json);
        }
    }
}