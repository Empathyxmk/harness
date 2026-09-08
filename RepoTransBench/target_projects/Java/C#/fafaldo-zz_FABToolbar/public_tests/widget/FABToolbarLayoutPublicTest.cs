using System;
using Moq;
using Xunit;
using FAFToolbar.Widget;

namespace PublicTests.Widget
{
    public class FABToolbarLayoutPublicTest
    {
        private Mock<IContext> mockContext;
        private Mock<IAttributeSet> mockAttrs;
        private Mock<ITypedArray> mockTypedArray;

        public FABToolbarLayoutPublicTest()
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

            mockTypedArray.Setup(t => t.GetInt(It.IsAny<int>(), It.IsAny<int>())).Returns(888);
            mockTypedArray.Setup(t => t.GetDimensionPixelSize(It.IsAny<int>(), It.IsAny<int>())).Returns(50);
            mockTypedArray.Setup(t => t.GetFloat(It.IsAny<int>(), It.IsAny<float>())).Returns(0.88f);
            mockTypedArray.Setup(t => t.GetResourceId(It.IsAny<int>(), It.IsAny<int>())).Returns(42);
            mockTypedArray.Setup(t => t.GetBoolean(It.IsAny<int>(), It.IsAny<bool>())).Returns(false);
        }

        [Fact]
        public void TestConstructorsWithOtherValues()
        {
            // Context constructor
            var layout1 = new FABToolbarLayout(mockContext.Object);
            Assert.NotNull(layout1);

            // Context + AttributeSet constructor
            var layout2 = new FABToolbarLayout(mockContext.Object, mockAttrs.Object);
            Assert.NotNull(layout2);

            // Context + AttributeSet + defStyleAttr constructor
            var layout3 = new FABToolbarLayout(mockContext.Object, mockAttrs.Object, 1);
            Assert.NotNull(layout3);
        }

        [Fact]
        public void TestParseAttrsPublic()
        {
            var layout = new FABToolbarLayout(mockContext.Object, mockAttrs.Object);
            mockContext.Verify(c => c.ObtainStyledAttributes(It.IsAny<IAttributeSet>(), It.IsAny<int[]>()), Times.AtLeastOnce());
            mockTypedArray.Verify(t => t.Recycle(), Times.AtLeastOnce());
        }
    }

    // Mocks/stubs for public test context
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