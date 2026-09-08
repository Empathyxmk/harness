using Xunit;
using Vatri.Ecommerce.Storage;
using System.IO;
using System.Linq;
using System;
using Microsoft.AspNetCore.Http;
using Moq;

namespace PublicTests
{
    public class FileSystemStorageServicePublicTest : IDisposable
    {
        private readonly string _testLocation = "test-public-upload-dir";
        public FileSystemStorageServicePublicTest()
        {
            if (!Directory.Exists(_testLocation))
                Directory.CreateDirectory(_testLocation);
        }

        public void Dispose()
        {
            if (Directory.Exists(_testLocation))
            {
                foreach (var file in Directory.EnumerateFiles(_testLocation, "*", SearchOption.AllDirectories))
                    File.Delete(file);
                Directory.Delete(_testLocation, true);
            }
        }

        [Fact]
        public void TestStoreAndLoadPublicFile()
        {
            var properties = new StorageProperties();
            properties.SetLocation(_testLocation);
            var storageService = new FileSystemStorageService(properties);
            storageService.Init();

            var fileMock = new Mock<IFormFile>();
            fileMock.Setup(f => f.FileName).Returns("publicfile.txt");
            fileMock.Setup(f => f.Length).Returns(18);
            fileMock.Setup(f => f.CopyTo(It.IsAny<Stream>()))
                                .Callback<Stream>(s => { var b = System.Text.Encoding.UTF8.GetBytes("test public content"); s.Write(b, 0, b.Length); });

            var storedFileName = storageService.Store(fileMock.Object, "publicfile.txt");
            Assert.Equal("publicfile.txt", storedFileName);

            var loadedPath = storageService.Load("publicfile.txt");
            Assert.Equal(Path.Combine(_testLocation, "publicfile.txt"), loadedPath);

            var resource = storageService.LoadAsResource("publicfile.txt");
            Assert.NotNull(resource);
            Assert.True(resource.Exists);

            // Test loadAll returns our uploaded file
            Assert.True(storageService.LoadAll().Any(x => x == "publicfile.txt"));
        }

        [Fact]
        public void TestDeleteAllPublic()
        {
            var properties = new StorageProperties();
            properties.SetLocation(_testLocation);
            var storageService = new FileSystemStorageService(properties);
            storageService.Init();

            var filePath = Path.Combine(_testLocation, "todelete-public.txt");
            File.WriteAllText(filePath, "dummy");
            Assert.True(File.Exists(filePath));
            storageService.DeleteAll();
            Assert.False(File.Exists(filePath));
        }
    }
}