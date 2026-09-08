using System;
using Xunit;
using ApereoCasAttack;

namespace PublicTests
{
    public class AppPublicTests
    {
        // "containsCasLowerOnly" utility mimics Java public test's helper
        private bool ContainsCasLowerOnly(string s)
        {
            return s != null && s.Contains("cas");
        }

        [Fact]
        public void TestContainsCasSubstring_Public()
        {
            Assert.True(ContainsCasLowerOnly("this has cas inside"));
            Assert.True(ContainsCasLowerOnly("xcasY"));
            Assert.True(ContainsCasLowerOnly("casual"));
        }

        [Fact]
        public void TestDoesNotContainCasSubstring_Public()
        {
            Assert.False(ContainsCasLowerOnly("CASE"));
            Assert.False(ContainsCasLowerOnly("archive"));
            Assert.False(ContainsCasLowerOnly("security"));
        }

        [Fact]
        public void TestPerformAttack_CasPresent_Public()
        {
            string target = "attackcas2024";
            string expected = "Simulating CAS attack on attackcas2024";
            Assert.Equal(expected, App.PerformAttack(target));
        }

        [Fact]
        public void TestPerformAttack_CasAbsent_Public()
        {
            string target = "adminpanel";
            string expected = "Target is not a CAS server: adminpanel";
            Assert.Equal(expected, App.PerformAttack(target));
        }

        [Fact]
        public void TestPerformAttack_OnlyCasWord_Public()
        {
            string target = "CaS";
            string expected = "Target is not a CAS server: CaS";
            Assert.Equal(expected, App.PerformAttack(target));
        }

        [Fact]
        public void TestPerformAttack_CasInMiddle_Public()
        {
            string target = "alphaCasOmega";
            string expected = "Target is not a CAS server: alphaCasOmega";
            Assert.Equal(expected, App.PerformAttack(target));
        }

        [Fact]
        public void TestPerformAttack_StartsWithCas_Public()
        {
            string target = "casualty";
            string expected = "Simulating CAS attack on casualty";
            Assert.Equal(expected, App.PerformAttack(target));
        }

        [Fact]
        public void TestPerformAttack_EndsWithCas_Public()
        {
            string target = "smartsystems.cas";
            string expected = "Simulating CAS attack on smartsystems.cas";
            Assert.Equal(expected, App.PerformAttack(target));
        }

        [Fact]
        public void TestPerformAttack_CasLikeButNotCAS_Public()
        {
            string target = "CASE";
            string expected = "Target is not a CAS server: CASE";
            Assert.Equal(expected, App.PerformAttack(target));
        }

        [Fact]
        public void TestPerformAttack_EmptyString_Public()
        {
            string target = "";
            string expected = "Target is not a CAS server: ";
            Assert.Equal(expected, App.PerformAttack(target));
        }
    }
}