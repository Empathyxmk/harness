using System;
using Xunit;
using System.Collections.Generic;

namespace Props2Js.Tests.Public
{
    public class PropertyConverterPublicTest
    {
        [Fact]
        public void TestConvertToJson_withString_public()
        {
            var p = new Dictionary<string, string> { { "color", "blue" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""color"":""blue""", json);
        }

        [Fact]
        public void TestConvertToJson_withInt_public()
        {
            var p = new Dictionary<string, string> { { "answer", "42" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""answer"":42", json);
        }

        [Fact]
        public void TestConvertToJson_withFloat_public()
        {
            var p = new Dictionary<string, string> { { "ratio", "3.14" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""ratio"":3.14", json);
        }

        [Fact]
        public void TestConvertToJson_withBooleanTrue_public()
        {
            var p = new Dictionary<string, string> { { "active", "true" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""active"":true", json);
        }

        [Fact]
        public void TestConvertToJson_withBooleanFalse_public()
        {
            var p = new Dictionary<string, string> { { "deleted", "false" } };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""deleted"":false", json);
        }

        [Fact]
        public void TestConvertToJsonP_public()
        {
            var p = new Dictionary<string, string> { { "score", "77" } };
            string outVal = PropertyConverter.ConvertToJsonP(p, "pubcb");
            Assert.StartsWith("pubcb(", outVal);
            Assert.EndsWith(");", outVal.Trim());
        }

        [Fact]
        public void TestConvertToJavaScript_var_public()
        {
            var p = new Dictionary<string, string> { { "animal", "cat" } };
            string js = PropertyConverter.ConvertToJavaScript(p, "pubVar");
            Assert.StartsWith("var pubVar=", js);
            Assert.EndsWith(";", js.Trim());
        }

        [Fact]
        public void TestConvertToJavaScript_assignment_public()
        {
            var p = new Dictionary<string, string> { { "animal", "dog" } };
            string js = PropertyConverter.ConvertToJavaScript(p, "globals.pet");
            Assert.DoesNotContain("var ", js);
            Assert.StartsWith("globals.pet=", js);
            Assert.EndsWith(";", js.Trim());
        }

        [Fact]
        public void TestConvertToJson_withMixedTypes_public()
        {
            var p = new Dictionary<string, string>
            {
                { "note", "hello" },
                { "age", "30" },
                { "pi", "3.1416" },
                { "success", "true" },
                { "error", "false" }
            };
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Contains(@"""note"":""hello""", json);
            Assert.Contains(@"""age"":30", json);
            Assert.Contains(@"""pi"":3.1416", json);
            Assert.Contains(@"""success"":true", json);
            Assert.Contains(@"""error"":false", json);
        }

        [Fact]
        public void TestConvertToJson_handlesEmptyProperties_public()
        {
            var p = new Dictionary<string, string>();
            string json = PropertyConverter.ConvertToJson(p);
            Assert.Equal("{}", json);
        }
    }
}