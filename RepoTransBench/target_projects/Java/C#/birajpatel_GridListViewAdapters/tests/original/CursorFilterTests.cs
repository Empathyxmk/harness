using System;
using Xunit;
using Moq;

namespace GridListViewAdapters.Tests
{
    public class CursorFilterTests
    {
        private Mock<ICursorFilterClient> clientMock;
        private Mock<ICursor> cursorMock;

        public CursorFilterTests()
        {
            clientMock = new Mock<ICursorFilterClient>();
            cursorMock = new Mock<ICursor>();
        }

        [Fact]
        public void ConvertResultToString_ReturnsString()
        {
            clientMock.Setup(c => c.ConvertToString(cursorMock.Object)).Returns("test");
            var filter = new CursorFilter(clientMock.Object);
            Assert.Equal("test", filter.ConvertResultToString(cursorMock.Object));
        }

        [Fact]
        public void PerformFiltering_WithCursor_ReturnsExpectedResults()
        {
            clientMock.Setup(c => c.RunQueryOnBackgroundThread("abc")).Returns(cursorMock.Object);
            cursorMock.Setup(c => c.GetCount()).Returns(5);
            var filter = new CursorFilter(clientMock.Object);
            var results = filter.PerformFiltering("abc");
            Assert.Equal(5, results.Count);
            Assert.Equal(cursorMock.Object, results.Values);
        }

        [Fact]
        public void PerformFiltering_NullCursor_ReturnsZeroResults()
        {
            clientMock.Setup(c => c.RunQueryOnBackgroundThread("none")).Returns((ICursor)null);
            var filter = new CursorFilter(clientMock.Object);
            var results = filter.PerformFiltering("none");
            Assert.Equal(0, results.Count);
            Assert.Null(results.Values);
        }

        [Fact]
        public void PublishResults_WithNonNullCursorDifferentFromOld_CallsChangeCursor()
        {
            var oldCursorMock = new Mock<ICursor>();
            var results = new FilterResults { Values = cursorMock.Object };

            clientMock.Setup(c => c.GetCursor()).Returns(oldCursorMock.Object);
            var filter = new CursorFilter(clientMock.Object);
            filter.PublishResults("c", results);
            clientMock.Verify(c => c.ChangeCursor(cursorMock.Object), Times.Once());
        }

        [Fact]
        public void PublishResults_WithNullValues_DoesNotCallChangeCursor()
        {
            var results = new FilterResults { Values = null };
            clientMock.Setup(c => c.GetCursor()).Returns(cursorMock.Object);
            var filter = new CursorFilter(clientMock.Object);
            filter.PublishResults("c", results);
            clientMock.Verify(c => c.ChangeCursor(It.IsAny<ICursor>()), Times.Never());
        }

        [Fact]
        public void PublishResults_WithSameCursor_DoesNotCallChangeCursor()
        {
            var results = new FilterResults { Values = cursorMock.Object };
            clientMock.Setup(c => c.GetCursor()).Returns(cursorMock.Object);
            var filter = new CursorFilter(clientMock.Object);
            filter.PublishResults("c", results);
            clientMock.Verify(c => c.ChangeCursor(It.IsAny<ICursor>()), Times.Never());
        }
    }
}