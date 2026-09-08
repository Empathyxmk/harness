using System.Linq;
using Xunit;
using Jkrasnay.SqlBuilder;

namespace Jkrasnay.SqlBuilder.PublicTests
{
    public class UniqueStringGeneratorPublicTests
    {
        [Fact]
        public void UniqueStringsGeneratedOfCorrectLength()
        {
            var gen = new UniqueStringGenerator(5);
            var s1 = gen.Get();
            var s2 = gen.Get();
            var s3 = gen.Get();
            Assert.Equal(5, s1.Length);
            Assert.Equal(5, s2.Length);
            Assert.Equal(5, s3.Length);
            Assert.NotEqual(s1, s2);
            Assert.NotEqual(s2, s3);
            Assert.NotEqual(s1, s3);
        }
    }
}