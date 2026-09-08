using System;
using System.Reflection;
using Xunit;
using SystraceGradlePlugin;

namespace TestsOriginal
{
    public class ReflectUtilTest
    {
        class SuperClass
        {
            private int superPrivate = 44;
            private int onlySuper = 101;
            private string field = "foo";
            public string superPublic = "hey";
            public void SuperMethod() { }
            private void OnlySuperMethod() { }
        }

        class SubClass : SuperClass
        {
            private int subPrivate = 55;
            private string subField = "bar";
            public void Bar() { }
            private void Secret() { }
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveOwnClass()
        {
            var f = ReflectUtil.GetDeclaredFieldRecursive(typeof(SubClass), "subPrivate");
            Assert.NotNull(f);
            var obj = new SubClass();
            var value = (int)f.GetValue(obj);
            Assert.Equal(55, value);
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveSuperClass()
        {
            var f = ReflectUtil.GetDeclaredFieldRecursive(typeof(SubClass), "superPrivate");
            Assert.NotNull(f);
            var obj = new SubClass();
            var value = (int)f.GetValue(obj);
            Assert.Equal(44, value);
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveNotFound()
        {
            Assert.Throws<MissingFieldException>(() =>
            {
                ReflectUtil.GetDeclaredFieldRecursive(typeof(SubClass), "nonexistent");
            });
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveBadType()
        {
            Assert.Throws<ArgumentException>(() =>
            {
                ReflectUtil.GetDeclaredFieldRecursive(1234, "subPrivate");
            });
        }

        [Fact]
        public void TestGetDeclaredFieldRecursiveClassNameString()
        {
            var typeFull = typeof(SubClass).FullName + ", " + typeof(SubClass).Assembly.GetName().Name;
            var f = ReflectUtil.GetDeclaredFieldRecursive(typeFull, "subPrivate");
            Assert.NotNull(f);
            var obj = new SubClass();
            var value = (int)f.GetValue(obj);
            Assert.Equal(55, value);
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveOwnClass()
        {
            var m = ReflectUtil.GetDeclaredMethodRecursive(typeof(SubClass), "Secret");
            Assert.NotNull(m);
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveSuperClass()
        {
            var m = ReflectUtil.GetDeclaredMethodRecursive(typeof(SubClass), "OnlySuperMethod");
            Assert.NotNull(m);
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveNotFound()
        {
            Assert.Throws<MissingMethodException>(() =>
            {
                ReflectUtil.GetDeclaredMethodRecursive(typeof(SubClass), "notFoundMethod");
            });
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveBadType()
        {
            Assert.Throws<ArgumentException>(() =>
            {
                ReflectUtil.GetDeclaredMethodRecursive(5.6, "Secret");
            });
        }

        [Fact]
        public void TestGetDeclaredMethodRecursiveClassNameString()
        {
            var typeFull = typeof(SubClass).FullName + ", " + typeof(SubClass).Assembly.GetName().Name;
            var m = ReflectUtil.GetDeclaredMethodRecursive(typeFull, "Secret");
            Assert.NotNull(m);
        }

        [Fact]
        public void TestPrivateConstructor()
        {
            Assert.Throws<NotSupportedException>(() => new PrivateCtorClass());
            Assert.Throws<NotSupportedException>(() => new ReflectUtil());
        }

        private class PrivateCtorClass : ReflectUtil
        {
        }
    }
}