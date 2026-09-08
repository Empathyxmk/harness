using System.Collections.Generic;
using Xunit;

namespace SansOrm.Tests.Public
{
    public class OrmElfPublicTest
    {
        [Fact]
        public void TestUnderlineToCamelPublic()
        {
            Assert.Equal("snakeCaseField", OrmBase.UnderlineToCamel("snake_case_field"));
            Assert.Equal("anotherExample", OrmBase.UnderlineToCamel("another_example"));
            Assert.Equal("simpleTest", OrmBase.UnderlineToCamel("simple_test"));
        }

        [Fact]
        public void TestCamelToUnderlinePublic()
        {
            Assert.Equal("user_name", OrmBase.CamelToUnderline("userName"));
            Assert.Equal("test_data", OrmBase.CamelToUnderline("testData"));
            Assert.Equal("red_blue_green", OrmBase.CamelToUnderline("redBlueGreen"));
        }

        [Fact]
        public void TestJoinPublic()
        {
            var items = new List<string> { "a", "b", "c" };
            Assert.Equal("a,b,c", OrmBase.Join(items, ","));
            Assert.Equal("a|b|c", OrmBase.Join(items, "|"));
            Assert.Equal("abc", OrmBase.Join(items, ""));
        }
    }

    public static class OrmBase
    {
        public static string UnderlineToCamel(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            var parts = str.Split('_');
            for (int i = 1; i < parts.Length; i++)
                parts[i] = char.ToUpper(parts[i][0]) + parts[i].Substring(1);
            return string.Join("", parts);
        }

        public static string CamelToUnderline(string str)
        {
            if (string.IsNullOrEmpty(str)) return str;
            var res = new List<char> { char.ToLower(str[0]) };
            for (int i = 1; i < str.Length; i++)
            {
                if (char.IsUpper(str[i])) { res.Add('_'); res.Add(char.ToLower(str[i])); }
                else res.Add(str[i]);
            }
            return new string(res.ToArray());
        }

        public static string Join(IEnumerable<string> items, string delimiter)
        {
            return string.Join(delimiter, items);
        }
    }
}