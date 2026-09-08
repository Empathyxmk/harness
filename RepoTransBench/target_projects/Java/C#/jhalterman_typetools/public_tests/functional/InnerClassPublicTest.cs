using System;
using System.Collections.Generic;
using Xunit;

namespace TypeTools.Tests.Public.functional
{
    public class InnerClassPublicTest
    {
        private class OuterPublic<A>
        {
            public class Inner<B> { }
            public class InnerSet : Inner<HashSet<A>> { }
            public class InnerHashSet : Inner<HashSet<HashSet<A>>> { }
        }

        [Fact]
        public void ResolveRawArgumentForInnerSet()
        {
            Assert.Equal(typeof(HashSet<>), TypeTools.TypeResolver.ResolveRawArgument(typeof(HashSet<>), typeof(OuterPublic<int>.InnerSet)).GetGenericTypeDefinition());
        }

        [Fact]
        public void ResolveRawArgumentForInnerHashSet()
        {
            Assert.Equal(typeof(HashSet<>), TypeTools.TypeResolver.ResolveRawArgument(typeof(HashSet<>), typeof(OuterPublic<int>.InnerHashSet)).GetGenericTypeDefinition());
            Assert.Equal(typeof(HashSet<>), TypeTools.TypeResolver.ResolveRawArgument(typeof(HashSet<>), typeof(OuterPublic<int>.InnerHashSet)).GetGenericTypeDefinition());
        }
    }
}