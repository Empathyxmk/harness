using Xunit;
using System.IO;
using System;
using System.Linq;
using System.Runtime.Serialization.Formatters.Binary;
using Jude95_Utils;

namespace Jude95_Utils.Tests
{
    public class JFileManagerTest
    {
        enum Dir { TEST }

        private static DirectoryInfo tempDir;

        public class DummyContext
        {
            public DirectoryInfo GetFilesDir() => tempDir;
        }

        [Serializable]
        public class TestObj
        {
            public int x;
            public TestObj(int x) { this.x = x; }
        }

        public JFileManagerTest()
        {
            // Required for [Fact] instance
        }

        static JFileManagerTest()
        {
            tempDir = Directory.CreateDirectory(Path.Combine(Path.GetTempPath(), "jfilemanager_test_" + Guid.NewGuid()));
        }

        ~JFileManagerTest()
        {
            if (tempDir != null && tempDir.Exists)
            {
                foreach (var file in tempDir.GetFiles())
                {
                    file.Delete();
                }
                foreach (var dir in tempDir.GetDirectories())
                {
                    dir.Delete(true);
                }
                tempDir.Delete(true);
            }
        }

        [Fact]
        public void TestInitAndGetFolder()
        {
            var mgr = JFileManager.GetInstance();
            mgr.Init(new DummyContext(), Enum.GetValues(typeof(Dir)));
            var folder = mgr.GetFolder(Dir.TEST);
            Assert.NotNull(folder);
            Assert.True(folder.GetFile().Exists);
        }

        [Fact]
        public void TestWriteAndReadString()
        {
            var mgr = JFileManager.GetInstance();
            mgr.Init(new DummyContext(), Enum.GetValues(typeof(Dir)));
            var folder = mgr.GetFolder(Dir.TEST);

            folder.WriteStringToFile("hello world", "string.txt");
            var read = folder.ReadStringFromFile("string.txt");
            Assert.Equal("hello world", read);

            Assert.Null(folder.ReadStringFromFile("not_exist.txt"));
        }

        [Fact]
        public void TestWriteAndReadObject()
        {
            var mgr = JFileManager.GetInstance();
            mgr.Init(new DummyContext(), Enum.GetValues(typeof(Dir)));
            var folder = mgr.GetFolder(Dir.TEST);

            TestObj obj = new TestObj(1234);
            folder.WriteObjectToFile(obj, "obj.bin");

            var read = folder.ReadObjectFromFile<TestObj>("obj.bin");
            Assert.Equal(1234, read.x);

            folder.DeleteChild("obj.bin");
            Assert.ThrowsAny<Exception>(() => folder.ReadObjectFromFile<TestObj>("obj.bin"));
        }

        [Fact]
        public void TestListAndDeleteChild()
        {
            var mgr = JFileManager.GetInstance();
            mgr.Init(new DummyContext(), Enum.GetValues(typeof(Dir)));
            var folder = mgr.GetFolder(Dir.TEST);

            folder.WriteStringToFile("data1", "f1.txt");
            folder.WriteStringToFile("data2", "f2.txt");
            Assert.Equal(2, folder.ListChildFile().Length);

            folder.DeleteChild("f1.txt");
            Assert.Equal(1, folder.ListChildFile().Length);
        }

        [Fact]
        public void TestClearAllData()
        {
            var mgr = JFileManager.GetInstance();
            mgr.Init(new DummyContext(), Enum.GetValues(typeof(Dir)));
            var folder = mgr.GetFolder(Dir.TEST);
            folder.WriteStringToFile("t", "f.txt");
            Assert.True(folder.GetChildFile("f.txt").Exists);
            mgr.ClearAllData();
            Assert.False(folder.GetChildFile("f.txt").Exists);
        }
    }
}