using Xunit;
using CloudGateway;

namespace OriginalTests.CloudGateway
{
    public class FallBackMethodControllerTest
    {
        [Fact]
        public void TestDepartmentServiceFallBack()
        {
            var controller = new FallBackMethodController();
            string result = controller.DepartmentServiceFallBack("test");
            Assert.Contains("Department Service is taking longer", result);
            Assert.Contains("test", result);
        }

        [Fact]
        public void TestDepartmentServiceFallBack_NullParam()
        {
            var controller = new FallBackMethodController();
            string result = controller.DepartmentServiceFallBack(null);
            Assert.Contains("Department Service is taking longer", result);
        }
    }
}