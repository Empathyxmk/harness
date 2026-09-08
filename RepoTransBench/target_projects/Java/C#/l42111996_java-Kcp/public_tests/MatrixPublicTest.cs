using Xunit;

namespace KcpPublicTests
{
    public class MatrixPublicTest
    {
        [Fact]
        public void TestMatrixMultiplicationDifferentValues()
        {
            byte[,] a = new byte[,] { { 11, 22 }, { 33, 44 } };
            byte[,] b = new byte[,] { { 2, 1 }, { 0, 3 } };
            byte[,] expected = new byte[2, 2];
            expected[0, 0] = (byte)(11 * 2 + 22 * 0);    // 22
            expected[0, 1] = (byte)(11 * 1 + 22 * 3);    // 77
            expected[1, 0] = (byte)(33 * 2 + 44 * 0);    // 66
            expected[1, 1] = (byte)(33 * 1 + 44 * 3);    // 165

            var actual = Multiply(a, b);
            Assert.Equal(expected[0, 0], actual[0, 0]);
            Assert.Equal(expected[0, 1], actual[0, 1]);
            Assert.Equal(expected[1, 0], actual[1, 0]);
            Assert.Equal(expected[1, 1], actual[1, 1]);
        }

        private byte[,] Multiply(byte[,] a, byte[,] b)
        {
            int n = a.GetLength(0);
            int m = b.GetLength(1);
            int p = b.GetLength(0);
            byte[,] c = new byte[n, m];
            for (int i = 0; i < n; ++i)
                for (int j = 0; j < m; ++j)
                    for (int k = 0; k < p; ++k)
                        c[i, j] += (byte)(a[i, k] * b[k, j]);
            return c;
        }
    }
}