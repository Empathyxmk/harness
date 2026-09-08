using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using whwlsfb_JDumpSpider;
using Xunit;

namespace whwlsfb_JDumpSpider.Tests.Public
{
    public class PublicDummyHeapHolder : IHeapHolder
    {
        public object FindClass(string var1) => "publicDummyClass";
        public IEnumerator GetClasses() => ((IEnumerable)new List<object>()).GetEnumerator();
        public bool IsInstanceOf(object javaClass, string className) => true;
        public bool IsArray(object javaClass) => true;
        public object[] GetSubClasses(object javaClass) => new object[] { "sub1" };
        public List<object> GetInstances(object javaClass) => new List<object> { "instance" };
        public List<object> GetFields(object javaClass) => new List<object> { "field" };
        public string GetClassName(object javaClass) => "publicDummyClass";
        public object GetSuperClass(object javaClass) => "publicSuperClass";
        public string GetFieldName(object field) => "fieldName";
        public object GetFieldClass(object field) => "fieldClass";
        public object FindThing(long objectId) => "foundThing";
        public object GetValueOfField(object instance, string fieldName) => "valueOfField";
        public Dictionary<string, string> GetFieldsByNameList(object instance, Dictionary<string, string> fieldList)
        {
            return new Dictionary<string, string> { { "username", "publicU" }, { "password", "publicP" }, { "jdbcUrl", "jdbc:public" } };
        }
        public Dictionary<string, string> ArrayDump(object instance) => new Dictionary<string, string>();
        public object[] GetArrayItems(object instance) => new object[] { "item1", "item2" };
        public string GetFieldStringValue(object instance, string fieldName) => "stringValue";
        public object GetFieldValue(object instance, string fieldName) => "fieldValue";
        public bool IsMap(object instance) => true;
        public object GetMap(object instance) => new Dictionary<string, string>();
        public string ToString(object instance) => "toStringResult";
        public byte[] ToByteArray(object _instance) => new byte[] { 1, 2, 3 };
    }

    public class PublicDummySpider : ISpider
    {
        public string GetName() => "publicDummy";
        public string Sniff(IHeapHolder heapHolder) => "public_sniffed";
    }

    public class MainPublicTests
    {
        [Fact]
        public void TestRunWithHelpFlagShowsHelpMessage()
        {
            var output = Main.Run(new string[] { "-help" });
            Assert.Contains("usage", output);
        }

        [Fact]
        public void TestRunWithNonexistentFileShowsMessageDifferentName()
        {
            string[] args = { "totally_missing_file.hprof" };
            var output = Main.Run(args);
            Assert.Contains("file not exist", output.ToLower());
        }

        [Fact]
        public void TestRunAsyncRequiresResultPathDifferentHeap()
        {
            string output = Main.RunAsync(new string[] { "randomheap.hprof" });
            Assert.Contains("must give a result file path", output.ToLower());
        }

        [Fact]
        public void TestGetArgValueThrowsOnDifferentFlag()
        {
            var m = new Main();
            FieldInfo f = typeof(Main).GetField("flag", BindingFlags.NonPublic | BindingFlags.Instance);
            var flist = new List<string>() { "-in" };
            f.SetValue(m, flist);

            Exception ex = Assert.ThrowsAny<Exception>(() =>
            {
                MethodInfo mi = typeof(Main).GetMethod("GetArgValue", BindingFlags.NonPublic | BindingFlags.Instance);
                mi.Invoke(m, new object[] { "-in" });
            });
            Assert.Contains("get '-in' value failed", ex.Message.ToLower());
        }

        [Fact]
        public void TestGetFileVersionBadFileDifferent()
        {
            var m = new Main();
            FieldInfo field = typeof(Main).GetField("heapfile", BindingFlags.NonPublic | BindingFlags.Instance);
            field.SetValue(m, new FileInfo("definitely_nonexistent_file.file"));
            Assert.ThrowsAny<Exception>(() =>
            {
                m.GetFileVersion();
            });
        }
    }
}