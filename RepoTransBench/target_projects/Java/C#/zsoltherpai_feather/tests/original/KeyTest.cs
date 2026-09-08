using System;
using System.Reflection;
using System.ComponentModel.DataAnnotations;
using Xunit;

namespace Feather.Tests
{
    public class KeyTest
    {
        public class Q1 : Attribute { }

        [Fact]
        public void KeyEqualitySameType()
        {
            var k1 = Key.Of(typeof(string));
            var k2 = Key.Of(typeof(string));
            Assert.Equal(k1, k2);
            Assert.Equal(k1.GetHashCode(), k2.GetHashCode());
        }

        [Fact]
        public void KeyInequalityType()
        {
            var k1 = Key.Of(typeof(string));
            var k2 = Key.Of(typeof(int));
            Assert.NotEqual(k1, k2);
        }

        [Fact]
        public void KeyWithQualifierAnnotation()
        {
            var k1 = Key.Of(typeof(string), typeof(Q1));
            Assert.Equal(typeof(Q1), k1.Qualifier);
            Assert.Null(k1.Name);
            Assert.Equal("System.String@Q1", k1.ToString());
        }

        [Fact]
        public void KeyWithNamed()
        {
            var k1 = Key.Of(typeof(string), "name");
            Assert.Equal(typeof(System.ComponentModel.DataAnnotations.DisplayAttribute), k1.Qualifier);
            Assert.Equal("name", k1.Name);
            Assert.Equal("System.String@\"name\"", k1.ToString());
        }

        [Fact]
        public void KeyWithQualifierObject()
        {
            var q1 = new Q1();
            var k = Key.Of(typeof(string), q1);
            Assert.Equal(typeof(Q1), k.Qualifier);
            Assert.Null(k.Name);
        }

        [Fact]
        public void KeyWithNamedQualifierObject()
        {
            var n = new System.ComponentModel.DataAnnotations.DisplayAttribute { Name = "foo" };
            var k = Key.Of(typeof(string), n);
            Assert.Equal(typeof(System.ComponentModel.DataAnnotations.DisplayAttribute), k.Qualifier);
            Assert.Equal("foo", k.Name);
        }

        [Fact]
        public void EqualsAndHashCodeNullQualifierName()
        {
            var k1 = Key.Of(typeof(string));
            var k2 = Key.Of(typeof(string));
            Assert.True(k1.Equals(k2));
            Assert.Equal(k1.GetHashCode(), k2.GetHashCode());
        }

        [Fact]
        public void NotEqualsIfQualifierDiffers()
        {
            var k1 = Key.Of(typeof(string));
            var k2 = Key.Of(typeof(string), typeof(Q1));
            Assert.NotEqual(k1, k2);
        }

        [Fact]
        public void NotEqualsIfNameDiffers()
        {
            var k1 = Key.Of(typeof(string), "name1");
            var k2 = Key.Of(typeof(string), "name2");
            Assert.NotEqual(k1, k2);
        }
    }

    // Key, and display/named attribute logic would be implemented as utility types for DI in .NET; not shown here.
}