using System;
using System.Collections;
using System.Collections.Generic;
using whwlsfb_JDumpSpider;
using whwlsfb_JDumpSpider.Spider;
using Xunit;

namespace whwlsfb_JDumpSpider.Tests.Public
{
    public class DataSource04PublicTests
    {
        public class PublicDummyHeapHolder : IHeapHolder
        {
            public object FindClass(string var1) => var1.Contains("AnotherDruidDataSourceWrapper") ? this : null;
            public IEnumerator GetClasses() => null;
            public bool IsInstanceOf(object javaClass, string className) => true;
            public bool IsArray(object javaClass) => true;
            public object[] GetSubClasses(object javaClass) => new object[] { "pubsub" };
            public List<object> GetInstances(object javaClass) => new List<object> { new object(), new object() };
            public List<object> GetFields(object javaClass) => new List<object> { "pubfield" };
            public string GetClassName(object javaClass) => "pubClazz";
            public object GetSuperClass(object javaClass) => null;
            public string GetFieldName(object field) => "";
            public object GetFieldClass(object field) => "";
            public object FindThing(long objectId) => null;
            public object GetValueOfField(object instance, string fieldName) => null;
            public Dictionary<string, string> GetFieldsByNameList(object instance, Dictionary<string, string> fieldList)
                => new Dictionary<string, string> { { "username", "pubuser" }, { "password", "pubpass" }, { "jdbcUrl", "jdbc:oracle://newhost/db" } };
            public Dictionary<string, string> ArrayDump(object instance) => new Dictionary<string, string>();
            public object[] GetArrayItems(object instance) => new object[0];
            public string GetFieldStringValue(object instance, string fieldName) => "";
            public object GetFieldValue(object instance, string fieldName) => null;
            public bool IsMap(object instance) => false;
            public object GetMap(object instance) => null;
            public string ToString(object instance) => "";
            public byte[] ToByteArray(object _instance) => new byte[0];
        }

        [Fact]
        public void TestGetNamePublic()
        {
            var ds = new DataSource04();
            Assert.Equal("AliDruidDataSourceWrapper", ds.GetName());
        }

        [Fact]
        public void TestSniffNoClassFoundPublic()
        {
            var ds = new DataSource04();
            IHeapHolder dummy = new NoClassHeapHolder();
            Assert.Null(ds.Sniff(dummy));
        }

        [Fact]
        public void TestSniffHappyPathPublic()
        {
            var ds = new DataSource04();
            PublicDummyHeapHolder heapHolder = new PublicDummyHeapHolder();
            string result = ds.Sniff(heapHolder);
            Assert.Contains("pubuser", result);
            Assert.Contains("pubpass", result);
            Assert.Contains("jdbc:oracle://newhost/db", result);
        }

        [Fact]
        public void TestSniffHandlesExceptionPublic()
        {
            var ds = new DataSource04();
            IHeapHolder heapHolder = new PublicDummyHeapHolderThrows();
            ds.Sniff(heapHolder);
        }

        public class NoClassHeapHolder : IHeapHolder
        {
            public object FindClass(string var1) => null;
            public IEnumerator GetClasses() => null;
            public bool IsInstanceOf(object javaClass, string className) => false;
            public bool IsArray(object javaClass) => false;
            public object[] GetSubClasses(object javaClass) => new object[0];
            public List<object> GetInstances(object javaClass) => new List<object>();
            public List<object> GetFields(object javaClass) => new List<object>();
            public string GetClassName(object javaClass) => null;
            public object GetSuperClass(object javaClass) => null;
            public string GetFieldName(object field) => null;
            public object GetFieldClass(object field) => null;
            public object FindThing(long objectId) => null;
            public object GetValueOfField(object instance, string fieldName) => null;
            public Dictionary<string, string> GetFieldsByNameList(object instance, Dictionary<string, string> fieldList) => new Dictionary<string, string>();
            public Dictionary<string, string> ArrayDump(object instance) => new Dictionary<string, string>();
            public object[] GetArrayItems(object instance) => new object[0];
            public string GetFieldStringValue(object instance, string fieldName) => null;
            public object GetFieldValue(object instance, string fieldName) => null;
            public bool IsMap(object instance) => false;
            public object GetMap(object instance) => null;
            public string ToString(object instance) => null;
            public byte[] ToByteArray(object _instance) => new byte[0];
        }

        public class PublicDummyHeapHolderThrows : PublicDummyHeapHolder
        {
            public override List<object> GetInstances(object javaClass) { throw new Exception("publicFail"); }
        }
    }
}