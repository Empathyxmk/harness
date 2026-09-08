using System;
using Xunit;
using gabrieldim_JUnitCACC;

namespace Tests.Original
{
    public class DifferenceBetweenDaysInYearExtendedTests
    {
        [Fact]
        public void TestSameDay()
        {
            Assert.Equal(0, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 1, 1, 2023, 1, 1));
        }

        [Fact]
        public void TestNonLeapYearNormalDates()
        {
            Assert.Equal(364, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 1, 1, 2023, 12, 31));
            Assert.Equal(-364, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 12, 31, 2023, 1, 1));
        }

        [Fact]
        public void TestLeapYearFebDates()
        {
            Assert.Equal(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2020, 2, 28, 2020, 2, 29));
            Assert.Equal(-1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2020, 3, 1, 2020, 2, 29));
        }

        [Fact]
        public void TestInvalidMonth()
        {
            var e1 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 0, 10, 2023, 1, 1)
            );
            Assert.Contains("Invalid", e1.Message);

            var e2 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2023, 1, 1, 2023, 13, 1)
            );
            Assert.Contains("Invalid", e2.Message);
        }

        [Fact]
        public void TestInvalidDay()
        {
            var e1 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2021, 2, 30, 2021, 2, 1)
            );
            Assert.Contains("Invalid", e1.Message);

            var e2 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 4, 31, 2022, 2, 1)
            );
            Assert.Contains("Invalid", e2.Message);
        }

        [Fact]
        public void TestDifferentYears()
        {
            var e = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2022, 1, 1, 2021, 1, 1)
            );
            Assert.Contains("Years must be the same", e.Message);
        }

        [Fact]
        public void TestLeapYearRecognition()
        {
            Assert.Equal(60, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2000, 1, 1, 2000, 3, 1)); // 2000 leap
            Assert.Equal(60, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2016, 1, 1, 2016, 3, 1)); // leap
            Assert.Equal(59, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2100, 1, 1, 2100, 3, 1)); // 2100 not leap
            Assert.Equal(59, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(1900, 1, 1, 1900, 3, 1)); // 1900 not leap
        }

        [Fact]
        public void TestFirstAndLastDaysOfMonth()
        {
            Assert.Equal(30, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 1, 1, 2024, 1, 31));
            Assert.Equal(-30, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 1, 31, 2024, 1, 1));
        }

        [Fact]
        public void TestMinimumValidDayAndMonth()
        {
            Assert.Equal(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 1, 1, 2024, 1, 2));
            Assert.Equal(-1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 1, 2, 2024, 1, 1));
        }

        [Fact]
        public void TestMaximumValidDayAndMonth()
        {
            Assert.Equal(1, DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2024, 12, 30, 2024, 12, 31));
        }

        [Fact]
        public void TestIsValidDatePrivateMethodViaInvalidInput()
        {
            var e1 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2021, 2, 29, 2021, 2, 28)
            );
            Assert.Contains("Invalid", e1.Message);

            var e2 = Assert.Throws<ArgumentException>(() =>
                DifferenceBetweenDaysInYear.differenceBetweenDaysInYear(2020, 2, 30, 2020, 2, 28)
            );
            Assert.Contains("Invalid", e2.Message);
        }
    }
}