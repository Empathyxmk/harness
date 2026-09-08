using Xunit;
using Ch02Core.Tags;

namespace OriginalTests.Tags
{
    public class CustomersRepositoryTest
    {
        private const string CUSTOMER_NAME = "John Smith";
        private CustomersRepository repository = new CustomersRepository();

        [Fact]
        public void TestNonExistence()
        {
            bool exists = repository.Contains("John Smith");
            Assert.False(exists);
        }

        [Fact]
        public void TestCustomerPersistence()
        {
            repository.Persist(new Customer(CUSTOMER_NAME));
            Assert.True(repository.Contains("John Smith"));
        }
    }
}