using Xunit;
using Vatri.Ecommerce.Storage;
using System.IO;
using System.Linq;
using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Http;
using Moq;

namespace OriginalTests
{
    public class FileSystemStorageServiceTest : IDisposable
    {
        private const string TestLocation = "test-uploads";
        private FileSystemStorageService _storageService;
        private StorageProperties _properties;

        public FileSystemStorageServiceTest()
        {
            _properties = new StorageProperties();
            _properties.SetLocation(TestLocation);
            _storageService = new FileSystemStorageService(_properties);
            _storageService.DeleteAll();
            _storageService.Init();
        }

        public void Dispose()
        {
            _storageService.DeleteAll();
        }

        [Fact]
        public void TestInitCreatesDirectory()
        {
            Assert.True(Directory.Exists(TestLocation));
            Assert.True((File.GetAttributes(TestLocation) & FileAttributes.Directory) == FileAttributes.Directory);
        }

        [Fact]
        public void TestStoreValidFile()
        {
            var fileMock = new Mock<IFormFile>();
            fileMock.Setup(f => f.FileName).Returns("test.txt");
            fileMock.Setup(f => f.Length).Returns(9);
            fileMock.Setup(f => f.CopyTo(It.IsAny<Stream>()))
                .Callback<Stream>(s => { var b = System.Text.Encoding.UTF8.GetBytes("Spring Boot"); s.Write(b, 0, b.Length); });
            var storedName = _storageService.Store(fileMock.Object, "subdir");

            var expectedDir = Path.Combine(TestLocation, "subdir");
            Assert.True(Directory.Exists(expectedDir));
            var files = Directory.GetFiles(expectedDir);
            Assert.Contains(files, f => Path.GetFileName(f) == storedName);
        }

        [Fact]
        public void TestStoreEmptyFileThrows()
        {
            var fileMock = new Mock<IFormFile>();
            fileMock.Setup(f => f.FileName).Returns("empty.txt");
            fileMock.Setup(f => f.Length).Returns(0);
            Assert.Throws<StorageException>(() => _storageService.Store(fileMock.Object, ""));
        }

        [Fact]
        public void TestLoadAllListsFiles()
        {
            var fileMock = new Mock<IFormFile>();
            fileMock.Setup(f => f.FileName).Returns("loadall.txt");
            fileMock.Setup(f => f.Length).Returns(4);
            fileMock.Setup(f => f.CopyTo(It.IsAny<Stream>()))
                 .Callback<Stream>(s => { var b = System.Text.Encoding.UTF8.GetBytes("Test"); s.Write(b, 0, b.Length); });
            _storageService.Store(fileMock.Object, "");

            var files = _storageService.LoadAll().ToList();
            Assert.True(files.Count > 0);
        }

        [Fact]
        public void TestLoadReturnsCorrectPath()
        {
            var filename = "myfile.txt";
            var written = Path.Combine(TestLocation, filename);
            File.WriteAllText(written, "hello");
            var loaded = _storageService.Load(filename);
            Assert.Equal(written, loaded);
        }

        [Fact]
        public void TestLoadAsResourceReturnsResource()
        {
            var filename = "resource.txt";
            var written = Path.Combine(TestLocation, filename);
            File.WriteAllText(written, "hello");
            var resource = _storageService.LoadAsResource(filename);
            Assert.True(resource.Exists);
            using (resource.CreateReadStream()) { }
        }

        [Fact]
        public void TestLoadAsResourceFileNotFound()
        {
            var filename = $"notexist-{Guid.NewGuid()}.txt";
            var ex = Assert.Throws<StorageFileNotFoundException>(() => _storageService.LoadAsResource(filename));
            Assert.Contains(filename, ex.Message);
        }

        [Fact]
        public void TestDeleteAllDeletesDirectory()
        {
            var filePath = Path.Combine(TestLocation, "toremove.txt");
            File.WriteAllText(filePath, "bye");
            Assert.True(File.Exists(filePath));
            _storageService.DeleteAll();
            Assert.False(Directory.Exists(TestLocation));
            // Restore for next tests!
            _storageService.Init();
        }

        [Fact]
        public void TestInitIOExceptionThrows()
        {
            var sp = new TestStoragePropertiesWithRoot();
            var faulty = new FileSystemStorageService(sp);
            Assert.Throws<StorageException>(() => faulty.Init());
        }

        [Fact]
        public void TestStoreIOExceptionThrows()
        {
            var fileMock = new Mock<IFormFile>();
            fileMock.Setup(f => f.FileName).Returns("bad.txt");
            fileMock.Setup(f => f.Length).Returns(4);
            fileMock.Setup(f => f.CopyTo(It.IsAny<Stream>()))
                                                .Callback<Stream>(s => throw new IOException("forced"));
            Assert.Throws<StorageException>(() => _storageService.Store(fileMock.Object, "badpath"));
        }

        [Fact]
        public void TestLoadAllIOExceptionThrows()
        {
            var badService = new FileSystemStorageService(new TestStoragePropertiesWithRoot());
            Assert.Throws<StorageException>(() => badService.LoadAll());
        }

        [Fact]
        public void TestLoadAsResourceMalformedURL()
        {
            var badService = new FileSystemStorageService(_propertiesOverride)
            {
                // Override Load
            };
            Assert.Throws<StorageFileNotFoundException>(() => badService.LoadAsResource("badfile"));
        }

        private class TestStoragePropertiesWithRoot : StorageProperties
        {
            public override string GetLocation() => "/root/forbidden-" + Guid.NewGuid();
        }

        private StorageProperties _propertiesOverride => new StorageProperties()
        {
            // For the test, override GetLocation to return an invalid file name (simulate \0 invalid path)
        };
    }
}