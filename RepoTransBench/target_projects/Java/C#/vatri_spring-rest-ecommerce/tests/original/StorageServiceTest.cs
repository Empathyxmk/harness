using Xunit;
using System;
using System.Linq;
using Vatri.Ecommerce.Storage;

namespace OriginalTests
{
    public class StorageServiceTest
    {
        [Fact]
        public void DummyInterfaceImplementation()
        {
            // Since StorageService is an interface, ensure that it can be implemented
            var s = new MyStorageService();
            Assert.NotNull(s);
            var ex = Record.Exception(() => s.Init());
            Assert.Null(ex);
            Assert.Equal("ok", s.Store(null, ""));
            Assert.NotNull(s.LoadAll());
            Assert.Null(s.Load(""));
            Assert.Null(s.LoadAsResource(""));
            ex = Record.Exception(() => s.DeleteAll());
            Assert.Null(ex);
        }

        private class MyStorageService : IStorageService
        {
            public void Init() { }
            public string Store(Microsoft.AspNetCore.Http.IFormFile f, string s) => "ok";
            public System.Collections.Generic.IEnumerable<string> LoadAll() => Enumerable.Empty<string>();
            public string Load(string file) => null;
            public Microsoft.Extensions.FileProviders.IFileInfo LoadAsResource(string file) => null;
            public void DeleteAll() { }
        }
    }
}