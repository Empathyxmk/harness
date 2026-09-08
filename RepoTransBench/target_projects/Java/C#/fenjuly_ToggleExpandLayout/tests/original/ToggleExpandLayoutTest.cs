using Xunit;
using Moq;
using Fenjuly.ToggleExpandLayout;

namespace Fenjuly.ToggleExpandLayout.Tests.Original
{
    public class ToggleExpandLayoutTest
    {
        private ToggleExpandLayout layout;
        private Context context;

        public ToggleExpandLayoutTest()
        {
            context = new Context();
            layout = new ToggleExpandLayout(context);
        }

        [Fact]
        public void TestSetOnToggleTouchListener()
        {
            var listener = new Mock<ToggleExpandLayout.IOnToggleTouchListener>();
            layout.SetOnToggleTouchListener(listener.Object);
            Assert.NotNull(layout);
        }

        [Fact]
        public void TestOpen_andClose_NoChildren()
        {
            var listener = new Mock<ToggleExpandLayout.IOnToggleTouchListener>();
            layout.SetOnToggleTouchListener(listener.Object);
            layout.Open();
            layout.Close();
        }

        [Fact]
        public void TestOpen_andClose_WithChildren()
        {
            var context = new Context();
            var layoutMock = new Mock<ToggleExpandLayout>(context) { CallBase = true };
            var child0 = new Mock<View>() { CallBase = true };
            child0.Setup(c => c.GetMeasuredWidth()).Returns(20);
            child0.Setup(c => c.GetMeasuredHeight()).Returns(15);

            var child1 = new Mock<View>() { CallBase = true };
            child1.Setup(c => c.GetMeasuredWidth()).Returns(30);
            child1.Setup(c => c.GetMeasuredHeight()).Returns(10);

            layoutMock.Setup(l => l.GetChildCount()).Returns(2);
            layoutMock.Setup(l => l.GetChildAt(0)).Returns(child0.Object);
            layoutMock.Setup(l => l.GetChildAt(1)).Returns(child1.Object);

            var listener = new Mock<ToggleExpandLayout.IOnToggleTouchListener>();
            layoutMock.Object.SetOnToggleTouchListener(listener.Object);

            layoutMock.Object.OnLayout(true, 0, 0, 30, 25);
            layoutMock.Object.Open();
            layoutMock.Object.Close();

            listener.Verify(l => l.OnStartOpen(It.IsAny<int>(), It.IsAny<int>()), Times.AtLeastOnce());
            listener.Verify(l => l.OnStartClose(It.IsAny<int>(), It.IsAny<int>()), Times.AtLeastOnce());
        }

        [Fact]
        public void TestMultipleListeners()
        {
            var listener1 = new Mock<ToggleExpandLayout.IOnToggleTouchListener>();
            var listener2 = new Mock<ToggleExpandLayout.IOnToggleTouchListener>();
            layout.SetOnToggleTouchListener(listener1.Object);
            layout.SetOnToggleTouchListener(listener2.Object);

            layout.Open();
            layout.Close();

            listener1.Verify(l => l.OnStartOpen(It.IsAny<int>(), It.IsAny<int>()), Times.AtLeast(0));
            listener2.Verify(l => l.OnStartOpen(It.IsAny<int>(), It.IsAny<int>()), Times.AtLeast(0));
        }
    }
}