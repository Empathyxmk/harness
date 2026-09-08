using Xunit;
using Moq;
using Fenjuly.ToggleExpandLayout;

namespace Fenjuly.ToggleExpandLayout.Tests.Public
{
    public class DropDownLayoutPublicTest
    {
        private DropDownLayout layout;
        private Context context;

        public DropDownLayoutPublicTest()
        {
            context = new Context();
            layout = new Mock<DropDownLayout>(context) { CallBase = true }.Object;
        }

        [Fact]
        public void TestOnLayoutWithDifferentSimpleChild()
        {
            // Simulate 2 children, both not ToggleExpandLayout
            var layoutMock = new Mock<DropDownLayout>(context) { CallBase = true };
            var child1 = new Mock<View>() { CallBase = true };
            var child2 = new Mock<View>() { CallBase = true };

            layoutMock.Setup(l => l.GetChildCount()).Returns(2);
            layoutMock.Setup(l => l.GetChildAt(0)).Returns(child1.Object);
            layoutMock.Setup(l => l.GetChildAt(1)).Returns(child2.Object);
            child1.Setup(c => c.GetMeasuredWidth()).Returns(13);
            child1.Setup(c => c.GetMeasuredHeight()).Returns(8);
            child2.Setup(c => c.GetMeasuredWidth()).Returns(17);
            child2.Setup(c => c.GetMeasuredHeight()).Returns(4);

            layoutMock.Object.OnLayout(true, 2, 3, 7, 12);
        }

        [Fact]
        public void TestOnLayoutWithDifferentToggleExpandLayoutChild()
        {
            var layoutMock = new Mock<DropDownLayout>(context) { CallBase = true };
            var toggleChild = new Mock<ToggleExpandLayout>(new Context()) { CallBase = true };
            var grandChild1 = new Mock<View>() { CallBase = true };
            var grandChild2 = new Mock<View>() { CallBase = true };
            var child2 = new Mock<View>() { CallBase = true };

            layoutMock.Setup(l => l.GetChildCount()).Returns(2);
            layoutMock.Setup(l => l.GetChildAt(0)).Returns(toggleChild.Object);
            layoutMock.Setup(l => l.GetChildAt(1)).Returns(child2.Object);

            toggleChild.Setup(tc => tc.GetMeasuredWidth()).Returns(30);
            toggleChild.Setup(tc => tc.GetMeasuredHeight()).Returns(6);
            toggleChild.Setup(tc => tc.GetChildCount()).Returns(2);
            toggleChild.Setup(tc => tc.GetChildAt(0)).Returns(grandChild1.Object);
            toggleChild.Setup(tc => tc.GetChildAt(1)).Returns(grandChild2.Object);
            grandChild1.Setup(gc => gc.GetMeasuredWidth()).Returns(20);
            grandChild1.Setup(gc => gc.GetMeasuredHeight()).Returns(5);
            grandChild2.Setup(gc => gc.GetMeasuredWidth()).Returns(9);
            grandChild2.Setup(gc => gc.GetMeasuredHeight()).Returns(2);

            child2.Setup(c => c.GetMeasuredWidth()).Returns(14);
            child2.Setup(c => c.GetMeasuredHeight()).Returns(7);

            layoutMock.Object.OnLayout(false, 4, 5, 6, 10);
        }
    }
}