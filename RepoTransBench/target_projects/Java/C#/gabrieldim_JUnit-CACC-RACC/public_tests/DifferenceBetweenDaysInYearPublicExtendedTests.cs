using System;
using Xunit;
using gabrieldim_JUnitCACC;

namespace PublicTests
{
    public class DifferenceBetweenDaysInYearPublicExtendedTests
    {
        [Fact]
        public void PublicTestSameDay()
        {
            Assert.Equal(0, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 5, 20, 2022, 5, 20));
        }

        [Fact]
        public void PublicTestNonLeapYearNormalDates()
        {
            Assert.Equal(257, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 3, 15, 2022, 11, 27));
            Assert.Equal(-257, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 11, 27, 2022, 3, 15));
        }

        [Fact]
        public void PublicTestLeapYearFebDates()
        {
            Assert.Equal(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2016, 2, 27, 2016, 2, 28));
            Assert.Equal(-2, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2016, 3, 1, 2016, 2, 28));
        }

        [Fact]
        public void PublicTestInvalidMonth()
        {
            var e1 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 0, 4, 2022, 6, 9)
            );
            Assert.Contains("Invalid", e1.Message);

            var e2 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 3, 14, 2022, 15, 7)
            );
            Assert.Contains("Invalid", e2.Message);
        }

        [Fact]
        public void PublicTestInvalidDay()
        {
            var e1 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 2, 30, 2023, 2, 1)
            );
            Assert.Contains("Invalid", e1.Message);

            var e2 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(1999, 6, 31, 1999, 3, 1)
            );
            Assert.Contains("Invalid", e2.Message);
        }

        [Fact]
        public void PublicTestDifferentYears()
        {
            var e = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2021, 4, 10, 2020, 5, 10)
            );
            Assert.Contains("Years must be the same", e.Message);
        }

        [Fact]
        public void PublicTestLeapYearRecognition()
        {
            // 2012 is a leap year, so Jan 1 -> Mar 1 is 60 days
            Assert.Equal(60, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2012, 1, 1, 2012, 3, 1)); // 2012 leap
            Assert.Equal(59, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2104, 1, 1, 2104, 3, 1)); // not leap
            Assert.Equal(59, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(1800, 1, 1, 1800, 3, 1)); // not leap
            Assert.Equal(60, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2400, 1, 1, 2400, 3, 1)); // leap
        }

        [Fact]
        public void PublicTestFirstAndLastDaysOfMonth()
        {
            Assert.Equal(27, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 4, 1, 2022, 4, 28));
            Assert.Equal(-27, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 4, 28, 2022, 4, 1));
        }

        [Fact]
        public void PublicTestMinimumValidDayAndMonth()
        {
            Assert.Equal(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 2, 1, 2023, 2, 2));
            Assert.Equal(-1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 2, 2, 2023, 2, 1));
        }

        [Fact]
        public void PublicTestMaximumValidDayAndMonth()
        {
            Assert.Equal(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 11, 29, 2023, 11, 30));
        }

        [Fact]
        public void PublicTestIsValidDatePrivateMethodViaInvalidInput()
        {
            var e1 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 2, 29, 2023, 2, 28)
            );
            Assert.Contains("Invalid", e1.Message);

            var e2 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 2, 30, 2024, 2, 28)
            );
            Assert.Contains("Invalid", e2.Message);
        }
    }
}