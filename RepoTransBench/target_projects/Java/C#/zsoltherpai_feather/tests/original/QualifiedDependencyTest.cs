using System;
using Xunit;

namespace Feather.Tests
{
    public class QualifiedDependencyTest
    {
        [Fact]
        public void QualifiedInstances()
        {
            var feather = FeatherBase.With(new Module());
            Assert.Equal(typeof(FooA), feather.Instance(Key.Of(typeof(IFoo), typeof(A))));
            Assert.Equal(typeof(FooB), feather.Instance(Key.Of(typeof(IFoo), typeof(B))));
        }

        [Fact]
        public void InjectedQualified()
        {
            var feather = FeatherBase.With(new Module());
            var dummy = (Dummy)feather.Instance(typeof(Dummy));
            Assert.Equal(typeof(FooB), dummy.Foo.GetType());
        }

        [Fact]
        public void FieldInjectedQualified()
        {
            var feather = FeatherBase.With(new Module());
            var dummy = new DummyTestUnit();
            feather.InjectFields(dummy);
            Assert.Equal(typeof(FooA), dummy.Foo.GetType());
        }

        public interface IFoo { }
        public class FooA : IFoo { }
        public class FooB : IFoo { }

        [AttributeUsage(AttributeTargets.All)]
        public class A : Attribute { }

        [AttributeUsage(AttributeTargets.All)]
        public class B : Attribute { }

        public class Module
        {
            [Provides, A]
            public IFoo AFoo(FooA fooA) => fooA;
            [Provides, B]
            public IFoo BFoo(FooB fooB) => fooB;
        }

        public class Dummy
        {
            public IFoo Foo { get; }
            public Dummy([B] IFoo foo)
            {
                Foo = foo;
            }
        }

        public class DummyTestUnit
        {
            [A]
            public IFoo Foo { get; set; }
        }
    }
    public class ProvidesAttribute : Attribute { }
}