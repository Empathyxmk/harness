using Xunit;
using CloudGateway;

namespace PublicTests.CloudGateway
{
    public class FallBackMethodControllerPublicTest
    {
        [Fact]
        public void TestDepartmentServiceFallBackWithAnotherParam()
        {
            var controller = new FallBackMethodController();
            string input = "publicExample";
            string result = controller.DepartmentServiceFallBack(input);
            Assert.Contains("Department Service is taking longer", result);
            Assert.Contains(input, result);
        }

        [Fact]
        public void TestDepartmentServiceFallBack_EmptyStringParam()
        {
            var controller = new FallBackMethodController();
            string result = controller.DepartmentServiceFallBack("");
            Assert.Contains("Department Service is taking longer", result);
            // It should also work with an empty string as parameter and return the fallback message
        }
    }
}