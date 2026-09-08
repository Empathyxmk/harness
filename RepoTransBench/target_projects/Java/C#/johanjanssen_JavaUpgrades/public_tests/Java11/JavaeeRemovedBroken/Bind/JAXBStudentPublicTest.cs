using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Public.Java11.JavaeeRemovedBroken.Bind
{
    public class JAXBStudentPublicTest
    {
        [Fact]
        public void TestStudentPublic()
        {
            var student = new JAXBStudent("Jordan", 30);
            Assert.Equal("Jordan", student.Name);
            Assert.Equal(30, student.Age);
        }
    }
}