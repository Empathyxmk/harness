using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Xunit;
using FluentAssertions;
using Jkrasnay.SqlBuilder.Orm;

namespace Jkrasnay.SqlBuilder.Tests.Original.Orm
{
    public class ReflectionUtilsTests
    {
        private class Address
        {
            public string street;
        }

        private class Person
        {
            public string name;
            public Address address;
        }

        [Fact]
        public void TestGetDeclaredFieldWithPath()
        {
            var field = ReflectionUtils.GetDeclaredFieldWithPath(typeof(Person), "name");
            field.Name.Should().Be("name");
            Assert.Equal(typeof(string), field.FieldType);
            Assert.Equal(typeof(Person), field.DeclaringType);

            field = ReflectionUtils.GetDeclaredFieldWithPath(typeof(Person), "address.street");
            field.Name.Should().Be("street");
            Assert.Equal(typeof(string), field.FieldType);
            Assert.Equal(typeof(Address), field.DeclaringType);
        }

        [Fact]
        public void TestGetFieldWithPath()
        {
            var person = new Person();
            person.name = "Joe";
            ReflectionUtils.GetFieldValueWithPath(person, "name").Should().Be("Joe");
            ReflectionUtils.GetFieldValueWithPath(person, "address.street").Should().BeNull();

            person.address = new Address();
            ReflectionUtils.GetFieldValueWithPath(person, "address.street").Should().BeNull();

            person.address.street = "123 Main";
            ReflectionUtils.GetFieldValueWithPath(person, "address.street").Should().Be("123 Main");
        }

        [Fact]
        public void TestSetFieldWithPath()
        {
            var person = new Person();
            ReflectionUtils.SetFieldValueWithPath(person, "name", "Joe");
            Assert.Equal("Joe", person.name);

            try
            {
                ReflectionUtils.SetFieldValueWithPath(person, "address.street", "123 Main");
                Assert.True(false);
            }
            catch (InvalidOperationException)
            {
            }

            person.address = new Address();
            ReflectionUtils.SetFieldValueWithPath(person, "address.street", "123 Main");
            Assert.Equal("123 Main", person.address.street);
        }
    }
}