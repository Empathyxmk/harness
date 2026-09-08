using System;
using System.Collections.Generic;
using System.Linq;
using Xunit;
using FluentAssertions;
using PilgrPaper.Models;
using PilgrPaper.TestUtils;

namespace PilgrPaper.OriginalTests
{
    /// <summary>
    /// Tests List write/read API
    /// </summary>
    public class DataTest : IDisposable
    {
        public DataTest()
        {
            Paper.Init();
            Paper.Book().Destroy();
        }

        [Fact]
        public void TestPutEmptyList()
        {
            var inserted = TestDataGenerator.GenPersonList(0);
            Paper.Book().Write("persons", inserted);
            Paper.Book().Read<List<Person>>("persons").Should().BeEmpty();
        }

        [Fact]
        public void TestPutGetList()
        {
            var inserted = TestDataGenerator.GenPersonList(10000);
            Paper.Book().Write("persons", inserted);
            var persons = Paper.Book().Read<List<Person>>("persons");
            persons.Should().BeEquivalentTo(inserted);
        }

        [Fact]
        public void TestPutMap()
        {
            var inserted = TestDataGenerator.GenPersonMap(10000);
            Paper.Book().Write("persons", inserted);
            var personMap = Paper.Book().Read<Dictionary<int, Person>>("persons");
            personMap.Should().BeEquivalentTo(inserted);
        }

        [Fact]
        public void TestPutPOJO()
        {
            var person = TestDataGenerator.GenPerson(new Person(), 1);
            Paper.Book().Write("profile", person);
            var savedPerson = Paper.Book().Read<Person>("profile");
            savedPerson.Should().BeEquivalentTo(person);
            savedPerson.Should().NotBeSameAs(person);
        }

        [Fact]
        public void TestPutSubAbstractListRandomAccess()
        {
            var origin = TestDataGenerator.GenPersonList(100);
            var sublist = origin.Skip(10).Take(20).ToList();
            TestReadWriteWithoutClassCheck(sublist);
        }

        [Fact]
        public void TestPutSubAbstractList()
        {
            var origin = new LinkedList<Person>(TestDataGenerator.GenPersonList(100));
            var sublist = origin.Skip(10).Take(20).ToList();
            TestReadWriteWithoutClassCheck(sublist);
        }

        [Fact]
        public void TestPutLinkedList()
        {
            var origin = new LinkedList<Person>(TestDataGenerator.GenPersonList(100));
            TestReadWrite(origin.ToList());
        }

        [Fact]
        public void TestPutArraysAsLists()
        {
            TestReadWrite(new List<string> { "123", "345" });
        }

        [Fact]
        public void TestPutCollectionsEmptyList()
        {
            TestReadWrite(new List<string>());
        }

        [Fact]
        public void TestPutCollectionsEmptyMap()
        {
            TestReadWrite(new Dictionary<string, string>());
        }

        [Fact]
        public void TestPutCollectionsEmptySet()
        {
            TestReadWrite(new HashSet<string>());
        }

        [Fact]
        public void TestPutSingletonList()
        {
            TestReadWrite(new List<string> { "item" });
        }

        [Fact]
        public void TestPutSingletonSet()
        {
            TestReadWrite(new HashSet<string> { "item" });
        }

        [Fact]
        public void TestPutSingletonMap()
        {
            var dict = new Dictionary<string, string> { { "key", "value" } };
            TestReadWrite(dict);
        }

        [Fact]
        public void TestPutGeorgianCalendar()
        {
            var calendar = new GregorianCalendar();
            TestReadWrite(calendar);
        }

        [Fact]
        public void TestPutSynchronizedList()
        {
            var list = new List<string>();
            lock (list)
            {
                TestReadWrite(list);
            }
        }

        [Fact]
        public void TestReadWriteClassWithoutNoArgConstructor()
        {
            TestReadWrite(new PersonArg("name"));
        }

        private object TestReadWriteWithoutClassCheck(object originObj)
        {
            Paper.Book().Write("obj", originObj);
            var readObj = Paper.Book().Read<object>("obj");
            readObj.Should().BeEquivalentTo(originObj);
            return readObj;
        }

        private void TestReadWrite(object originObj)
        {
            var readObj = TestReadWriteWithoutClassCheck(originObj);
            readObj.GetType().Should().Be(originObj.GetType());
        }

        public void Dispose()
        {
            // Cleanup if needed
        }
    }
}