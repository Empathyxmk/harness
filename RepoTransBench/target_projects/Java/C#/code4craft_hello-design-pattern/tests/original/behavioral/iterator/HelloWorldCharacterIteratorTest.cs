using Xunit;
using System;
using System.Collections.Generic;

namespace HelloDesignPattern.Tests.behavioral.iterator
{
    public class HelloWorldCharacterIteratorTest
    {
        [Fact]
        public void TestIterator()
        {
            char[] arr = new[] {'A', 'B', 'C'};
            IEnumerator<char> iter = new HelloWorldCharacterIterator(arr);
            Assert.True(iter.MoveNext());
            Assert.Equal('A', iter.Current);
            Assert.True(iter.MoveNext());
            Assert.Equal('B', iter.Current);
            Assert.True(iter.MoveNext());
            Assert.Equal('C', iter.Current);
            Assert.False(iter.MoveNext());
        }

        [Fact]
        public void TestNextThrows()
        {
            char[] arr = new char[0];
            IEnumerator<char> iter = new HelloWorldCharacterIterator(arr);
            Assert.False(iter.MoveNext());
            Assert.Throws<InvalidOperationException>(() => { var _ = iter.Current; });
        }
    }
}