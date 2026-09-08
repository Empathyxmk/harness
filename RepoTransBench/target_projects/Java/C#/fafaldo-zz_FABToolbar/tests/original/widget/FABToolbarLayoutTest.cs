using System;
using Moq;
using Xunit;
using FAFToolbar.Widget;

namespace Tests.Original.Widget
{
    public class FABToolbarLayoutTest
    {
        private Mock<IContext> mockContext;
        private Mock<IAttributeSet> mockAttrs;
        private Mock<ITypedArray> mockTypedArray;

        public FABToolbarLayoutTest()
        {
            SetUp();
        }

        public void SetUp()
        {
            mockContext = new Mock<IContext>();
            mockAttrs = new Mock<IAttributeSet>();
            mockTypedArray = new Mock<ITypedArray>();

            mockContext.Setup(c => c.ObtainStyledAttributes(It.IsAny<IAttributeSet>(), It.IsAny<int[]>()))
                .Returns(mockTypedArray.Object);

            mockTypedArray.Setup(t => t.GetInt(It.IsAny<int>(), It.IsAny<int>())).Returns(500);
            mockTypedArray.Setup(t => t.GetDimensionPixelSize(It.IsAny<int>(), It.IsAny<int>())).Returns(20);
            mockTypedArray.Setup(t => t.GetFloat(It.IsAny<int>(), It.IsAny<float>())).Returns(0.42f);
            mockTypedArray.Setup(t => t.GetResourceId(It.IsAny<int>(), It.IsAny<int>())).Returns(-1);
            mockTypedArray.Setup(t => t.GetBoolean(It.IsAny<int>(), It.IsAny<bool>())).Returns(true);
        }

        [Fact]
        public void TestConstructorsAndParseAttrs()
        {
            // Context only
            var layout1 = new FABToolbarLayout(mockContext.Object);
            Assert.NotNull(layout1);

            // Context + AttributeSet
            var layout2 = new FABToolbarLayout(mockContext.Object, mockAttrs.Object);
            Assert.NotNull(layout2);

            // Context + AttributeSet + defStyleAttr
            var layout3 = new FABToolbarLayout(mockContext.Object, mockAttrs.Object, 0);
            Assert.NotNull(layout3);
        }

        [Fact]
        public void TestParseAttrsFallbacks()
        {
            var layout = new FABToolbarLayout(mockContext.Object, mockAttrs.Object);
            mockContext.Verify(c => c.ObtainStyledAttributes(It.IsAny<IAttributeSet>(), It.IsAny<int[]>()), Times.AtLeastOnce());
            mockTypedArray.Verify(t => t.Recycle(), Times.AtLeastOnce());
        }
    }

    // Mocks/stubs for the interfaces
    // Mimic minimal Android API required for the test logic

    public interface IContext
    {
        ITypedArray ObtainStyledAttributes(IAttributeSet attrs, int[] attrs2);
    }

    public interface IAttributeSet { }

    public interface ITypedArray
    {
        int GetInt(int index, int defValue);
        int GetDimensionPixelSize(int index, int defValue);
        float GetFloat(int index, float defValue);
        int GetResourceId(int index, int defValue);
        bool GetBoolean(int index, bool defValue);
        void Recycle();
    }
}