using Xunit;

namespace MarkushiAndroidUi.Tests.Original
{
    public class LineSegmentTests
    {
        [Fact]
        public void TestConstructorAndGetStartIdx()
        {
            var seg = new LineSegment(1, 2, 3);
            Assert.Equal(new[] { 1, 2, 3 }, seg.Indexes);
            Assert.Equal(1, seg.GetStartIdx());
        }

        [Fact]
        public void TestParcelableWriteAndRead()
        {
            var seg = new LineSegment(4, 5, 6);

            var stream = new System.IO.MemoryStream();
            seg.WriteToStream(stream);
            stream.Position = 0;

            var created = LineSegment.Creator.CreateFromStream(stream);
            Assert.Equal(new[] { 4, 5, 6 }, created.Indexes);

            var array = LineSegment.Creator.NewArray(2);
            Assert.Equal(2, array.Length);

            stream.Dispose();
        }

        [Fact]
        public void TestDescribeContents()
        {
            var seg = new LineSegment(1, 2);
            Assert.Equal(0, seg.DescribeContents());
        }
    }
}