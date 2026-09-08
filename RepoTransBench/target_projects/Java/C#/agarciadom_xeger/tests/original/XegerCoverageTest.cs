using System;
using System.Reflection;
using Xunit;

namespace XegerLib.Tests.Original
{
    public class XegerCoverageTest
    {
        [Fact]
        public void TestConstructorWithRandom()
        {
            var xeger = new Xeger("abc|def", new Random(123));
            Assert.NotNull(xeger);
            Assert.NotNull(xeger.GetRandom());
        }

        [Fact]
        public void TestSetAndGetRandom()
        {
            var xeger = new Xeger("a+", new Random(123));
            var r = new Random(456);
            xeger.SetRandom(r);
            Assert.Same(r, xeger.GetRandom());
        }

        [Fact]
        public void TestGenerateSimpleLiteral()
        {
            var xeger = new Xeger("abc", new Random(321));
            string generated = xeger.Generate();
            Assert.Equal("abc", generated);
        }

        [Fact]
        public void TestGenerateWithDefaultRandom()
        {
            var xeger = new Xeger("b");
            string generated = xeger.Generate();
            Assert.Equal("b", generated);
        }

        [Fact]
        public void TestGetRandomIntWorksOnSimpleCases()
        {
            int result = Xeger.GetRandomInt(5, 5, new Random(1));
            Assert.Equal(5, result);

            int result2 = Xeger.GetRandomInt(1, 10, new Random(1));
            Assert.InRange(result2, 1, 10);
        }

        [Fact]
        public void TestGenerateWithBoundedLengthThrowsMinimum()
        {
            var xeger = new Xeger("a?", new Random(1));
            var ex = Assert.Throws<Xeger.FailedRandomWalkException>(() =>
            {
                xeger.Generate(2, 2);
            });
            Assert.True(
                ex.Message.Contains("current = 0 < min = 2")
                || ex.Message.Contains("current = 1 < min = 2")
            );
        }

        [Fact]
        public void TestGenerateWithBoundedLengthThrowsMaximum()
        {
            var xeger = new Xeger("a{3}", new Random(1));
            var ex = Assert.Throws<Xeger.FailedRandomWalkException>(() =>
            {
                xeger.Generate(1, 2); // regex "a{3}" requires at least 3 chars, max is lower
            });
            Assert.Contains("exceeded maximum walk length", ex.Message.ToLowerInvariant());
        }

        [Fact]
        public void TestGenerateWithBoundedLengthProducesAcceptableLength()
        {
            var xeger = new Xeger("a{2,4}", new Random(2));
            string val = xeger.Generate(2, 4);
            Assert.Matches(@"a{2,4}", val);
            Assert.InRange(val.Length, 2, 4);
        }

        [Fact]
        public void TestFailedRandomWalkException()
        {
            var ex = new Xeger.FailedRandomWalkException("fail");
            Assert.NotNull(ex.Message);
            Assert.Equal("fail", ex.Message);
        }

        [Fact]
        public void TestAppendRandomChoiceMinLength()
        {
            // Assumes that appendRandomChoice exists and is accessible (via reflection) in C#
            var xeger = new Xeger("ab?", new Random(3));

            // Use reflection to call the internal method
            var method = typeof(Xeger).GetMethod("AppendRandomChoice", BindingFlags.NonPublic | BindingFlags.Instance);
            Assert.NotNull(method);

            // State simulation and binding
            var stateType = Type.GetType("DK.Brics.Automaton.State, DK.Brics.Automaton");
            if (stateType == null)
                throw new Exception("Automaton State type not found. Check that DK.Brics.Automaton is referenced.");

            object st = new DK.Brics.Automaton.RegExp("a?b").ToAutomaton().InitialState;

            var sb = new System.Text.StringBuilder();
            var result = method.Invoke(xeger, new object[] { sb, st, 0, 0 });
            Assert.NotNull(result); // should return something (optionally check type)
        }
    }
}