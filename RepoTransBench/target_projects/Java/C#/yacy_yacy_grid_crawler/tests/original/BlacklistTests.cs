using System;
using System.IO;
using System.Text.RegularExpressions;
using Xunit;
using yacy_yacy_grid_crawler.crawler;
using yacy_yacy_grid_crawler.tools;

namespace yacy_yacy_grid_crawler.tests.original
{
    public class BlacklistTests : IDisposable
    {
        private Blacklist blacklist;
        private FileInfo testFile;

        public BlacklistTests()
        {
            blacklist = new Blacklist();
            var path = Path.Combine(Path.GetTempPath(), $"blacklist_{Guid.NewGuid()}.txt");
            testFile = new FileInfo(path);
        }

        public void Dispose()
        {
            if (testFile.Exists)
                testFile.Delete();
        }

        [Fact]
        public void TestLoadPlainPatterns()
        {
            File.WriteAllLines(testFile.FullName, new[]
            {
                ".*forbidden.com.* # info1",
                "# this is a comment",
                ".*blockme.net.*"
            });
            blacklist.load(testFile);

            var url1 = new MultiProtocolURL("http://forbidden.com/page");
            var url2 = new MultiProtocolURL("http://blockme.net/");
            var url3 = new MultiProtocolURL("http://allowed.com/");

            Assert.NotNull(blacklist.isBlacklisted(url1.toNormalform(true), url1));
            Assert.NotNull(blacklist.isBlacklisted(url2.toNormalform(true), url2));
            Assert.Null(blacklist.isBlacklisted(url3.toNormalform(true), url3));
        }

        [Fact]
        public void TestLoadHostPattern()
        {
            File.WriteAllText(testFile.FullName, "host example.com # host entry\n");
            blacklist.load(testFile);

            var url = new MultiProtocolURL("http://example.com/page");
            Assert.NotNull(blacklist.isBlacklisted(url.toNormalform(true), url));
            var other = new MultiProtocolURL("http://test.com/page");
            Assert.Null(blacklist.isBlacklisted(other.toNormalform(true), other));
        }

        [Fact]
        public void TestPatternSyntaxError()
        {
            File.WriteAllText(testFile.FullName, ".*this[is(bad\n");
            Exception ex = Record.Exception(() => blacklist.load(testFile));
            // Should not throw
            Assert.Null(ex);
        }

        [Fact]
        public void TestBlacklistInfoConstructorWithInvalidPattern()
        {
            Assert.Throws<ArgumentException>(() =>
                new Blacklist.BlacklistInfo("*This is [invalid", "src", "", null)
            );
        }

        [Fact]
        public void TestBlacklistCaches()
        {
            File.WriteAllText(testFile.FullName, ".*foo.com.*\n");
            blacklist.load(testFile);
            var url = new MultiProtocolURL("http://foo.com/bar");
            var str = url.toNormalform(true);
            Assert.NotNull(blacklist.isBlacklisted(str, url));
            // Cache
            Assert.NotNull(blacklist.isBlacklisted(str, url));
        }

        [Fact]
        public void TestBlacklistMissCache()
        {
            File.WriteAllText(testFile.FullName, ".*nothingtomatch.net.*\n");
            blacklist.load(testFile);
            var url = new MultiProtocolURL("http://notfoo.com/");
            var str = url.toNormalform(true);
            Assert.Null(blacklist.isBlacklisted(str, url));
            // Cache
            Assert.Null(blacklist.isBlacklisted(str, url));
        }

        [Fact]
        public void TestBlacklistInfoFields()
        {
            var bi = new Blacklist.BlacklistInfo(".*test.com.*", "src", "information", "host.com");
            Assert.NotNull(bi.matcher);
            Assert.Equal("src", bi.source);
            Assert.Equal("information", bi.info);
            Assert.Equal("host.com", bi.host);
        }
    }
}