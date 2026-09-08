using System;
using Xunit;

namespace Feather.Tests
{
    public class TransitiveDependencyTest
    {
        [Fact]
        public void Transitive()
        {
            var feather = FeatherBase.With();
            var a = (A)feather.Instance(typeof(A));
            Assert.NotNull(a.BField.CField);
        }

        public class A
        {
            public B BField { get; }
            public A(B b)
            {
                BField = b;
            }
        }

        public class B
        {
            public C CField { get; }
            public B(C c)
            {
                CField = c;
            }
        }

        public class C { }
    }
}