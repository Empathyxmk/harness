using System;
using System.Reflection;
using Xunit;
using SystraceGradlePlugin;

namespace PublicTests
{
    public class ReflectUtilPublicTest
    {
        class RootClass
        {
            private int rootPrivate = 88;
            private int onlyRoot = 202;
            private string rootField = "baz";
            public string rootPublic = "yo";
            public void RootMethod() { }
            private void OnlyRootMethod() { }
        }

        class DerivedClass : RootClass
        {
            private int derivedPrivate = 99;
            private string derivedField = "qux";
            public void QuxMethod() { }
            private void Mystery() { }
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveOwnClassPublic()
        {
            var f = ReflectUtil.GetDeclaredFieldRecursive(typeof(DerivedClass), "derivedPrivate");
            Assert.NotNull(f);
            var obj = new DerivedClass();
            var value = (int)f.GetValue(obj);
            Assert.Equal(99, value);
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveSuperClassPublic()
        {
            var f = ReflectUtil.GetDeclaredFieldRecursive(typeof(DerivedClass), "rootPrivate");
            Assert.NotNull(f);
            var obj = new DerivedClass();
            var value = (int)f.GetValue(obj);
            Assert.Equal(88, value);
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveNotFoundPublic()
        {
            Assert.Throws<MissingFieldException>(() =>
            {
                ReflectUtil.GetDeclaredFieldRecursive(typeof(DerivedClass), "noSuchField");
            });
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveBadTypePublic()
        {
            Assert.Throws<ArgumentException>(() =>
            {
                ReflectUtil.GetDeclaredFieldRecursive(new object(), "derivedPrivate");
            });
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveClassNameStringPublic()
        {
            var typeFull = typeof(DerivedClass).FullName + ", " + typeof(DerivedClass).Assembly.GetName().Name;
            var f = ReflectUtil.GetDeclaredFieldRecursive(typeFull, "derivedPrivate");
            Assert.NotNull(f);
            var obj = new DerivedClass();
            var value = (int)f.GetValue(obj);
            Assert.Equal(99, value);
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveOwnClassPublic()
        {
            var m = ReflectUtil.GetDeclaredMethodRecursive(typeof(DerivedClass), "Mystery");
            Assert.NotNull(m);
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveSuperClassPublic()
        {
            var m = ReflectUtil.GetDeclaredMethodRecursive(typeof(DerivedClass), "OnlyRootMethod");
            Assert.NotNull(m);
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveNotFoundPublic()
        {
            Assert.Throws<MissingMethodException>(() =>
            {
                ReflectUtil.GetDeclaredMethodRecursive(typeof(DerivedClass), "notFoundPublicMethod");
            });
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveBadTypePublic()
        {
            Assert.Throws<ArgumentException>(() =>
            {
                ReflectUtil.GetDeclaredMethodRecursive(true, "Mystery");
            });
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveClassNameStringPublic()
        {
            var typeFull = typeof(DerivedClass).FullName + ", " + typeof(DerivedClass).Assembly.GetName().Name;
            var m = ReflectUtil.GetDeclaredMethodRecursive(typeFull, "Mystery");
            Assert.NotNull(m);
        }

        [Fact]
        public void TestPrivateConstructorPublic()
        {
            Assert.Throws<NotSupportedException>(() => new PrivateCtorClass());
            Assert.Throws<NotSupportedException>(() => new ReflectUtil());
        }

        private class PrivateCtorClass : ReflectUtil
        {
        }
    }
}