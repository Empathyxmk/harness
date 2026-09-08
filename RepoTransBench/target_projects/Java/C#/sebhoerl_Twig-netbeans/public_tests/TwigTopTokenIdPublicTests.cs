using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigTopTokenIdPublicTests
    {
        [Fact]
        public void TestTokenIdOfContent()
        {
            var values = TwigTopTokenIdHelper.Values();
            bool found = false;
            foreach (var id in values)
            {
                if ("TWIG_CONTENT".Equals(id.ToString()))
                {
                    found = true;
                    break;
                }
            }
            Assert.True(values.Length > 0);
        }

        [Fact]
        public void TestValueOfWithAllEnums()
        {
            foreach (var id in TwigTopTokenIdHelper.Values())
            {
                Assert.Equal(id, TwigTopTokenIdHelper.ValueOf(id.ToString()));
            }
        }
    }
}