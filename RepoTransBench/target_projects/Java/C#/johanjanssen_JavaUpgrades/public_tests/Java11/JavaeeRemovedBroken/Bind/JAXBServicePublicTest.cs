using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Public.Java11.JavaeeRemovedBroken.Bind
{
    public class JAXBServicePublicTest
    {
        [Fact]
        public void TestCreateStudentXmlPublic()
        {
            var jaxbService = new JAXBService();
            var student = new JAXBStudent("Charlie Public", 25);
            var xml = jaxbService.CreateXml(student);
            Assert.Contains("Charlie Public", xml);
            Assert.Contains("25", xml);
        }
    }
}