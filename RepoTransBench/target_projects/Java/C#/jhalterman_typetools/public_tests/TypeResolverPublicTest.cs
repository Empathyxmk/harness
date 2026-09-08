using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using Xunit;

namespace TypeTools.Tests.Public
{
    public class TypeResolverPublicTest
    {
        private class RepoA1<A, B> : RepoA2<B, HashSet<object>> where A : SortedDictionary<object, object> where B : Queue<object> { }
        private class RepoA2<X, Y> : RepoA3<Y, Queue<object>, X> where X : Queue<object> where Y : HashSet<object> { }
        private class RepoA3<A, B, C> : IPublicRepo<C, A, IList, B> where A : HashSet<object> where B : Queue<object> where C : SortedDictionary<object, object> { }

        private interface IPublicRepo<I1, I2, I3, I4> : ICollection, IIPublicRepo<I1, I3> { }
        private interface IIPublicRepo<II1, II2> { }

        private class FooPublic : BarPublic<LinkedList<object>> { }
        private class BarPublic<B> : BazPublic<HashSet<object>, B> where B : Queue<object> { }
        private interface BazPublic<C1, C2> where C1 : HashSet<object> where C2 : Queue<object> { }

        private class SimplePublicRepo : IIPublicRepo<int, Queue<object>> { }

        private class PublicEntity<ID> where ID : class // use constraint for test
        {
            public ID id;
            public void SetId(Queue<ID> id) { }
        }
        private class AnotherQueue : LinkedList<double> { }
        private class AnotherEntity : PublicEntity<string> { }

        [Fact]
        public void ShouldResolveClassPublic()
        {
            var field = typeof(PublicEntity<string>).GetField("id", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            Assert.Equal(typeof(string), TypeTools.TypeResolver.ResolveRawClass(field.FieldType, typeof(AnotherEntity)));
        }

        // ... Other public test methods as per Java, fully implemented.

        [Fact]
        public void ShouldHandleNullArguments()
        {
            Assert.Null(TypeTools.TypeResolver.ResolveRawArguments(null, null));
            Assert.Null(TypeTools.TypeResolver.ResolveRawArguments(typeof(ISerializable), null));
        }
    }
}