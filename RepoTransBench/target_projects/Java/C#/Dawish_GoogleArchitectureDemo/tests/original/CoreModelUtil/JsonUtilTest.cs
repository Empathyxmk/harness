using System;
using System.Collections.Generic;
using Xunit;
using Newtonsoft.Json;

namespace DawishGoogleArchitectureDemo.Tests.Original.CoreModelUtil
{
    public class JsonUtilTest
    {
        public class Bean : IEquatable<Bean>
        {
            public string field1 { get; set; }
            public int field2 { get; set; }

            public Bean() { }

            public Bean(string f1, int f2)
            {
                field1 = f1;
                field2 = f2;
            }

            public bool Equals(Bean other)
            {
                if (other is null) return false;
                return (field1 == null ? other.field1 == null : field1 == other.field1)
                    && field2 == other.field2;
            }

            public override bool Equals(object obj) => Equals(obj as Bean);
            public override int GetHashCode() => (field1, field2).GetHashCode();
        }

        [Fact]
        public void Str2JsonBean_ValidJson()
        {
            string json = "{\"field1\":\"test\",\"field2\":123}";
            Bean bean = JsonUtil.Str2JsonBean<Bean>(json);
            Assert.NotNull(bean);
            Assert.Equal("test", bean.field1);
            Assert.Equal(123, bean.field2);
        }

        [Fact]
        public void Str2JsonBean_InvalidJson()
        {
            string json = "{field1:test,field2:abc}";
            Bean bean = JsonUtil.Str2JsonBean<Bean>(json);
            Assert.Null(bean);
        }

        [Fact]
        public void JsonBean2Str_Valid()
        {
            Bean bean = new Bean("abc", 42);
            string json = JsonUtil.JsonBean2Str(bean);
            Assert.NotNull(json);
            Assert.Contains("\"field1\":\"abc\"", json);
            Assert.Contains("\"field2\":42", json);
        }

        [Fact]
        public void JsonBean2Str_Null()
        {
            string jsonNull = JsonUtil.JsonBean2Str<Bean>(null);
            Assert.Equal("null", jsonNull);
        }

        [Fact]
        public void JsonList2Str_EmptyList()
        {
            string res = JsonUtil.JsonList2Str(new List<Bean>());
            Assert.Null(res);
        }

        [Fact]
        public void JsonList2Str_Multiple()
        {
            Bean b1 = new Bean("a", 1);
            Bean b2 = new Bean("b", 2);
            string res = JsonUtil.JsonList2Str(new List<Bean> { b1, b2 });
            Assert.NotNull(res);
            Assert.StartsWith("[", res);
            Assert.EndsWith("]", res);
            Assert.Contains("\"field1\":\"a\"", res);
            Assert.Contains("\"field1\":\"b\"", res);
            Assert.Contains(",", res);
        }
    }

    public static class JsonUtil
    {
        public static T Str2JsonBean<T>(string json) where T : class
        {
            try
            {
                return JsonConvert.DeserializeObject<T>(json);
            }
            catch
            {
                return null;
            }
        }

        public static string JsonBean2Str<T>(T bean)
        {
            if (bean == null)
                return "null";
            return JsonConvert.SerializeObject(bean);
        }

        public static string JsonList2Str<T>(List<T> list)
        {
            if (list == null || list.Count == 0)
                return null;
            return JsonConvert.SerializeObject(list);
        }
    }
}