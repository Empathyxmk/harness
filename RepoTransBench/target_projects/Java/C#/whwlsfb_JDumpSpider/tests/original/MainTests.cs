using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using whwlsfb_JDumpSpider;
using Xunit;

namespace whwlsfb_JDumpSpider.Tests.Original
{
    public class DummyHeapHolder : IHeapHolder
    {
        public object FindClass(string var1) => "dummyClass";
        public IEnumerator GetClasses() => ((IEnumerable)new List<object>()).GetEnumerator();
        public bool IsInstanceOf(object javaClass, string className) => false;
        public bool IsArray(object javaClass) => false;
        public object[] GetSubClasses(object javaClass) => new object[0];
        public List<object> GetInstances(object javaClass) => new List<object>();
        public List<object> GetFields(object javaClass) => new List<object>();
        public string GetClassName(object javaClass) => "dummyClass";
        public object GetSuperClass(object javaClass) => null;
        public string GetFieldName(object field) => "";
        public object GetFieldClass(object field) => "";
        public object FindThing(long objectId) => null;
        public object GetValueOfField(object instance, string fieldName) => null;
        public Dictionary<string, string> GetFieldsByNameList(object instance, Dictionary<string, string> fieldList)
        {
            return new Dictionary<string, string> { { "username", "u" }, { "password", "p" }, { "jdbcUrl", "j" } };
        }
        public Dictionary<string, string> ArrayDump(object instance) => new Dictionary<string, string>();
        public object[] GetArrayItems(object instance) => new object[0];
        public string GetFieldStringValue(object instance, string fieldName) => "";
        public object GetFieldValue(object instance, string fieldName) => null;
        public bool IsMap(object instance) => false;
        public object GetMap(object instance) => new Dictionary<string, string>();
        public string ToString(object instance) => "";
        public byte[] ToByteArray(object _instance) => new byte[0];
    }

    public class DummySpider : ISpider
    {
        public string GetName() => "dummy";
        public string Sniff(IHeapHolder heapHolder) => "sniffed";
    }

    public class MainTests
    {
        [Fact]
        public void TestRunWithNoArgsShowsMessage()
        {
            var output = Main.Run(new string[] { });
            Assert.Contains("please give a heap filepath", output);
        }

        [Fact]
        public void TestRunWithNonexistentFileShowsMessage()
        {
            string[] args = { "nonexistent_file.hprof" };
            var output = Main.Run(args);
            Assert.Contains("file not exist", output);
        }

        [Fact]
        public void TestRunAsyncRequiresResultPath()
        {
            string output = Main.RunAsync(new string[] { "heap.hprof" });
            Assert.Contains("must give a result file path", output);
        }

        [Fact]
        public void TestGetArgValueThrowsOnError()
        {
            var m = new Main();
            // Simulate the -out arg present but no value after
            FieldInfo f = typeof(Main).GetField("flag", BindingFlags.NonPublic | BindingFlags.Instance);
            var flist = new List<string>() { "-out" };
            f.SetValue(m, flist);
            Exception ex = Assert.ThrowsAny<Exception>(() =>
            {
                MethodInfo mi = typeof(Main).GetMethod("GetArgValue", BindingFlags.NonPublic | BindingFlags.Instance);
                mi.Invoke(m, new object[] { "-out" });
            });
            Assert.Contains("Get '-out' value failed", ex.Message);
        }

        [Fact]
        public void TestGetFileVersionBadFile()
        {
            var m = new Main();
            FieldInfo field = typeof(Main).GetField("heapfile", BindingFlags.NonPublic | BindingFlags.Instance);
            field.SetValue(m, new FileInfo("nope.file.that.is.never.there"));
            Assert.ThrowsAny<Exception>(() =>
            {
                m.GetFileVersion();
            });
        }
    }
}