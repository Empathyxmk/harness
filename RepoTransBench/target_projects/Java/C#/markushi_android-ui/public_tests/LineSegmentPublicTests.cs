using Xunit;

namespace MarkushiAndroidUi.PublicTests
{
    public class LineSegmentPublicTests
    {
        [Fact]
        public void TestConstructorAndGetStartIdxPublic()
        {
            var seg = new LineSegment(10, 20, 30);
            Assert.Equal(new[] { 10, 20, 30 }, seg.Indexes);
            Assert.Equal(10, seg.GetStartIdx());
        }

        [Fact]
        public void TestParcelableWriteAndReadPublic()
        {
            var seg = new LineSegment(7, 8, 9);

            var stream = new System.IO.MemoryStream();
            seg.WriteToStream(stream);
            stream.Position = 0;

            var created = LineSegment.Creator.CreateFromStream(stream);
            Assert.Equal(new[] { 7, 8, 9 }, created.Indexes);

            var array = LineSegment.Creator.NewArray(3);
            Assert.Equal(3, array.Length);

            stream.Dispose();
        }

        [Fact]
        public void TestDescribeContentsPublic()
        {
            var seg = new LineSegment(4, 8);
            Assert.Equal(0, seg.DescribeContents());
        }
    }
}