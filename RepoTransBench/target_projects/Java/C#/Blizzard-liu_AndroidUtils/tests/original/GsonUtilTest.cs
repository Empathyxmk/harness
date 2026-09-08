using System;
using System.Collections.Generic;
using System.Text.Json;
using Xunit;

namespace AndroidUtils.Tests
{
    public class GsonUtilTest
    {
        [Fact]
        public void TestParseMapToJson_ValidMap()
        {
            var map = new Dictionary<string, string> { { "foo", "bar" } };
            string json = GsonUtil.ParseMapToJson(map);
            Assert.Contains("\"foo\":\"bar\"", json);
        }

        [Fact]
        public void TestParseMapToJson_NullMap()
        {
            string json = GsonUtil.ParseMapToJson<string, string>(null);
            Assert.Equal("null", json);
        }

        [Fact]
        public void TestParseJsonToBean_ValidJson()
        {
            string json = "{\"name\":\"Alice\", \"age\":30}";
            var bean = GsonUtil.ParseJsonToBean<TestBean>(json);
            Assert.NotNull(bean);
            Assert.Equal("Alice", bean.Name);
            Assert.Equal(30, bean.Age);
        }

        [Fact]
        public void TestParseJsonToBean_InvalidJson()
        {
            string json = "{name:Alice, age:30}";
            var bean = GsonUtil.ParseJsonToBean<TestBean>(json);
            Assert.Null(bean);
        }

        [Fact]
        public void TestParseJsonToMap_ValidJson()
        {
            string json = "{\"foo\":\"bar\",\"num\":42}";
            var map = GsonUtil.ParseJsonToMap(json);
            Assert.Equal("bar", map["foo"].ToString());
            Assert.True(Math.Abs(Convert.ToDouble(map["num"]) - 42) < 0.01);
        }

        [Fact]
        public void TestParseJsonToMap_InvalidJson()
        {
            string json = "{foo:bar,num:42}";
            var map = GsonUtil.ParseJsonToMap(json);
            Assert.Null(map);
        }

        [Fact]
        public void TestParseJsonToList_Valid()
        {
            var expected = new List<TestBean>
            {
                new TestBean("A", 1),
                new TestBean("B", 2)
            };
            string json = "[{\"name\":\"A\",\"age\":1},{\"name\":\"B\",\"age\":2}]";
            var result = GsonUtil.ParseJsonToList<TestBean>(json);
            Assert.Equal(2, result.Count);
            Assert.Equal("A", result[0].Name);
            Assert.Equal(1, result[0].Age);
        }

        [Fact]
        public void TestParseJsonToList_Invalid()
        {
            string json = "[{name:A,age:1},{name:B,age:2}]";
            Assert.ThrowsAny<Exception>(() =>
            {
                GsonUtil.ParseJsonToList<TestBean>(json);
            });
        }

        [Fact]
        public void TestGetFieldValue_Valid()
        {
            string json = "{\"key\":\"value\",\"other\":\"x\"}";
            Assert.Equal("value", GsonUtil.GetFieldValue(json, "key"));
        }

        [Fact]
        public void TestGetFieldValue_KeyNotPresent()
        {
            string json = "{\"key1\":\"value1\"}";
            Assert.Equal("", GsonUtil.GetFieldValue(json, "missing"));
        }

        [Fact]
        public void TestGetFieldValue_EmptyJson()
        {
            Assert.Null(GsonUtil.GetFieldValue("", "foo"));
        }

        [Fact]
        public void TestGetFieldValue_InvalidJson()
        {
            string json = "{key:value}";
            Assert.Null(GsonUtil.GetFieldValue(json, "key"));
        }

        public class TestBean
        {
            public string Name { get; set; } = "";
            public int Age { get; set; } = 0;
            public TestBean() { }
            public TestBean(string n, int a)
            {
                Name = n;
                Age = a;
            }
        }
    }

    public static class GsonUtil
    {
        public static string ParseMapToJson<TKey, TValue>(Dictionary<TKey, TValue> map)
        {
            if (map == null) return "null";
            return JsonSerializer.Serialize(map);
        }
        public static T ParseJsonToBean<T>(string json)
        {
            try
            {
                return JsonSerializer.Deserialize<T>(json);
            }
            catch
            {
                return default(T);
            }
        }
        public static Dictionary<string, object> ParseJsonToMap(string json)
        {
            try
            {
                return JsonSerializer.Deserialize<Dictionary<string, object>>(json);
            }
            catch
            {
                return null;
            }
        }
        public static List<T> ParseJsonToList<T>(string json)
        {
            return JsonSerializer.Deserialize<List<T>>(json);
        }
        public static string GetFieldValue(string json, string key)
        {
            if (string.IsNullOrEmpty(json)) return null;
            try
            {
                var dict = JsonSerializer.Deserialize<Dictionary<string, object>>(json);
                if (dict != null && dict.ContainsKey(key))
                    return dict[key]?.ToString() ?? "";
                else if (dict != null)
                    return "";
            }
            catch
            {
                return null;
            }
            return null;
        }
    }
}