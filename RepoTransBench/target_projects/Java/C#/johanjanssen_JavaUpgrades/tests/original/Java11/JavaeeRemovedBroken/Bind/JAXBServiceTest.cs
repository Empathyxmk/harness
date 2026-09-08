using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Original.Java11.JavaeeRemovedBroken.Bind
{
    public class JAXBServiceTest
    {
        [Fact]
        public void TestMarshalAndUnmarshal()
        {
            var student = new JAXBStudent();
            student.Id = 1;
            student.Name = "Test Student";
            var service = new JAXBService();

            var xml = service.Marshal(student);
            Assert.NotNull(xml);
            var unmarshalled = service.Unmarshal(xml);
            Assert.NotNull(unmarshalled);
            Assert.Equal(student.Id, unmarshalled.Id);
            Assert.Equal(student.Name, unmarshalled.Name);
        }

        [Fact]
        public void TestMarshalNull()
        {
            var service = new JAXBService();
            var xml = service.Marshal(null);
            Assert.Null(xml);
        }

        [Fact]
        public void TestUnmarshalNull()
        {
            var service = new JAXBService();
            var student = service.Unmarshal(null);
            Assert.Null(student);
        }
    }
}