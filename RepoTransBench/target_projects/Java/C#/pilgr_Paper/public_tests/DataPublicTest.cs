using System;
using System.Collections.Generic;
using System.Linq;
using Xunit;
using FluentAssertions;
using PilgrPaper.Models;
using PilgrPaper.TestUtils;

namespace PilgrPaper.PublicTests
{
    /// <summary>
    /// Public test cases for List write/read API with different data
    /// </summary>
    public class DataPublicTest : IDisposable
    {
        public DataPublicTest()
        {
            Paper.Init();
            Paper.Book().Destroy();
        }

        [Fact]
        public void TestPutEmptyListPublic()
        {
            var inserted = TestDataGenerator.GenPersonList(3);
            Paper.Book().Write("persons_pub", inserted);
            Paper.Book().Read<List<Person>>("persons_pub").Should().HaveCount(3);

            Paper.Book().Write("persons_pub", new List<Person>());
            Paper.Book().Read<List<Person>>("persons_pub").Should().BeEmpty();
        }

        [Fact]
        public void TestPutGetListPublic()
        {
            var inserted = TestDataGenerator.GenPersonList(7);
            Paper.Book().Write("alt_persons", inserted);
            var persons = Paper.Book().Read<List<Person>>("alt_persons");
            persons.Should().BeEquivalentTo(inserted);
        }

        [Fact]
        public void TestPutMapPublic()
        {
            var inserted = TestDataGenerator.GenPersonMap(5);
            Paper.Book().Write("alt_persons_map", inserted);

            var personMap = Paper.Book().Read<Dictionary<int, Person>>("alt_persons_map");
            personMap.Should().BeEquivalentTo(inserted);
        }

        [Fact]
        public void TestPutPOJOPublic()
        {
            var person = TestDataGenerator.GenPerson(new Person(), 42);
            Paper.Book().Write("new_profile", person);

            var savedPerson = Paper.Book().Read<Person>("new_profile");
            savedPerson.Should().BeEquivalentTo(person);
            savedPerson.Should().NotBeSameAs(person);
        }

        [Fact]
        public void TestPutSubAbstractListRandomAccessPublic()
        {
            var origin = TestDataGenerator.GenPersonList(20);
            var sublist = origin.Skip(5).Take(12).ToList();
            TestReadWriteWithoutClassCheck(sublist);
        }

        [Fact]
        public void TestPutSubAbstractListPublic()
        {
            var origin = new LinkedList<Person>(TestDataGenerator.GenPersonList(20));
            var sublist = origin.Skip(5).Take(12).ToList();
            TestReadWriteWithoutClassCheck(sublist);
        }

        [Fact]
        public void TestPutLinkedListPublic()
        {
            var origin = new LinkedList<Person>(TestDataGenerator.GenPersonList(15));
            TestReadWrite(origin.ToList());
        }

        [Fact]
        public void TestPutArraysAsListsPublic()
        {
            TestReadWrite(new List<string> { "abc", "xyz", "def" });
        }

        [Fact]
        public void TestPutCollectionsEmptyListPublic()
        {
            TestReadWrite(new List<string>());
        }

        [Fact]
        public void TestPutCollectionsEmptyMapPublic()
        {
            TestReadWrite(new Dictionary<int, string>());
        }

        [Fact]
        public void TestPutCollectionsEmptySetPublic()
        {
            TestReadWrite(new HashSet<string>());
        }

        [Fact]
        public void TestPutSingletonListPublic()
        {
            TestReadWrite(new List<string> { "singleton_item" });
        }

        [Fact]
        public void TestPutSingletonSetPublic()
        {
            TestReadWrite(new HashSet<string> { "singleton" });
        }

        [Fact]
        public void TestPutSingletonMapPublic()
        {
            TestReadWrite(new Dictionary<string, string> { { "onlykey", "onlyvalue" } });
        }

        [Fact]
        public void TestPutGeorgianCalendarPublic()
        {
            var cal = new GregorianCalendar(1999, 8, 13);
            TestReadWrite(cal);
        }

        [Fact]
        public void TestPutSynchronizedListPublic()
        {
            var arr = new List<string> { "hello" };
            lock (arr)
            {
                TestReadWrite(arr);
            }
        }

        [Fact]
        public void TestReadWriteClassWithoutNoArgConstructorPublic()
        {
            TestReadWrite(new PersonArg("alice"));
        }

        private object TestReadWriteWithoutClassCheck(object originObj)
        {
            Paper.Book().Write("obj_pub", originObj);
            var readObj = Paper.Book().Read<object>("obj_pub");
            readObj.Should().BeEquivalentTo(originObj);
            return readObj;
        }

        private void TestReadWrite(object originObj)
        {
            var readObj = TestReadWriteWithoutClassCheck(originObj);
            readObj.GetType().Should().Be(originObj.GetType());
        }

        public void Dispose() { }
    }
}