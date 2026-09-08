using System;
using System.Collections.Generic;
using Xunit;

namespace TypeTools.Tests.Original.functional
{
    public class InnerClassTest : TypeTools.Tests.Original.AbstractTypeResolverTest
    {
        public InnerClassTest() : base(true) { }
        public InnerClassTest(bool cacheEnabled) : base(cacheEnabled) { }

        public class Foo<T> where T : struct
        {
            public class Bar : List<T> { }
        }

        public class FooPrime : Foo<int>
        {
            public class BarPrime : Bar { }
        }

        [Fact]
        public void ShouldResolveTypeArgumentOnInnerClass()
        {
            var result = TypeTools.TypeResolver.ResolveRawArgument(typeof(List<>), typeof(FooPrime.BarPrime));
            Assert.Equal(typeof(int), result);
        }
    }
}