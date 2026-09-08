using System;
using System.Reflection;
using Xunit;

namespace XegerLib.Tests.Public
{
    public class XegerCoveragePublicTest
    {
        [Fact]
        public void TestConstructorWithRandom()
        {
            var xeger = new Xeger("xyz|uvw", new Random(321));
            Assert.NotNull(xeger);
            Assert.NotNull(xeger.GetRandom());
        }

        [Fact]
        public void TestSetAndGetRandom()
        {
            var xeger = new Xeger("b+", new Random(4545));
            var r = new Random(999);
            xeger.SetRandom(r);
            Assert.Same(r, xeger.GetRandom());
        }

        [Fact]
        public void TestGenerateSimpleLiteral()
        {
            var xeger = new Xeger("acd", new Random(222));
            string generated = xeger.Generate();
            Assert.Equal("acd", generated);
        }

        [Fact]
        public void TestGenerateWithDefaultRandom()
        {
            var xeger = new Xeger("z");
            string generated = xeger.Generate();
            Assert.Equal("z", generated);
        }

        [Fact]
        public void TestGetRandomIntWorksOnSimpleCases()
        {
            int result = Xeger.GetRandomInt(8, 8, new Random(5));
            Assert.Equal(8, result);

            int result2 = Xeger.GetRandomInt(2, 8, new Random(7));
            Assert.InRange(result2, 2, 8);
        }

        [Fact]
        public void TestGenerateWithBoundedLengthThrowsMinimum()
        {
            var xeger = new Xeger("b?", new Random(4));
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
            var xeger = new Xeger("b{5}", new Random(4));
            var ex = Assert.Throws<Xeger.FailedRandomWalkException>(() =>
            {
                xeger.Generate(1, 3); // regex "b{5}" requires at least 5 chars, max is lower
            });
            Assert.Contains("exceeded maximum walk length", ex.Message.ToLowerInvariant());
        }

        [Fact]
        public void TestGenerateWithBoundedLengthProducesAcceptableLength()
        {
            var xeger = new Xeger("c{1,3}", new Random(5));
            string val = xeger.Generate(1, 3);
            Assert.Matches(@"c{1,3}", val);
            Assert.InRange(val.Length, 1, 3);
        }

        [Fact]
        public void TestFailedRandomWalkException()
        {
            var ex = new Xeger.FailedRandomWalkException("another fail");
            Assert.NotNull(ex.Message);
            Assert.Equal("another fail", ex.Message);
        }

        [Fact]
        public void TestAppendRandomChoiceMinLength()
        {
            var xeger = new Xeger("ba?", new Random(8));

            var method = typeof(Xeger).GetMethod("AppendRandomChoice", BindingFlags.NonPublic | BindingFlags.Instance);
            Assert.NotNull(method);

            var stateType = Type.GetType("DK.Brics.Automaton.State, DK.Brics.Automaton");
            if (stateType == null)
                throw new Exception("Automaton State type not found. Check that DK.Brics.Automaton is referenced.");

            object st = new DK.Brics.Automaton.RegExp("b?a").ToAutomaton().InitialState;

            var sb = new System.Text.StringBuilder();
            var result = method.Invoke(xeger, new object[] { sb, st, 0, 0 });
            Assert.NotNull(result);
        }
    }
}