using Xunit;
using Moq;
using Fenjuly.ToggleExpandLayout;

namespace Fenjuly.ToggleExpandLayout.Tests.Original
{
    public class DropDownLayoutTest
    {
        private DropDownLayout layout;
        private Context context;

        public DropDownLayoutTest()
        {
            context = new Context();
            layout = Moq.Mock.Of<DropDownLayout>(MockBehavior.Default, c => c.GetChildCount() == 0);
        }

        [Fact]
        public void TestOnLayoutWithSimpleChild()
        {
            // Simulate 1 child not ToggleExpandLayout
            var layoutMock = new Mock<DropDownLayout>(context) { CallBase = true };
            var child = new Mock<View>() { CallBase = true };
            layoutMock.Setup(l => l.GetChildCount()).Returns(1);
            layoutMock.Setup(l => l.GetChildAt(0)).Returns(child.Object);
            child.Setup(c => c.GetMeasuredWidth()).Returns(10);
            child.Setup(c => c.GetMeasuredHeight()).Returns(5);

            layoutMock.Object.OnLayout(true, 0, 0, 10, 10);
        }

        [Fact]
        public void TestOnLayoutWithToggleExpandLayoutChild()
        {
            var layoutMock = new Mock<DropDownLayout>(context) { CallBase = true };
            var toggleChild = new Mock<ToggleExpandLayout>(new Context()) { CallBase = true };
            var grandChild = new Mock<View>() { CallBase = true };

            layoutMock.Setup(l => l.GetChildCount()).Returns(1);
            layoutMock.Setup(l => l.GetChildAt(0)).Returns(toggleChild.Object);
            toggleChild.Setup(tc => tc.GetMeasuredWidth()).Returns(22);
            toggleChild.Setup(tc => tc.GetMeasuredHeight()).Returns(7);
            toggleChild.Setup(tc => tc.GetChildCount()).Returns(1);
            toggleChild.Setup(tc => tc.GetChildAt(0)).Returns(grandChild.Object);
            grandChild.Setup(gc => gc.GetMeasuredWidth()).Returns(15);
            grandChild.Setup(gc => gc.GetMeasuredHeight()).Returns(3);

            layoutMock.Object.OnLayout(false, 1, 2, 3, 4);
        }
    }
}