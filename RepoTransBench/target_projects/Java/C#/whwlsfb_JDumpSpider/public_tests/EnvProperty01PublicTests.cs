using System;
using System.Collections;
using System.Collections.Generic;
using whwlsfb_JDumpSpider;
using whwlsfb_JDumpSpider.Spider;
using Xunit;

namespace whwlsfb_JDumpSpider.Tests.Public
{
    public class EnvProperty01PublicTests
    {
        public class PublicDummyHeapHolder : IHeapHolder
        {
            public object FindClass(string var1) => var1 == "java.lang.PublicProcessEnvironment" ? this : null;
            public IEnumerator GetClasses() => null;
            public bool IsInstanceOf(object javaClass, string className) => false;
            public bool IsArray(object javaClass) => false;
            public object[] GetSubClasses(object javaClass) => new object[0];
            public List<object> GetInstances(object javaClass)
            {
                return new List<object> { new object(), new object() };
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
                return new Dictionary<string, string> { { "PUBLIC_ENV", "VALUE42" } };
            }
            public object[] GetArrayItems(object instance) => new object[0];
            public string GetFieldStringValue(object instance, string fieldName) => null;
            public object GetFieldValue(object instance, string fieldName) => null;
            public bool IsMap(object instance) => instance is IDictionary;
            public object GetMap(object instance) => new Dictionary<string, string>();
            public string ToString(object instance) => null;
            public byte[] ToByteArray(object _instance) => new byte[0];
        }

        [Fact]
        public void TestGetNamePublic()
        {
            var env = new EnvProperty01();
            Assert.Equal("ProcessEnvironment", env.GetName());
        }

        [Fact]
        public void TestSniffHappyPathPublic()
        {
            var env = new EnvProperty01();
            PublicDummyHeapHolder heapHolder = new PublicDummyHeapHolder();
            string s = env.Sniff(heapHolder);
            Assert.Contains("PUBLIC_ENV", s);
            Assert.Contains("VALUE42", s);
        }

        [Fact]
        public void TestSniffHandlesExceptionPublic()
        {
            var env = new EnvProperty01();
            IHeapHolder heapHolder = new PublicDummyHeapHolderThrows();
            env.Sniff(heapHolder); // should not throw!
        }

        [Fact]
        public void TestSniffNoClassFoundPublic()
        {
            var env = new EnvProperty01();
            IHeapHolder heapHolder = new NoClassHeapHolder();
            Assert.Null(env.Sniff(heapHolder));
        }

        // Helper classes
        public class PublicDummyHeapHolderThrows : PublicDummyHeapHolder
        {
            public override object GetMap(object instance) { throw new Exception("bad_public"); }
        }

        public class NoClassHeapHolder : PublicDummyHeapHolder
        {
            public override object FindClass(string var1) { return null; }
        }
    }
}