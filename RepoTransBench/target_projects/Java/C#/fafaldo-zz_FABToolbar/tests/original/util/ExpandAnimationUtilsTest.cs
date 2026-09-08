using System.Collections.Generic;
using Moq;
using Xunit;
using FAFToolbar.Util;

namespace Tests.Original.Util
{
    public class ExpandAnimationUtilsTest
    {
        private Mock<IViewGroup> mockViewGroup;
        private Mock<IView> mockChild1;
        private Mock<IView> mockChild2;

        public ExpandAnimationUtilsTest()
        {
            SetUp();
        }

        public void SetUp()
        {
            mockViewGroup = new Mock<IViewGroup>();
            mockChild1 = new Mock<IView>();
            mockChild2 = new Mock<IView>();

            mockViewGroup.Setup(vg => vg.GetChildCount()).Returns(2);
            mockViewGroup.Setup(vg => vg.GetChildAt(0)).Returns(mockChild1.Object);
            mockViewGroup.Setup(vg => vg.GetChildAt(1)).Returns(mockChild2.Object);

            mockChild1.SetupGet(v => v.Left).Returns(10);
            mockChild1.SetupGet(v => v.Top).Returns(20);
            mockChild1.SetupGet(v => v.Width).Returns(30);
            mockChild1.SetupGet(v => v.Height).Returns(40);

            mockChild2.SetupGet(v => v.Left).Returns(100);
            mockChild2.SetupGet(v => v.Top).Returns(200);
            mockChild2.SetupGet(v => v.Width).Returns(50);
            mockChild2.SetupGet(v => v.Height).Returns(60);
        }

        [Fact]
        public void TestBuild()
        {
            int pivotX = 50;
            int pivotY = 60;
            float fraction = 0.5f;
            int duration = 300;
            int delay = 50;

            var animators = ExpandAnimationUtils.Build(mockViewGroup.Object, pivotX, pivotY, fraction, duration, delay);
            Assert.Equal(5, animators.Count);
            for (int i = 0; i < 4; i++)
            {
                Assert.NotNull(animators[i]);
            }
            Assert.NotNull(animators[4]);
        }

        [Fact]
        public void TestBuildReversed()
        {
            int pivotX = 30;
            int pivotY = 90;
            float fraction = 0.3f;
            int duration = 400;
            int delay = 20;

            var animators = ExpandAnimationUtils.BuildReversed(mockViewGroup.Object, pivotX, pivotY, fraction, duration, delay);
            Assert.Equal(5, animators.Count);
            for (int i = 0; i < 5; i++)
            {
                Assert.NotNull(animators[i]);
            }
        }
    }

    // Minimal interfaces to simulate Android's View/ViewGroup API
    public interface IViewGroup
    {
        int GetChildCount();
        IView GetChildAt(int index);
    }

    public interface IView
    {
        int Left { get; }
        int Top { get; }
        int Width { get; }
        int Height { get; }
    }
}