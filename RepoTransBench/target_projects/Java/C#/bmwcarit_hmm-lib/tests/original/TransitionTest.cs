using System;
using Xunit;
using BmwcaritHmmLib;

namespace OriginalTests
{
    public class TransitionTest
    {
        [Fact]
        public void TestEqualsAndHashCode()
        {
            var t1 = new Transition<string>("A", "B");
            var t2 = new Transition<string>("A", "B");
            var t3 = new Transition<string>("B", "A");
            var t4 = new Transition<string>("A", "C");
            Assert.Equal(t1, t2);
            Assert.Equal(t1.GetHashCode(), t2.GetHashCode());
            Assert.NotEqual(t1, t3);
            Assert.NotEqual(t1.GetHashCode(), t3.GetHashCode());
            Assert.NotEqual(t1, t4);
        }

        [Fact]
        public void TestEqualsWithNulls()
        {
            var t1 = new Transition<string>(null, "B");
            var t2 = new Transition<string>(null, "B");
            var t3 = new Transition<string>("A", null);
            var t4 = new Transition<string>(null, null);
            var t5 = new Transition<string>(null, null);

            Assert.Equal(t1, t2);
            Assert.Equal(t4, t5);
            Assert.NotEqual(t1, t3);
        }

        [Fact]
        public void TestToString()
        {
            var t = new Transition<string>("A", "B");
            Assert.Contains("fromCandidate=A", t.ToString());
            Assert.Contains("toCandidate=B", t.ToString());
        }

        [Fact]
        public void TestNotEqualsOtherTypesAndNull()
        {
            var t = new Transition<string>("A", "B");
            Assert.False(t.Equals(null));
            Assert.False(t.Equals("not_a_transition"));
        }
    }
}