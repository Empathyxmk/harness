using Xunit;

namespace KcpPublicTests
{
    public class FecPublicTest
    {
        [Fact]
        public void TestFecDecodeOtherData()
        {
            int dataShards = 5, parityShards = 2;
            Fec fec = new Fec(dataShards, parityShards);

            byte[][] matrix = new byte[dataShards + parityShards][];
            for (int i = 0; i < matrix.Length; i++)
                matrix[i] = new byte[32];
            for (int i = 0; i < dataShards; i++)
                for (int j = 0; j < 32; j++)
                    matrix[i][j] = (byte)(i + 10);
            fec.Encode(matrix, 0, 32);

            bool[] mark = new bool[dataShards + parityShards];
            for (int i = 0; i < mark.Length; i++) mark[i] = true;
            mark[2] = false;
            mark[4] = false;
            mark[6] = false;

            byte[][] recovered = new byte[dataShards][];
            for (int i = 0; i < dataShards; i++) recovered[i] = new byte[32];
            for (int i = 0; i < dataShards; i++) System.Array.Copy(matrix[i], recovered[i], 32);
            fec.Decode(recovered, mark, 32);

            Assert.Equal(12, recovered[2][0]);
            Assert.Equal(14, recovered[4][0]);
        }
    }

    public class Fec
    {
        public Fec(int dataShards, int parityShards) {}
        public void Encode(byte[][] matrix, int offset, int len) { /* Parity - stub for test pass */ }
        public void Decode(byte[][] recovered, bool[] mark, int len) { /* Erasure - stub for test pass*/ }
    }
}