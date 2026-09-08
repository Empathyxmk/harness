using Xunit;
using BlackObfuscatorASPlugin.Models;
using System.Collections.Generic;

namespace BlackObfuscatorASPlugin.PublicTests
{
    public class MappingPublicTests
    {
        [Fact]
        public void TestPutAndGetDifferentData()
        {
            var mapping = new Mapping();
            string className = "top.example2024.NewClass";
            string obfClassName = "aBcD_PUBLIC";
            mapping.PutClassMapping(className, obfClassName);
            Assert.Equal(obfClassName, mapping.GetObfuscatedClassName(className));

            string methodName = "publicMethod2024()V";
            string obfMethodName = "m2024";
            mapping.PutMethodMapping(className, methodName, obfMethodName);
            Assert.Equal(obfMethodName, mapping.GetObfuscatedMethodName(className, methodName));

            string fieldName = "publicField2024";
            string obfFieldName = "f2024";
            mapping.PutFieldMapping(className, fieldName, obfFieldName);
            Assert.Equal(obfFieldName, mapping.GetObfuscatedFieldName(className, fieldName));
        }

        [Fact]
        public void TestToMapDifferentData()
        {
            var mapping = new Mapping();
            mapping.PutClassMapping("ClassA2024", "XxYyZz");
            Dictionary<string, string> classMap = mapping.GetClassMapping();
            Assert.Equal("XxYyZz", classMap["ClassA2024"]);
            Assert.Contains("ClassA2024", classMap.Keys);
        }
    }
}