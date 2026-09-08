using System;
using Xunit;
using BmwcaritHmmLib;

namespace PublicTests
{
    public class TransitionPublicTest
    {
        [Fact]
        public void TestEqualsAndHashCodePublic()
        {
            var t1 = new Transition<string>("X", "Y");
            var t2 = new Transition<string>("X", "Y");
            var t3 = new Transition<string>("Y", "Z");
            var t4 = new Transition<string>("X", "Z");
            Assert.Equal(t1, t2);
            Assert.Equal(t1.GetHashCode(), t2.GetHashCode());
            Assert.NotEqual(t1, t3);
            Assert.NotEqual(t1.GetHashCode(), t3.GetHashCode());
            Assert.NotEqual(t1, t4);
        }

        [Fact]
        public void TestEqualsWithNullsPublic()
        {
            var t1 = new Transition<string>(null, "Y");
            var t2 = new Transition<string>(null, "Y");
            var t3 = new Transition<string>("X", null);
            var t4 = new Transition<string>(null, null);
            var t5 = new Transition<string>(null, null);

            Assert.Equal(t1, t2);
            Assert.Equal(t4, t5);
            Assert.NotEqual(t1, t3);
        }

        [Fact]
        public void TestToStringPublic()
        {
            var t = new Transition<string>("Q", "P");
            Assert.Contains("fromCandidate=Q", t.ToString());
            Assert.Contains("toCandidate=P", t.ToString());
        }

        [Fact]
        public void TestNotEqualsOtherTypesAndNullPublic()
        {
            var t = new Transition<string>("I", "J");
            Assert.False(t.Equals(null));
            Assert.False(t.Equals(12345));
        }
    }
}