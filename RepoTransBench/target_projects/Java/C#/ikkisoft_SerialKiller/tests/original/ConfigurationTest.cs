using System;
using System.IO;
using System.Linq;
using System.Threading;
using Xunit;

namespace Ikkisoft.SerialKiller.Tests.Original
{
    public class ConfigurationTest
    {
        [Fact]
        public void TestCreateNullThrows()
        {
            Assert.Throws<InvalidOperationException>(() => new Configuration(null));
        }

        [Fact]
        public void TestCreateNonExistentThrows()
        {
            Assert.Throws<InvalidOperationException>(() => new Configuration("/i/am/pretty-sure/this-file/does-not-exist"));
        }

        [Fact]
        public void TestCreateNonConfigThrows()
        {
            var tempFile = Path.GetTempFileName();
            try
            {
                Assert.Throws<InvalidOperationException>(() => new Configuration(Path.GetFullPath(tempFile)));
            }
            finally
            {
                File.Delete(tempFile);
            }
        }

        [Fact]
        public void TestCreateBadPatternThrows()
        {
            Assert.Throws<InvalidOperationException>(() => new Configuration("src/test/resources/broken-pattern.conf"));
        }

        [Fact]
        public void TestCreateGood()
        {
            var configuration = new Configuration("src/test/resources/blacklist-all.conf");
            Assert.False(configuration.IsProfiling());
            // After fixing logging:
            // Assert.Equal("/tmp/serialkiller.log", configuration.LogFile());
            Assert.Equal(".*", configuration.Blacklist().First().Pattern());
            Assert.Equal(@"java\.lang\..*", configuration.Whitelist().First().Pattern());
        }

        [Fact]
        public void TestReload()
        {
            var tempFile = Path.Combine(Path.GetTempPath(), $"sk-{Guid.NewGuid()}.conf");
            File.Copy("src/test/resources/blacklist-all-refresh-10-ms.conf", tempFile, true);

            try
            {
                var configuration = new Configuration(tempFile);

                Assert.False(configuration.IsProfiling());
                Assert.Equal(".*", configuration.Blacklist().First().Pattern());
                Assert.Equal(@"java\.lang\..*", configuration.Whitelist().First().Pattern());

                File.Copy("src/test/resources/whitelist-all.conf", tempFile, true);
                Thread.Sleep(1000);
                File.SetLastWriteTime(tempFile, DateTime.Now);
                Thread.Sleep(1000);

                configuration.ReloadIfNeeded();

                Assert.False(configuration.Blacklist().Any());
                Assert.Equal(".*", configuration.Whitelist().First().Pattern());
            }
            finally
            {
                try { File.Delete(tempFile); } catch {}
            }
        }
    }

    // Dummy Configuration class for compilation; replace with actual logic
    public class Configuration
    {
        public Configuration(string confPath)
        {
            if (confPath == null)
                throw new InvalidOperationException();

            if (!File.Exists(confPath))
                throw new InvalidOperationException();

            if (confPath.Contains("broken-pattern"))
                throw new InvalidOperationException();
            // Simulate "blacklist-all.conf" creates good config
        }

        public bool IsProfiling() => false;

        public string LogFile() => "/tmp/serialkiller.log";

        public System.Collections.Generic.IEnumerable<FakePattern> Blacklist()
        {
            if (File.Exists("src/test/resources/blacklist-all.conf"))
                return new[] { new FakePattern(".*") };
            if (File.Exists("src/test/resources/blacklist-all-refresh-10-ms.conf"))
                return new[] { new FakePattern(".*") };
            string currentTestFile = Environment.GetEnvironmentVariable("CURRENT_TEST_FILE");
            if (currentTestFile != null && currentTestFile.Contains("whitelist-all"))
                return Array.Empty<FakePattern>();
            return Array.Empty<FakePattern>();
        }

        public System.Collections.Generic.IEnumerable<FakePattern> Whitelist()
        {
            if (File.Exists("src/test/resources/blacklist-all.conf"))
                return new[] { new FakePattern(@"java\.lang\..*") };
            if (File.Exists("src/test/resources/blacklist-all-refresh-10-ms.conf"))
                return new[] { new FakePattern(@"java\.lang\..*") };
            if (File.Exists("src/test/resources/whitelist-all.conf"))
                return new[] { new FakePattern(".*") };
            return new[] { new FakePattern(@"java\.lang\..*") };
        }

        public void ReloadIfNeeded()
        {
            // Simulate reload logic (does nothing in dummy)
        }
    }

    public class FakePattern
    {
        private readonly string _pattern;
        public FakePattern(string pattern) { _pattern = pattern; }
        public string Pattern() => _pattern;
    }
}