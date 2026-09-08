using Xunit;
using Ch02Core.Tags;

namespace OriginalTests.Tags
{
    public class CustomerTest
    {
        private const string CUSTOMER_NAME = "John Smith";

        [Fact]
        public void TestCustomer()
        {
            var customer = new Customer(CUSTOMER_NAME);
            Assert.Equal("John Smith", customer.Name);
        }
    }
}