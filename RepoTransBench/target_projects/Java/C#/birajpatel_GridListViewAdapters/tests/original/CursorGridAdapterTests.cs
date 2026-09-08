using System;
using System.Collections.Generic;
using Xunit;
using Moq;

namespace GridListViewAdapters.Tests
{
    public class CursorGridAdapterTests
    {
        private class ConcreteCursorGridAdapter : CursorGridAdapter<object>
        {
            public ConcreteCursorGridAdapter(IContext context, int totalCardsInRow, ICursor c)
                : base(context, totalCardsInRow, c) { }
            public override IView GetView(int position, IView convertView, IViewGroup parent) => null;
            public override Card<object> GetNewCard(int cardPositionInRow) => null;
        }

        private Mock<IContext> contextMock;
        private Mock<ICursor> cursorMock;
        private ConcreteCursorGridAdapter adapter;

        public CursorGridAdapterTests()
        {
            contextMock = new Mock<IContext>(MockBehavior.Default);
            cursorMock = new Mock<ICursor>(MockBehavior.Default);

            contextMock.Setup(c => c.GetSystemService(It.IsAny<string>())).Returns((object)null);
            var displayMetrics = new DisplayMetrics { WidthPixels = 240, HeightPixels = 320 };
            contextMock.Setup(c => c.Resources.DisplayMetrics).Returns(displayMetrics);
            cursorMock.Setup(c => c.GetCount()).Returns(5);

            adapter = new ConcreteCursorGridAdapter(contextMock.Object, 2, cursorMock.Object);
        }

        [Fact]
        public void ReturnsSameCursorFromGetCursor()
        {
            Assert.Same(cursorMock.Object, adapter.GetCursor());
        }

        [Fact]
        public void ChangeCursor_ClosesOld()
        {
            var old = new Mock<ICursor>();
            adapter.MCursor = old.Object;
            var newCursor = new Mock<ICursor>();
            newCursor.Setup(c => c.GetCount()).Returns(3);
            adapter.ChangeCursor(newCursor.Object);
            old.Verify(c => c.Close(), Times.Once);
            Assert.Same(newCursor.Object, adapter.GetCursor());
        }

        [Fact]
        public void SwapCursor_ReturnsNullWhenSame()
        {
            adapter.MCursor = cursorMock.Object;
            Assert.Null(adapter.SwapCursor(cursorMock.Object));
        }

        [Fact]
        public void SwapCursor_ReturnsOldAndUpdates()
        {
            var old = new Mock<ICursor>();
            var newC = new Mock<ICursor>();
            newC.Setup(c => c.GetCount()).Returns(4);

            adapter.MCursor = old.Object;
            var result = adapter.SwapCursor(newC.Object);
            Assert.Same(old.Object, result);
            Assert.Same(newC.Object, adapter.GetCursor());
        }

        [Fact]
        public void SwapCursorToNull_ReturnsOldAndSetsNull()
        {
            adapter.MCursor = cursorMock.Object;
            var returned = adapter.SwapCursor(null);
            Assert.Same(cursorMock.Object, returned);
            Assert.Null(adapter.GetCursor());
        }

        [Fact]
        public void ConvertToString_HandlesNull()
        {
            Assert.Equal(string.Empty, adapter.ConvertToString(null));
        }

        [Fact]
        public void ConvertToString_HandlesNonNull()
        {
            var c = new Mock<ICursor>();
            c.Setup(x => x.ToString()).Returns("CURSORSTR");
            Assert.Equal("CURSORSTR", adapter.ConvertToString(c.Object));
        }

        [Fact]
        public void RunQueryOnBackgroundThread_WithProvider()
        {
            var cursor = new Mock<ICursor>();
            var provider = new Mock<IFilterQueryProvider>();
            provider.Setup(p => p.RunQuery("kkk")).Returns(cursor.Object);
            adapter.MFilterQueryProvider = provider.Object;
            Assert.Same(cursor.Object, adapter.RunQueryOnBackgroundThread("kkk"));
        }

        [Fact]
        public void RunQueryOnBackgroundThread_NoProvider_ReturnsCursor()
        {
            adapter.MCursor = cursorMock.Object;
            adapter.MFilterQueryProvider = null;
            Assert.Same(cursorMock.Object, adapter.RunQueryOnBackgroundThread("z"));
        }
    }
}