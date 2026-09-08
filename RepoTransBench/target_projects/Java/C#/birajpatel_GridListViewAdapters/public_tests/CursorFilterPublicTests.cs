using Xunit;
using Moq;

namespace GridListViewAdapters.PublicTests
{
    public class CursorFilterPublicTests
    {
        private Mock<ICursorFilterClient> clientMock;
        private Mock<ICursor> cursorMock;

        public CursorFilterPublicTests()
        {
            clientMock = new Mock<ICursorFilterClient>();
            cursorMock = new Mock<ICursor>();
        }

        [Fact]
        public void ConvertResultToStringPublic()
        {
            clientMock.Setup(c => c.ConvertToString(cursorMock.Object)).Returns("publicTest");
            var filter = new CursorFilter(clientMock.Object);
            Assert.Equal("publicTest", filter.ConvertResultToString(cursorMock.Object));
        }

        [Fact]
        public void PerformFilteringWithCursorPublic()
        {
            clientMock.Setup(c => c.RunQueryOnBackgroundThread("xyz")).Returns(cursorMock.Object);
            cursorMock.Setup(c => c.GetCount()).Returns(7);
            var filter = new CursorFilter(clientMock.Object);
            var results = filter.PerformFiltering("xyz");
            Assert.Equal(7, results.Count);
            Assert.Equal(cursorMock.Object, results.Values);
        }

        [Fact]
        public void PerformFilteringNullCursorPublic()
        {
            clientMock.Setup(c => c.RunQueryOnBackgroundThread("nullcase")).Returns((ICursor)null);
            var filter = new CursorFilter(clientMock.Object);
            var results = filter.PerformFiltering("nullcase");
            Assert.Equal(0, results.Count);
            Assert.Null(results.Values);
        }

        [Fact]
        public void PublishResultsWithNonNullCursorDifferentFromOldPublic()
        {
            var oldCursorMock = new Mock<ICursor>();
            var results = new FilterResults { Values = cursorMock.Object };

            clientMock.Setup(c => c.GetCursor()).Returns(oldCursorMock.Object);
            var filter = new CursorFilter(clientMock.Object);
            filter.PublishResults("z", results);
            clientMock.Verify(c => c.ChangeCursor(cursorMock.Object), Times.Once());
        }

        [Fact]
        public void PublishResultsWithNullValuesPublic()
        {
            var results = new FilterResults { Values = null };
            clientMock.Setup(c => c.GetCursor()).Returns(cursorMock.Object);
            var filter = new CursorFilter(clientMock.Object);
            filter.PublishResults("z", results);
            clientMock.Verify(c => c.ChangeCursor(It.IsAny<ICursor>()), Times.Never());
        }

        [Fact]
        public void PublishResultsWithSameCursorPublic()
        {
            var results = new FilterResults { Values = cursorMock.Object };
            clientMock.Setup(c => c.GetCursor()).Returns(cursorMock.Object);
            var filter = new CursorFilter(clientMock.Object);
            filter.PublishResults("z", results);
            clientMock.Verify(c => c.ChangeCursor(It.IsAny<ICursor>()), Times.Never());
        }
    }
}