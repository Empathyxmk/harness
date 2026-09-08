using Xunit;
using FluentAssertions;
using Ch02Core.Hamcrest;

namespace OriginalTests.Hamcrest
{
    public class HamcrestMatchersTest
    {
        private const string FIRST_NAME = "John";
        private const string LAST_NAME = "Smith";
        private readonly Customer _customer = new Customer(FIRST_NAME, LAST_NAME);

        [Fact(DisplayName = "Hamcrest is, anyOf, allOf")]
        public void TestHamcrestIs()
        {
            int price1 = 1, price2 = 1, price3 = 2;
            price1.Should().Be(1);
            new[] { price2, price3 }.Should().Contain(1);
            price1.Should().Be(price2);
        }

        [Fact(DisplayName = "Null expected")]
        public void TestNull()
        {
            object? obj = null;
            obj.Should().BeNull();
        }

        [Fact(DisplayName = "Object expected")]
        public void TestNotNull()
        {
            _customer.Should().NotBeNull();
        }

        [Fact(DisplayName = "Check correct customer properties")]
        public void CheckCorrectCustomerProperties()
        {
            _customer.FirstName.Should().Be(FIRST_NAME);
            _customer.LastName.Should().Be(LAST_NAME);
        }
    }
}