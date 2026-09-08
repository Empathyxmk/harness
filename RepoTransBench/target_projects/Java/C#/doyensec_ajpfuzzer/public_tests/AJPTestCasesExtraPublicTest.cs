using System.Collections.Generic;
using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Public
{
    public class AJPTestCasesExtraPublicTest
    {
        [Fact]
        public void TestGetAllCasesNonEmpty()
        {
            IList<string> cases = AJPTestCases.GetAllCases();
            Assert.NotEmpty(cases);
        }

        [Fact]
        public void TestGetAllCasesContainsTest()
        {
            IList<string> cases = AJPTestCases.GetAllCases();
            bool found = false;
            foreach (var s in cases)
            {
                if (s.StartsWith("GET "))
                {
                    found = true;
                    break;
                }
            }
            Assert.True(found, "At least one case should start with 'GET '");
        }
    }
}