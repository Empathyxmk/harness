using Xunit;
using System.Linq;
using Vatri.Ecommerce.Storage;

namespace PublicTests
{
    public class StorageServicePublicTest
    {
        [Fact]
        public void DummyInterfaceImplementationDifferentData()
        {
            var s = new MyStorageService();
            Assert.NotNull(s);
            var ex = Record.Exception(() => s.Init());
            Assert.Null(ex);
            Assert.Equal("public-ok", s.Store(null, "public"));
            Assert.True(s.LoadAll().Any());
            Assert.Equal("publicfile", s.Load("public"));
            Assert.Null(s.LoadAsResource("public"));
            ex = Record.Exception(() => s.DeleteAll());
            Assert.Null(ex);
        }

        private class MyStorageService : IStorageService
        {
            public void Init() { }
            public string Store(Microsoft.AspNetCore.Http.IFormFile f, string s) => "public-ok";
            public System.Collections.Generic.IEnumerable<string> LoadAll() => new[] { "publicfile" };
            public string Load(string file) => "publicfile";
            public Microsoft.Extensions.FileProviders.IFileInfo LoadAsResource(string file) => null;
            public void DeleteAll() { }
        }
    }
}