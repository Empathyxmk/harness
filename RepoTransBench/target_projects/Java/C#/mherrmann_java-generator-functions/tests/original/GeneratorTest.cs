using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using Xunit;
using GeneratorLib;

namespace OriginalTests
{
    public class GeneratorTest
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
            List<int> oneEltList = new List<int> { 1 };
            Assert.Equal(oneEltList, List(new ListGenerator<int>(oneEltList)));
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
            List<int> twoEltList = new List<int> { 1, 2 };
            Assert.Equal(twoEltList, List(new ListGenerator<int>(twoEltList)));
        }

        [Fact]
        public void TestInfiniteGenerator()
        {
            InfiniteGenerator generator = new InfiniteGenerator();
            TestInfiniteGenerator(generator);
        }

        private void TestInfiniteGenerator(InfiniteGenerator generator)
        {
            int NUM_ELTS_TO_INSPECT = 1000;
            var generatorEnumerator = generator.GetEnumerator();
            for (int i = 0; i < NUM_ELTS_TO_INSPECT; i++)
            {
                Assert.True(generatorEnumerator.MoveNext());
                Assert.Equal(1, generatorEnumerator.Current);
            }
        }

        private class InfiniteGenerator : Generator<int>
        {
            protected override void run()
            {
                while (true)
                    yield(1);
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

        private class GeneratorRaisingException : Generator<int>
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