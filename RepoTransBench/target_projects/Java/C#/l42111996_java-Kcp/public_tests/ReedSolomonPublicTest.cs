using Xunit;

namespace KcpPublicTests
{
    public class ReedSolomonPublicTest
    {
        [Fact]
        public void TestEncodeDecodeWithOtherData()
        {
            var rs = ReedSolomon.Create(4, 3);
            byte[][] shards = new byte[7][];
            for (int i = 0; i < 7; i++)
                shards[i] = new byte[10];

            for (int i = 0; i < 4; i++)
                for (int j = 0; j < 10; j++)
                    shards[i][j] = (byte)((i + 1) * (j + 3));

            rs.EncodeParity(shards, 0, 10);

            // Simulate missing shards
            shards[1] = new byte[10];
            shards[5] = new byte[10];
            shards[6] = new byte[10];
            bool[] shardPresent = new bool[] { true, false, true, true, true, false, false };

            rs.DecodeMissing(shards, shardPresent, 0, 10);

            for (int i = 0; i < 4; i++)
                for (int j = 0; j < 10; j++)
                    Assert.Equal((byte)((i + 1) * (j + 3)), shards[i][j]);
        }
    }

    // Minimal stub for compilation. Full class should provide actual implementation.
    public class ReedSolomon
    {
        private int dataShards, parityShards;
        public static ReedSolomon Create(int dataShards, int parityShards) => new ReedSolomon(dataShards, parityShards);
        private ReedSolomon(int dataShards, int parityShards)
        {
            this.dataShards = dataShards;
            this.parityShards = parityShards;
        }
        public void EncodeParity(byte[][] shards, int offset, int byteCount) { /* Simulate parity */ }
        public void DecodeMissing(byte[][] shards, bool[] shardPresent, int offset, int byteCount) { /* Simulate decoding */ }
    }
}