using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using Xunit;
using GeneratorLib;

namespace PublicTests
{
    public class GeneratorPublicTest
    {
        [Fact]
        public void TestEmptyGenerator()
        {
            Assert.Equal(new List<object>(), List(new EmptyGenerator()));
        }

        private class EmptyGenerator : Generator
        {
            protected override void run()
            {
            }
        }

        public static List<T> List<T>(IEnumerable<T> enumerable)
        {
            return enumerable.ToList();
        }

        [Fact]
        public void TestOneEltGenerator()
        {
            List<string> oneEltList = new List<string> { "hello" };
            Assert.Equal(oneEltList, List(new ListGenerator<string>(oneEltList)));
        }

        private class ListGenerator<T> : Generator<T>
        {
            private readonly List<T> elements;
            public ListGenerator(List<T> elements)
            {
                this.elements = elements;
            }
            protected override void run()
            {
                foreach (var element in elements)
                {
                    yield(element);
                }
            }
        }

        [Fact]
        public void TestTwoEltGenerator()
        {
            List<double> twoEltList = new List<double> { 3.14, 2.71 };
            Assert.Equal(twoEltList, List(new ListGenerator<double>(twoEltList)));
        }

        [Fact]
        public void TestInfiniteGenerator()
        {
            InfiniteGenerator generator = new InfiniteGenerator();
            TestInfiniteGenerator(generator);
        }

        private void TestInfiniteGenerator(InfiniteGenerator generator)
        {
            int NUM_ELTS_TO_INSPECT = 777;
            var generatorEnumerator = generator.GetEnumerator();
            for (int i = 0; i < NUM_ELTS_TO_INSPECT; i++)
            {
                Assert.True(generatorEnumerator.MoveNext());
                Assert.Equal("repeat", generatorEnumerator.Current);
            }
        }

        private class InfiniteGenerator : Generator<string>
        {
            protected override void run()
            {
                while (true)
                    yield("repeat");
            }
        }

        [Fact]
        public void TestInfiniteGeneratorLeavesNoRunningThreads()
        {
            InfiniteGenerator generator = new InfiniteGenerator();
            TestInfiniteGenerator(generator);
            generator.Dispose();

            Assert.False(generator.producer.IsAlive, "Background thread should have terminated.");
        }

        private class CustomRuntimeException : Exception { }

        private class GeneratorRaisingException : Generator<string>
        {
            protected override void run()
            {
                throw new CustomRuntimeException();
            }
        }

        [Fact]
        public void TestGeneratorRaisingExceptionHasNext()
        {
            var generator = new GeneratorRaisingException();
            var enumerator = generator.GetEnumerator();
            Assert.Throws<CustomRuntimeException>(() => { enumerator.MoveNext(); });
        }

        [Fact]
        public void TestGeneratorRaisingExceptionNext()
        {
            var generator = new GeneratorRaisingException();
            var enumerator = generator.GetEnumerator();
            Assert.Throws<CustomRuntimeException>(() =>
            {
                enumerator.MoveNext();
                var t = enumerator.Current;
            });
        }
    }
}