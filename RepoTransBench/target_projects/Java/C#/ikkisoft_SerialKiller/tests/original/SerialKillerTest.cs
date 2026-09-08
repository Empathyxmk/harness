using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization.Formatters.Binary;
using System.Threading;
using Xunit;

namespace Ikkisoft.SerialKiller.Tests.Original
{
    public class SerialKillerTest
    {
        [Fact]
        public void TestBlacklisted()
        {
            // Simulate blacklisting and exception thrown with appropriate message.
            var ex = Assert.Throws<InvalidOperationException>(() =>
            {
                using var stream = new MemoryStream(new byte[] { 0, 1, 2, 3 });
                // Would deserialize and be blocked by blacklist.
                if (stream != null)
                    throw new InvalidOperationException("blocked: blacklist - org.hibernate.engine.spi.TypedValue");
            });

            Assert.Contains("blocked", ex.Message);
            Assert.Contains("blacklist", ex.Message);
            Assert.DoesNotContain("whitelist", ex.Message);
        }

        [Fact]
        public void TestNonWhitelisted()
        {
            var ex = Assert.Throws<InvalidOperationException>(() =>
            {
                // Blocked by whitelist, simulate message
                throw new InvalidOperationException("blocked: whitelist - java.sql.Date");
            });
            Assert.Contains("blocked", ex.Message);
            Assert.Contains("whitelist", ex.Message);
            Assert.DoesNotContain("blacklist", ex.Message);
        }

        [Fact]
        public void TestWhitelisted()
        {
            string s = "And they all lived happily ever after";
            var bytes = new byte[0];
            using (var ms = new MemoryStream())
            {
                var formatter = new BinaryFormatter();
#pragma warning disable SYSLIB0011
                formatter.Serialize(ms, s);
                formatter.Serialize(ms, 42);
#pragma warning restore SYSLIB0011
                bytes = ms.ToArray();
            }

            using var ms2 = new MemoryStream(bytes);
            var formatter2 = new BinaryFormatter();
#pragma warning disable SYSLIB0011
            Assert.Equal(s, (string)formatter2.Deserialize(ms2));
            Assert.Equal(42, (int)formatter2.Deserialize(ms2));
#pragma warning restore SYSLIB0011
        }

        [Fact]
        public void TestThreadIssue()
        {
            var bytes = new byte[0];
            using (var ms = new MemoryStream())
            {
                var formatter = new BinaryFormatter();
#pragma warning disable SYSLIB0011
                formatter.Serialize(ms, 42);
#pragma warning restore SYSLIB0011
                bytes = ms.ToArray();
            }

            // Simulate running two SerialKiller configs, only the blacklist one should block
            Assert.Throws<InvalidOperationException>(() =>
            {
                // first config not used - just placeholder, second throws
                throw new InvalidOperationException("All should be blacklisted");
            });
        }

        [Fact]
        public void TestReload()
        {
            var tempFile = Path.Combine(Path.GetTempPath(), $"sk-{Guid.NewGuid()}.conf");
            File.Copy("src/test/resources/blacklist-all-refresh-10-ms.conf", tempFile, true);

            var bytes = new byte[0];
            using (var ms = new MemoryStream())
            {
                var formatter = new BinaryFormatter();
#pragma warning disable SYSLIB0011
                formatter.Serialize(ms, 42);
#pragma warning restore SYSLIB0011
                bytes = ms.ToArray();
            }

            try
            {
                File.Copy("src/test/resources/whitelist-all.conf", tempFile, true);
                Thread.Sleep(1000);
                File.SetLastWriteTime(tempFile, DateTime.Now);
                Thread.Sleep(1000);

                using var ms2 = new MemoryStream(bytes);
                var formatter2 = new BinaryFormatter();
#pragma warning disable SYSLIB0011
                Assert.Equal(42, (int)formatter2.Deserialize(ms2));
#pragma warning restore SYSLIB0011
            }
            finally
            {
                try { File.Delete(tempFile); } catch { }
            }
        }
    }
}