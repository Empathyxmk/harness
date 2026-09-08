using System;
using Xunit;
using FluentAssertions;

namespace PilgrPaper.PublicTests
{
    public class CustomBookPublicTest : IDisposable
    {
        public CustomBookPublicTest()
        {
            Paper.Init();
        }

        [Fact]
        public void GetFolderPathForBookCustomPublic()
        {
            var path = Paper.Book("public_custom").GetPath();
            path.Should().EndWith("/io.paperdb.test/files/public_custom");
        }

        [Fact]
        public void GetFilePathForKeyCustomBookPublic()
        {
            var path = Paper.Book("public_custom").GetPath("my_val");
            path.Should().EndWith("/io.paperdb.test/files/public_custom/my_val.pt");
        }

        [Fact]
        public void ReadWriteDeleteToDifferentBooksPublic()
        {
            var publicBook = "public_custom";
            Paper.Book().Destroy();
            Paper.Book(publicBook).Destroy();

            Paper.Book().Write("country", "Denmark");
            Paper.Book(publicBook).Write("country", "Norway");

            Paper.Book().Read<string>("country").Should().Be("Denmark");
            Paper.Book(publicBook).Read<string>("country").Should().Be("Norway");

            Paper.Book().Delete("country");
            Paper.Book().Contains("country").Should().BeFalse();
            Paper.Book(publicBook).Contains("country").Should().BeTrue();
        }

        public void Dispose()
        {
        }
    }
}