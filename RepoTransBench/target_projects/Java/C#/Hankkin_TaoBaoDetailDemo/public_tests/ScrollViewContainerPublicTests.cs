using Xunit;
using Hankkin.Library;

namespace Hankkin.TaoBaoDetailDemo.Public.Tests
{
    public class ScrollViewContainerPublicTests
    {
        private class MyMockContext { }

        [Fact]
        public void Test_Constructor()
        {
            var ctx = new MyMockContext();
            var svc1 = new ScrollViewContainer(ctx);
            Assert.NotNull(svc1);

            var svc2 = new ScrollViewContainer(ctx, null);
            Assert.NotNull(svc2);
        }

        [Fact]
        public void Test_TouchEventDispatchReturnsTrueOnACTION_UP()
        {
            var ctx = new MyMockContext();
            var svc = new ScrollViewContainer(ctx);
            var upEvent = new MockMotionEvent(MockMotionEvent.ActionType.Up, 12.0f, 24.0f);
            bool result = svc.DispatchTouchEvent(upEvent);
            Assert.True(result);
        }
    }
}