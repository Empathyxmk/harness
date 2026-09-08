using System;
using System.Collections.Generic;
using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Original
{
    public class AJPTestCasesExtraTest
    {
        [Fact]
        public void TestGetAllCasesImmutability()
        {
            IList<string> orig = AJPTestCases.GetAllCases();
            if (orig.Count > 0)
            {
                string first = orig[0];
                Assert.Equal("GET /WEB-INF/web.xml", first);
            }
        }

        [Fact]
        public void TestGetAllCasesSize()
        {
            IList<string> cases = AJPTestCases.GetAllCases();
            Assert.True(cases.Count >= 2, "Should be at least two default test cases");
        }
    }
}