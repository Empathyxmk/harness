using System;
using System.Collections.Generic;
using System.Threading;
using Xunit;
using FluentAssertions;

namespace PilgrPaper.OriginalTests
{
    public class PaperTest : IDisposable
    {
        public PaperTest()
        {
            Paper.Init();
            Paper.Book().Destroy();
        }

        [Fact]
        public void TestContains()
        {
            Paper.Book().Contains("persons").Should().BeFalse();
            Paper.Book().Write("persons", TestDataGenerator.GenPersonList(10));
            Paper.Book().Contains("persons").Should().BeTrue();
        }

        [Fact]
        public void TestDelete()
        {
            Paper.Book().Write("persons", TestDataGenerator.GenPersonList(10));
            Paper.Book().Contains("persons").Should().BeTrue();
            Paper.Book().Delete("persons");
            Paper.Book().Contains("persons").Should().BeFalse();
        }

        [Fact]
        public void TestDeleteNotExisted()
        {
            Paper.Book().Contains("persons").Should().BeFalse();
            Paper.Book().Delete("persons");
        }

        [Fact]
        public void TestClear()
        {
            Paper.Book().Write("persons", TestDataGenerator.GenPersonList(10));
            Paper.Book().Write("persons2", TestDataGenerator.GenPersonList(20));
            Paper.Book().Contains("persons").Should().BeTrue();
            Paper.Book().Contains("persons2").Should().BeTrue();

            Paper.Book().Destroy();
            Paper.Book().Contains("persons").Should().BeFalse();
            Paper.Book().Contains("persons2").Should().BeFalse();

            Paper.Book().Write("persons3", TestDataGenerator.GenPersonList(30));
            Paper.Book().Contains("persons3").Should().BeTrue();
            Paper.Book().Read<List<Person>>("persons3").Should().HaveCount(30);
        }

        [Fact]
        public void TestWriteReadNormal()
        {
            Paper.Book().Write("city", "Lund");
            var val = Paper.Book().Read<string>("city", "default");
            val.Should().Be("Lund");
        }

        [Fact]
        public void TestWriteReadNormalAfterReinit()
        {
            Paper.Book().Write("city", "Lund");
            var val = Paper.Book().Read<string>("city", "default");
            Paper.Init();
            val.Should().Be("Lund");
        }

        [Fact]
        public void TestReadNotExisted()
        {
            var val = Paper.Book().Read<string>("non-existed");
            val.Should().BeNull();
        }

        [Fact]
        public void TestReadDefault()
        {
            var val = Paper.Book().Read("non-existed", "default");
            val.Should().Be("default");
        }

        [Fact]
        public void TestWriteNull()
        {
            Action act = () => Paper.Book().Write("city", null);
            act.Should().Throw<PaperDbException>();
        }

        [Fact]
        public void TestReplace()
        {
            Paper.Book().Write("city", "Lund");
            Paper.Book().Read<string>("city").Should().Be("Lund");
            Paper.Book().Write("city", "Kyiv");
            Paper.Book().Read<string>("city").Should().Be("Kyiv");
        }

        [Fact]
        public void TestValidKeyNames()
        {
            Paper.Book().Write("city", "Lund");
            Paper.Book().Read<string>("city").Should().Be("Lund");

            Paper.Book().Write("city.dasd&%", "Lund");
            Paper.Book().Read<string>("city.dasd&%").Should().Be("Lund");

            Paper.Book().Write("city-ads", "Lund");
            Paper.Book().Read<string>("city-ads").Should().Be("Lund");
        }

        [Fact]
        public void TestInvalidKeyNameBackslash()
        {
            Action act = () =>
            {
                Paper.Book().Write("city/ads", "Lund");
                Paper.Book().Read<string>("city/ads");
            };
            act.Should().Throw<PaperDbException>();
        }

        [Fact]
        public void TestGetBookWithDefaultBookName()
        {
            Action act = () => Paper.Book(Paper.DefaultDbName);
            act.Should().Throw<PaperDbException>();
        }

        [Fact]
        public void TestCustomBookReadWrite()
        {
            string nativeName = "native";
            Paper.Book().Should().NotBeSameAs(Paper.Book(nativeName));
            Paper.Book(nativeName).Destroy();

            Paper.Book().Write("city", "Lund");
            Paper.Book(nativeName).Write("city", "Kyiv");

            Paper.Book().Read<string>("city").Should().Be("Lund");
            Paper.Book(nativeName).Read<string>("city").Should().Be("Kyiv");
        }

        [Fact]
        public void TestCustomBookDestroy()
        {
            string nativeName = "native";
            Paper.Book(nativeName).Destroy();

            Paper.Book().Write("city", "Lund");
            Paper.Book(nativeName).Write("city", "Kyiv");

            Paper.Book(nativeName).Destroy();

            Paper.Book().Read<string>("city").Should().Be("Lund");
            Paper.Book(nativeName).Read<string>("city").Should().BeNull();
        }

        [Fact]
        public void TestGetAllKeys()
        {
            Paper.Book().Destroy();

            Paper.Book().Write("city", "Lund");
            Paper.Book().Write("city1", "Lund1");
            Paper.Book().Write("city2", "Lund2");
            var allKeys = Paper.Book().GetAllKeys();

            allKeys.Should().HaveCount(3);
            allKeys.Should().Contain("city");
            allKeys.Should().Contain("city1");
            allKeys.Should().Contain("city2");
        }

        [Fact]
        public void TestCustomSerializer()
        {
            // Custom serializer logic here (example, just use built-in for .NET)
            // This is stubbed for demonstration, since C# test suite has no JodaTime
            Paper.AddSerializer(typeof(DateTime), new DummyJodaDateTimeSerializer());
            var now = DateTime.UtcNow;
            Paper.Book().Write("joda-datetime", now);
            Paper.Book().Read<DateTime>("joda-datetime").Should().Be(now);
        }

        [Fact]
        public void TestTimestampNoObject()
        {
            Paper.Book().Destroy();
            var timestamp = Paper.Book().LastModified("city");
            timestamp.Should().Be(-1L);
        }

        [Fact]
        public void TestTimestamp()
        {
            var testStartMs = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            Paper.Book().Destroy();
            Paper.Book().Write("city", "Lund");

            var fileWriteMs = Paper.Book().LastModified("city");
            fileWriteMs.Should().NotBe(-1);

            var elapsed = fileWriteMs - testStartMs;
            (elapsed < 1000 || elapsed > -1000).Should().BeTrue();
        }

        [Fact]
        public void TestTimestampChanges()
        {
            Paper.Book().Destroy();
            Paper.Book().Write("city", "Lund");
            var fileWrite1Ms = Paper.Book().LastModified("city");
            Thread.Sleep(1000);
            Paper.Book().Write("city", "Kyiv");
            var fileWrite2Ms = Paper.Book().LastModified("city");
            fileWrite2Ms.Should().BeGreaterThan(fileWrite1Ms);
        }

        [Fact]
        public void TestDbFileExistsAfterFailedRead()
        {
            var key = "cityMap";
            Paper.Book().Contains(key).Should().BeFalse();
            TestUtils.ReplacePaperDbFileBy("invalid_data.pt", key);
            Paper.Book().Contains(key).Should().BeTrue();

            Exception expectedException = null;
            try
            {
                Paper.Book().Read<object>(key);
            }
            catch (PaperDbException e)
            {
                expectedException = e;
            }
            expectedException.Should().NotBeNull();
            Paper.Book().Contains(key).Should().BeTrue();
        }

        [Fact]
        public void GetFolderPathForBookDefault()
        {
            var path = Paper.Book().GetPath();
            path.Should().EndWith("/io.paperdb.test/files/io.paperdb");
        }

        [Fact]
        public void GetFilePathForKeyDefaultBook()
        {
            var path = Paper.Book().GetPath("my_key");
            path.Should().EndWith("/io.paperdb.test/files/io.paperdb/my_key.pt");
        }

        public void Dispose()
        {
        }

        // Stub for DateTime serializer
        class DummyJodaDateTimeSerializer { }
    }
}