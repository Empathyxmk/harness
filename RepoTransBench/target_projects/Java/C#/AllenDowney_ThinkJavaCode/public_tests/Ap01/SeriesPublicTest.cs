using Xunit;
using AllenDowney.ThinkJavaCode;

namespace PublicTests.Ap01
{
    public class SeriesPublicTest
    {
        [Fact]
        public void TestGeometricSeriesDifferentData()
        {
            int result = Series.GeometricSeriesSum(3, 2, 4);
            Assert.Equal(45, result);

            Assert.Equal(111, Series.GeometricSeriesSum(1, 10, 3));
        }

        [Fact]
        public void TestArithmeticSeriesDifferentData()
        {
            int result = Series.ArithmeticSeriesSum(2, 5, 4);
            Assert.Equal(38, result);

            Assert.Equal(15, Series.ArithmeticSeriesSum(3, 0, 5));
        }
    }
}