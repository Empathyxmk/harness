using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Original.Java11.JavaeeRemovedBroken.Bind
{
    public class JAXBStudentTest
    {
        [Fact]
        public void TestAllArgsConstructorAndAccessors()
        {
            var student = new JAXBStudent(2, "Jane Doe");
            Assert.Equal(2, student.Id);
            Assert.Equal("Jane Doe", student.Name);

            student.Id = 3;
            student.Name = "John Smith";
            Assert.Equal(3, student.Id);
            Assert.Equal("John Smith", student.Name);
        }

        [Fact]
        public void TestToStringNotNull()
        {
            var student = new JAXBStudent(42, "Test User");
            Assert.NotNull(student.ToString());
            Assert.Contains("42", student.ToString());
            Assert.Contains("Test User", student.ToString());
        }
    }
}