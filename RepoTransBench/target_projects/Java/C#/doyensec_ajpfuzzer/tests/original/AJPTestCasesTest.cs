using System;
using System.Collections.Generic;
using Xunit;
using Doyensec.Ajpfuzzer;

namespace Doyensec.Ajpfuzzer.Tests.Original
{
    public class AJPTestCasesTest
    {
        [Fact]
        public void TestGetAllCasesReturnsNonEmptyList()
        {
            IList<string> cases = AJPTestCases.GetAllCases();
            Assert.NotNull(cases);
            Assert.NotEmpty(cases);
        }

        [Fact]
        public void TestCaseContainsKnownAttackPayloads()
        {
            IList<string> cases = AJPTestCases.GetAllCases();
            string found = null;
            foreach (var s in cases)
            {
                if (s.Contains("/WEB-INF/web.xml"))
                {
                    found = s;
                    break;
                }
            }
            Assert.NotNull(found);
        }

        [Fact]
        public void TestListIsUnmodifiable()
        {
            IList<string> c1 = AJPTestCases.GetAllCases();
            Assert.Throws<NotSupportedException>(() => ((IList<string>)c1).Add("test-case"));
        }
    }
}