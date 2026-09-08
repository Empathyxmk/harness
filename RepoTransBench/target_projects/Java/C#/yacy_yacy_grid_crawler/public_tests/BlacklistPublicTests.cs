using System;
using System.IO;
using System.Text.RegularExpressions;
using Xunit;
using yacy_yacy_grid_crawler.crawler;
using yacy_yacy_grid_crawler.tools;

namespace yacy_yacy_grid_crawler.public_tests
{
    public class BlacklistPublicTests : IDisposable
    {
        private Blacklist blacklist;
        private FileInfo testFile;

        public BlacklistPublicTests()
        {
            blacklist = new Blacklist();
            var path = Path.Combine(Path.GetTempPath(), $"blacklistpub_{Guid.NewGuid()}.txt");
            testFile = new FileInfo(path);
        }

        public void Dispose()
        {
            if (testFile.Exists)
                testFile.Delete();
        }

        [Fact]
        public void TestLoadPlainPatterns_Public()
        {
            File.WriteAllLines(testFile.FullName, new[]
            {
                ".*denythis.org.* # info2",
                "# another comment",
                ".*lockme.io.*"
            });
            blacklist.load(testFile);

            var url1 = new MultiProtocolURL("http://denythis.org/document");
            var url2 = new MultiProtocolURL("http://lockme.io/data");
            var url3 = new MultiProtocolURL("http://good.com/");

            Assert.NotNull(blacklist.isBlacklisted(url1.toNormalform(true), url1));
            Assert.NotNull(blacklist.isBlacklisted(url2.toNormalform(true), url2));
            Assert.Null(blacklist.isBlacklisted(url3.toNormalform(true), url3));
        }

        [Fact]
        public void TestLoadHostPattern_Public()
        {
            File.WriteAllText(testFile.FullName, "host othersite.org # public host entry\n");
            blacklist.load(testFile);

            var url = new MultiProtocolURL("http://othersite.org/info");
            Assert.NotNull(blacklist.isBlacklisted(url.toNormalform(true), url));
            var other = new MultiProtocolURL("http://diffsite.org/home");
            Assert.Null(blacklist.isBlacklisted(other.toNormalform(true), other));
        }

        [Fact]
        public void TestPatternSyntaxError_Public()
        {
            File.WriteAllText(testFile.FullName, ".*wrong(syntax\n");
            Exception ex = Record.Exception(() => blacklist.load(testFile));
            // Should not throw
            Assert.Null(ex);
        }

        [Fact]
        public void TestBlacklistInfoConstructorWithInvalidPattern_Public()
        {
            Assert.Throws<ArgumentException>(() =>
                new Blacklist.BlacklistInfo("*Wrong [pattern", "src2", "", null)
            );
        }

        [Fact]
        public void TestBlacklistCaches_Public()
        {
            File.WriteAllText(testFile.FullName, ".*bar.org.*\n");
            blacklist.load(testFile);
            var url = new MultiProtocolURL("http://bar.org/example");
            var str = url.toNormalform(true);
            Assert.NotNull(blacklist.isBlacklisted(str, url));
            // Cache
            Assert.NotNull(blacklist.isBlacklisted(str, url));
        }

        [Fact]
        public void TestBlacklistMissCache_Public()
        {
            File.WriteAllText(testFile.FullName, ".*abcxyz42.com.*\n");
            blacklist.load(testFile);
            var url = new MultiProtocolURL("http://notbar.org/home");
            var str = url.toNormalform(true);
            Assert.Null(blacklist.isBlacklisted(str, url));
            // Cache
            Assert.Null(blacklist.isBlacklisted(str, url));
        }

        [Fact]
        public void TestBlacklistInfoFields_Public()
        {
            var bi = new Blacklist.BlacklistInfo(".*another-test.org.*", "srcFile", "extra-info", "host.org");
            Assert.NotNull(bi.matcher);
            Assert.Equal("srcFile", bi.source);
            Assert.Equal("extra-info", bi.info);
            Assert.Equal("host.org", bi.host);
        }
    }
}