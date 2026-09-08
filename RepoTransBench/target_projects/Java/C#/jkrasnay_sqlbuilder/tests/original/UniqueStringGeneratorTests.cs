using System;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.Tests.Original
{
    public class UniqueStringGeneratorTests
    {
        [Fact]
        public void TestHappyPath()
        {
            var gen = new UniqueStringGenerator(8);
            var s1 = gen.Get();
            var s2 = gen.Get();

            Assert.Equal(8, s1.Length);
            Assert.Equal(8, s2.Length);
            Assert.NotEqual(s1, s2);
        }

        [Fact]
        public void TestInoffensive()
        {
            var gen = new UniqueStringGenerator(8);
            Assert.False(gen.IsOffensive("puppies"));
            Assert.False(gen.IsOffensive("muffins"));
            Assert.True(gen.IsOffensive("fvck"));
            Assert.True(gen.IsOffensive("abcshitdef"));
            Assert.True(gen.IsOffensive("abcsh1tdef"));
            Assert.True(gen.IsOffensive("1a552"));
        }
    }
}