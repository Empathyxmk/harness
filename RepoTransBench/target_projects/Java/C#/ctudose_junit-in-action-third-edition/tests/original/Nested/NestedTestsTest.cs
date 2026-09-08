using Xunit;
using Ch02Core.Nested;
using System;

namespace OriginalTests.Nested
{
    public class NestedTestsTest
    {
        private const string FIRST_NAME = "John";
        private const string LAST_NAME = "Smith";

        public class BuilderTest
        {
            private const string MIDDLE_NAME = "Michael";

            [Fact]
            public void CustomerBuilder()
            {
                DateTime customerDate = new DateTime(2019, 4, 21);
                var customer = new Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME)
                    .WithMiddleName(MIDDLE_NAME)
                    .WithBecomeCustomer(customerDate)
                    .Build();

                Assert.Equal(Gender.MALE, customer.Gender);
                Assert.Equal(FIRST_NAME, customer.FirstName);
                Assert.Equal(LAST_NAME, customer.LastName);
                Assert.Equal(MIDDLE_NAME, customer.MiddleName);
                Assert.Equal(customerDate, customer.BecomeCustomer);
            }
        }

        public class CustomerEqualsTest
        {
            private const string OTHER_FIRST_NAME = "John";
            private const string OTHER_LAST_NAME = "Doe";

            [Fact]
            public void TestDifferentCustomers()
            {
                var customer = new Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME)
                    .Build();
                var otherCustomer = new Customer.Builder(Gender.MALE, OTHER_FIRST_NAME, OTHER_LAST_NAME)
                    .Build();
                Assert.NotEqual(customer, otherCustomer);
            }

            [Fact]
            public void TestSameCustomer()
            {
                var customer = new Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME).Build();
                var otherCustomer = new Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME).Build();

                Assert.Equal(customer, otherCustomer);
                Assert.NotSame(customer, otherCustomer); // reference equality, should not be the same instance
            }
        }

        public class CustomerHashCodeTest
        {
            private const string OTHER_FIRST_NAME = "John";
            private const string OTHER_LAST_NAME = "Doe";

            [Fact]
            public void TestDifferentCustomers()
            {
                var customer = new Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME)
                    .Build();
                var otherCustomer = new Customer.Builder(Gender.MALE, OTHER_FIRST_NAME, OTHER_LAST_NAME)
                    .Build();
                Assert.NotEqual(customer.GetHashCode(), otherCustomer.GetHashCode());
            }

            [Fact]
            public void TestSameCustomer()
            {
                var customer = new Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME)
                    .Build();
                var otherCustomer = new Customer.Builder(Gender.MALE, FIRST_NAME, LAST_NAME)
                    .Build();
                Assert.Equal(customer.GetHashCode(), otherCustomer.GetHashCode());
            }
        }
    }
}