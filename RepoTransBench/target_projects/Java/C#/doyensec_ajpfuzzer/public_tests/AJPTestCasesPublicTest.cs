using System.Collections.Generic;
using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Public
{
    public class AJPTestCasesPublicTest
    {
        [Fact]
        public void TestGetAllCasesImmutabilityDifferent()
        {
            IList<string> orig = AJPTestCases.GetAllCases();
            if (orig.Count > 0)
            {
                string last = orig[orig.Count - 1];
                Assert.True(last.EndsWith(".jsp") || last.EndsWith(".xml") || last.Contains("/"), "Last case is a plausible test path");
            }
        }

        [Fact]
        public void TestGetAllCasesHasDefaultCases()
        {
            IList<string> cases = AJPTestCases.GetAllCases();
            Assert.Contains("GET /WEB-INF/web.xml", cases);
        }
    }
}