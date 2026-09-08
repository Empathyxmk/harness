using System;
using Xunit;
using gabrieldim_JUnitCACC;

namespace Tests.Original
{
    public class DifferenceBetweenDaysInYearTests
    {
        [Fact]
        public void Test1_Predicate1()
        {
            int output = DifferenceBetweenDaysInYear.Cal(7, 1, 6, 1, 2021);
            Assert.Equal(31, output);
        }

        [Fact]
        public void Test2_Predicate1()
        {
            int output = DifferenceBetweenDaysInYear.Cal(1, 3, 4, 15, 2019);
            Assert.Equal(102, output);
        }

        [Fact]
        public void Test3_Predicate2()
        {
            int output = DifferenceBetweenDaysInYear.Cal(2, 5, 4, 27, 2000);
            Assert.Equal(82, output);
        }

        [Fact]
        public void Test4_Predicate2()
        {
            int output = DifferenceBetweenDaysInYear.Cal(5, 6, 4, 28, 65);
            Assert.Equal(53, output);
        }

        [Fact]
        public void Test5_Predicate2()
        {
            int output = DifferenceBetweenDaysInYear.Cal(9, 9, 4, 11, 1200);
            Assert.Equal(32, output);
        }
    }
}