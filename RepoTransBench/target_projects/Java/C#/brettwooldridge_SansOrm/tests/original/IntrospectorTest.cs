using Xunit;

namespace SansOrm.Tests.Original
{
    public class IntrospectorTest
    {
        [Fact]
        public void ShouldCacheClassMeta()
        {
            var is1 = Introspector.GetIntrospected(typeof(TargetClass1));
            var is2 = Introspector.GetIntrospected(typeof(TargetClass1));
            Assert.NotNull(is1);
            Assert.Same(is1, is2);
        }

        public static class Introspector
        {
            private static readonly System.Collections.Concurrent.ConcurrentDictionary<System.Type, Introspected> cache
                = new System.Collections.Concurrent.ConcurrentDictionary<System.Type, Introspected>();
            public static Introspected GetIntrospected(System.Type type)
            {
                return cache.GetOrAdd(type, t => new Introspected());
            }
        }
        public class Introspected { }
        public class TargetClass1 { }
    }
}