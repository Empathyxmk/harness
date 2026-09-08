using System;
using Xunit;
using gabrieldim_JUnitCACC;

namespace PublicTests
{
    public class DifferenceBetweenDaysInYearPublicTests
    {
        [Fact]
        public void PublicTest1_Predicate1()
        {
            int output = DifferenceBetweenDaysInYear.Cal(5, 2, 4, 2, 2024);
            Assert.Equal(28, output);
        }

        [Fact]
        public void PublicTest2_Predicate1()
        {
            int output = DifferenceBetweenDaysInYear.Cal(12, 11, 5, 23, 2018);
            Assert.Equal(171, output);
        }

        [Fact]
        public void PublicTest3_Predicate2()
        {
            int output = DifferenceBetweenDaysInYear.Cal(10, 1, 12, 22, 1998);
            Assert.Equal(21, output);
        }

        [Fact]
        public void PublicTest4_Predicate2()
        {
            int output = DifferenceBetweenDaysInYear.Cal(3, 7, 9, 15, 105);
            Assert.Equal(8, output);
        }

        [Fact]
        public void PublicTest5_Predicate2()
        {
            int output = DifferenceBetweenDaysInYear.Cal(11, 5, 12, 1, 1300);
            Assert.Equal(170, output);
        }
    }
}