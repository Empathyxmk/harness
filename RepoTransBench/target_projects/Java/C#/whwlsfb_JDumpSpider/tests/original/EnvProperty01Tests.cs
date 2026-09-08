using System;
using System.Collections;
using System.Collections.Generic;
using whwlsfb_JDumpSpider;
using whwlsfb_JDumpSpider.Spider;
using Xunit;

namespace whwlsfb_JDumpSpider.Tests.Original
{
    public class EnvProperty01Tests
    {
        public class DummyHeapHolder : IHeapHolder
        {
            public object FindClass(string var1) => var1 == "java.lang.ProcessEnvironment" ? this : null;
            public IEnumerator GetClasses() => null;
            public bool IsInstanceOf(object javaClass, string className) => false;
            public bool IsArray(object javaClass) => false;
            public object[] GetSubClasses(object javaClass) => new object[0];
            public List<object> GetInstances(object javaClass)
            {
                return new List<object> { new object() };
            }
            public List<object> GetFields(object javaClass) => new List<object>();
            public string GetClassName(object javaClass) => null;
            public object GetSuperClass(object javaClass) => null;
            public string GetFieldName(object field) => null;
            public object GetFieldClass(object field) => null;
            public object FindThing(long objectId) => null;
            public object GetValueOfField(object instance, string fieldName) => null;
            public Dictionary<string, string> GetFieldsByNameList(object instance, Dictionary<string, string> fieldList) => new Dictionary<string, string>();
            public Dictionary<string, string> ArrayDump(object instance)
            {
                return new Dictionary<string, string> { { "ENVVAR", "VAL" } };
            }
            public object[] GetArrayItems(object instance) => new object[0];
            public string GetFieldStringValue(object instance, string fieldName) => null;
            public object GetFieldValue(object instance, string fieldName) => null;
            public bool IsMap(object instance) => instance is IDictionary;
            public object GetMap(object instance) => new object();
            public string ToString(object instance) => null;
            public byte[] ToByteArray(object _instance) => new byte[0];
        }

        [Fact]
        public void TestGetName()
        {
            var env = new EnvProperty01();
            Assert.Equal("ProcessEnvironment", env.GetName());
        }

        [Fact]
        public void TestSniffHappyPath()
        {
            var env = new EnvProperty01();
            DummyHeapHolder heapHolder = new DummyHeapHolder();
            string s = env.Sniff(heapHolder);
            Assert.Contains("ENVVAR", s);
            Assert.Contains("VAL", s);
        }

        [Fact]
        public void TestSniffHandlesException()
        {
            var env = new EnvProperty01();
            IHeapHolder heapHolder = new DummyHeapHolderThrows();
            env.Sniff(heapHolder); // should not throw!
        }

        [Fact]
        public void TestSniffNoClassFound()
        {
            var env = new EnvProperty01();
            IHeapHolder heapHolder = new NoClassHeapHolder();
            Assert.Null(env.Sniff(heapHolder));
        }

        // Helper classes
        public class DummyHeapHolderThrows : DummyHeapHolder
        {
            public override object GetMap(object instance) { throw new Exception("bad"); }
        }

        public class NoClassHeapHolder : DummyHeapHolder
        {
            public override object FindClass(string var1) { return null; }
        }
    }
}