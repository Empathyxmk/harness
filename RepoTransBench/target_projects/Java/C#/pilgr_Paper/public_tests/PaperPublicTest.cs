using System;
using System.Collections.Generic;
using System.Threading;
using Xunit;
using FluentAssertions;

namespace PilgrPaper.PublicTests
{
    public class PaperPublicTest : IDisposable
    {
        public PaperPublicTest()
        {
            Paper.Init();
            Paper.Book().Destroy();
        }

        [Fact]
        public void TestContainsPublic()
        {
            Paper.Book().Contains("cities").Should().BeFalse();
            Paper.Book().Write("cities", TestDataGenerator.GenPersonList(5));
            Paper.Book().Contains("cities").Should().BeTrue();
        }

        [Fact]
        public void TestDeletePublic()
        {
            Paper.Book().Write("countries", TestDataGenerator.GenPersonList(2));
            Paper.Book().Contains("countries").Should().BeTrue();
            Paper.Book().Delete("countries");
            Paper.Book().Contains("countries").Should().BeFalse();
        }

        [Fact]
        public void TestDeleteNotExistedPublic()
        {
            Paper.Book().Contains("cities").Should().BeFalse();
            Paper.Book().Delete("cities");
        }

        [Fact]
        public void TestClearPublic()
        {
            Paper.Book().Write("kings", TestDataGenerator.GenPersonList(2));
            Paper.Book().Write("queens", TestDataGenerator.GenPersonList(4));
            Paper.Book().Contains("kings").Should().BeTrue();
            Paper.Book().Contains("queens").Should().BeTrue();

            Paper.Book().Destroy();
            Paper.Book().Contains("kings").Should().BeFalse();
            Paper.Book().Contains("queens").Should().BeFalse();

            Paper.Book().Write("lords", TestDataGenerator.GenPersonList(6));
            Paper.Book().Contains("lords").Should().BeTrue();
            Paper.Book().Read<List<Person>>("lords").Should().HaveCount(6);
        }

        [Fact]
        public void TestWriteReadNormalPublic()
        {
            Paper.Book().Write("fruit", "Apple");
            var val = Paper.Book().Read<string>("fruit", "Banana");
            val.Should().Be("Apple");
        }

        [Fact]
        public void TestWriteReadNormalAfterReinitPublic()
        {
            Paper.Book().Write("drink", "Water");
            var val = Paper.Book().Read<string>("drink", "Tea");
            Paper.Init();
            val.Should().Be("Water");
        }

        [Fact]
        public void TestReadNotExistedPublic()
        {
            var val = Paper.Book().Read<string>("unknown-key");
            val.Should().BeNull();
        }

        [Fact]
        public void TestReadDefaultPublic()
        {
            var val = Paper.Book().Read<string>("missing-key", "fallback");
            val.Should().Be("fallback");
        }

        [Fact]
        public void TestWriteNullPublic()
        {
            Action act = () => Paper.Book().Write("empty_val", null);
            act.Should().Throw<PaperDbException>();
        }

        [Fact]
        public void TestReplacePublic()
        {
            Paper.Book().Write("flower", "Rose");
            Paper.Book().Read<string>("flower").Should().Be("Rose");
            Paper.Book().Write("flower", "Tulip");
            Paper.Book().Read<string>("flower").Should().Be("Tulip");
        }

        [Fact]
        public void TestValidKeyNamesPublic()
        {
            Paper.Book().Write("animal", "Lion");
            Paper.Book().Read<string>("animal").Should().Be("Lion");

            Paper.Book().Write("animal.info$@", "Lion");
            Paper.Book().Read<string>("animal.info$@").Should().Be("Lion");

            Paper.Book().Write("creature-123", "Tiger");
            Paper.Book().Read<string>("creature-123").Should().Be("Tiger");
        }

        [Fact]
        public void TestInvalidKeyNameBackslashPublic()
        {
            Action act = () =>
            {
                Paper.Book().Write("key/with/slash", "Value");
                Paper.Book().Read<string>("key/with/slash");
            };
            act.Should().Throw<PaperDbException>();
        }

        [Fact]
        public void TestGetBookWithDefaultBookNamePublic()
        {
            Action act = () => Paper.Book(Paper.DefaultDbName);
            act.Should().Throw<PaperDbException>();
        }

        [Fact]
        public void TestCustomBookReadWritePublic()
        {
            var alt = "alternate";
            Paper.Book().Should().NotBeSameAs(Paper.Book(alt));
            Paper.Book(alt).Destroy();

            Paper.Book().Write("river", "Amazon");
            Paper.Book(alt).Write("river", "Nile");

            Paper.Book().Read<string>("river").Should().Be("Amazon");
            Paper.Book(alt).Read<string>("river").Should().Be("Nile");
        }

        [Fact]
        public void TestCustomBookDestroyPublic()
        {
            var alt = "alternate";
            Paper.Book(alt).Destroy();

            Paper.Book().Write("river", "Ganges");
            Paper.Book(alt).Write("river", "Thames");

            Paper.Book(alt).Destroy();

            Paper.Book().Read<string>("river").Should().Be("Ganges");
            Paper.Book(alt).Read<string>("river").Should().BeNull();
        }

        [Fact]
        public void TestGetAllKeysPublic()
        {
            Paper.Book().Destroy();

            Paper.Book().Write("ocean", "Pacific");
            Paper.Book().Write("ocean2", "Atlantic");
            Paper.Book().Write("ocean3", "Indian");
            var allKeys = Paper.Book().GetAllKeys();

            allKeys.Should().HaveCount(3);
            allKeys.Should().Contain("ocean");
            allKeys.Should().Contain("ocean2");
            allKeys.Should().Contain("ocean3");
        }

        [Fact]
        public void TestCustomSerializerPublic()
        {
            Paper.AddSerializer(typeof(DateTime), new DummyJodaDateTimeSerializer());
            var now = DateTime.UtcNow.AddDays(1);
            Paper.Book().Write("dt1", now);
            Paper.Book().Read<DateTime>("dt1").Should().Be(now);
        }

        [Fact]
        public void TestTimestampNoObjectPublic()
        {
            Paper.Book().Destroy();
            var timestamp = Paper.Book().LastModified("nothing_here");
            timestamp.Should().Be(-1L);
        }

        [Fact]
        public void TestTimestampPublic()
        {
            var testStartMs = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
            Paper.Book().Destroy();
            Paper.Book().Write("continent", "Asia");

            var fileWriteMs = Paper.Book().LastModified("continent");
            fileWriteMs.Should().NotBe(-1);

            var elapsed = fileWriteMs - testStartMs;
            (elapsed >= 0).Should().BeTrue();
            Paper.Book().Read<string>("continent").Should().NotBeNull();
        }

        public void Dispose()
        {
        }

        class DummyJodaDateTimeSerializer { }
    }
}