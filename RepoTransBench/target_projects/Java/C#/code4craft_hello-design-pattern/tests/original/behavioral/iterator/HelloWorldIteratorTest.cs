using Xunit;
using System;

namespace HelloDesignPattern.Tests.behavioral.iterator
{
    public class HelloWorldIteratorTest
    {
        [Fact]
        public void TestHelloWorldIterator()
        {
            var helloIterator = "Hello Iterator!";
            var helloWorldCharacterIterator = new HelloWorldCharacterIterator(helloIterator.ToCharArray());
            var result = "";
            while (helloWorldCharacterIterator.MoveNext())
            {
                result += helloWorldCharacterIterator.Current;
            }
            Assert.Equal(helloIterator, result);
        }

        [Fact]
        public void TestHelloWorldIteratorRemove()
        {
            var helloIterator = "Hello Iterator!";
            var helloWorldCharacterIterator = new HelloWorldCharacterIterator(helloIterator.ToCharArray());
            Assert.Throws<NotSupportedException>(() => helloWorldCharacterIterator.Remove());
        }
    }
}