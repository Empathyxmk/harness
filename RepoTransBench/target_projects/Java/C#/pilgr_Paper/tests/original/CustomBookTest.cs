using System;
using Xunit;
using FluentAssertions;

namespace PilgrPaper.OriginalTests
{
    public class CustomBookTest : IDisposable
    {
        public CustomBookTest()
        {
            Paper.Init();
        }

        [Fact]
        public void GetFolderPathForBookCustom()
        {
            var path = Paper.Book("custom").GetPath();
            path.Should().EndWith("/io.paperdb.test/files/custom");
        }

        [Fact]
        public void GetFilePathForKeyCustomBook()
        {
            var path = Paper.Book("custom").GetPath("my_key");
            path.Should().EndWith("/io.paperdb.test/files/custom/my_key.pt");
        }

        [Fact]
        public void ReadWriteDeleteToDifferentBooks()
        {
            string custom = "custom";
            Paper.Book().Destroy();
            Paper.Book(custom).Destroy();

            Paper.Book().Write("city", "Victoria");
            Paper.Book(custom).Write("city", "Kyiv");

            Paper.Book().Read<string>("city").Should().Be("Victoria");
            Paper.Book(custom).Read<string>("city").Should().Be("Kyiv");

            Paper.Book().Delete("city");
            Paper.Book().Contains("city").Should().BeFalse();
            Paper.Book(custom).Contains("city").Should().BeTrue();
        }

        public void Dispose()
        {
        }
    }
}