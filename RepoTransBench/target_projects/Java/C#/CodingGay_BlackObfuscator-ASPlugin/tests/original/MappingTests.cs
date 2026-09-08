using Xunit;
using System.IO;
using BlackObfuscatorASPlugin.Models;
using System.Linq;

namespace BlackObfuscatorASPlugin.Tests.Original
{
    public class MappingTests : System.IDisposable
    {
        private string _mappingFile;

        public MappingTests()
        {
            _mappingFile = Path.GetTempFileName();
            File.WriteAllLines(_mappingFile, new[]
            {
                "# This is a comment",
                "com.abc.ClassA -> com.obf.X:",
                "  # Indented comment",
                "com.abc.ClassB -> com.obf.Y:",
                "bad mapping line",
                "com.abc.ClassC -> com.obf.Z:"
            });
        }

        [Fact]
        public void TestValidMappings()
        {
            var mapping = new Mapping(_mappingFile);
            Assert.Equal("com.obf.X", mapping.Get("com.abc.ClassA"));
            Assert.Equal("com.obf.Y", mapping.Get("com.abc.ClassB"));
            Assert.Equal("com.obf.Z", mapping.Get("com.abc.ClassC"));
            Assert.Null(mapping.Get("com.abc.NotExist"));
            Assert.True(mapping.GetMapping().Count >= 3);
        }

        [Fact]
        public void TestNullFile()
        {
            var m = new Mapping(null);
            Assert.NotNull(m.GetMapping());
            Assert.Empty(m.GetMapping());
        }

        [Fact]
        public void TestNonExistentFile()
        {
            var m = new Mapping("fakefile_doesnot_exist.txt");
            Assert.NotNull(m.GetMapping());
            Assert.Empty(m.GetMapping());
        }

        [Fact]
        public void TestMalformedLines()
        {
            string malformedFile = Path.GetTempFileName();
            try
            {
                File.WriteAllLines(malformedFile, new[]
                {
                    "malformed_line",
                    "com.onlyonepart -> ",
                    " -> onlysecondpart:",
                    "correct.package -> correct.target:"
                });
                var m = new Mapping(malformedFile);
                Assert.Equal("correct.target", m.Get("correct.package"));
            }
            finally
            {
                File.Delete(malformedFile);
            }
        }

        public void Dispose()
        {
            if (File.Exists(_mappingFile))
            {
                File.Delete(_mappingFile);
            }
        }
    }
}