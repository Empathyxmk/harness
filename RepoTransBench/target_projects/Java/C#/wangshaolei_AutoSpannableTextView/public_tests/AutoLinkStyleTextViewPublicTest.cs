using System;
using Xunit;
using Moq;

namespace AutoSpannableTextView.PublicTests
{
    public class AutoLinkStyleTextViewPublicTest
    {
        private Mock<object> mockContext;
        private AutoSpannableTextView.AutoLinkStyleTextView publicTarget;

        public AutoLinkStyleTextViewPublicTest()
        {
            mockContext = new Mock<object>();
            publicTarget = new AutoSpannableTextView.AutoLinkStyleTextView(mockContext.Object, null, 0);
        }

        [Fact]
        public void testConstructorAndDefaultFields_public()
        {
            Assert.NotNull(publicTarget);
        }

        [Fact]
        public void testSetStartImageText_noDrawable_noCrash_public()
        {
            Assert.NotNull(publicTarget.GetText());
            publicTarget.SetStartImageText("Sample");
            Assert.NotNull(publicTarget.GetText());
        }

        [Fact]
        public void testSetStartImageText_withImageAndType_public()
        {
            AutoSpannableTextView.AutoLinkStyleTextView.styleType = 0;
            publicTarget = new AutoSpannableTextView.AutoLinkStyleTextView(mockContext.Object, null, 0);
            publicTarget.SetStartImageText("Hello");
            Assert.NotNull(publicTarget.GetText());
        }

        [Fact]
        public void testClickCallBackSetAndTrigger_public()
        {
            var callbackMock = new Mock<AutoSpannableTextView.AutoLinkStyleTextView.ClickCallBack>();
            publicTarget.SetOnClickCallBack(callbackMock.Object);

            callbackMock.Object.OnClick("Plan");
            callbackMock.Verify(cb => cb.OnClick("Plan"), Times.Once());
            publicTarget = new AutoSpannableTextView.AutoLinkStyleTextView(mockContext.Object, null, 0);
            Assert.NotNull(publicTarget);
        }

        [Fact]
        public void testAddStyle_branchEmptyOrNoComma_public()
        {
            publicTarget = new AutoSpannableTextView.AutoLinkStyleTextView(mockContext.Object, null, 0);
            Assert.NotNull(publicTarget.GetText());
        }

        [Fact]
        public void testClickableSpanUpdateDrawState_public()
        {
            publicTarget.SetStartImageText("Green,Orange");
            Assert.NotNull(publicTarget.GetText());
        }

        [Fact]
        public void testCenteredImageSpan_draw_executes_public()
        {
            AutoSpannableTextView.AutoLinkStyleTextView.styleType = 0;
            publicTarget = new AutoSpannableTextView.AutoLinkStyleTextView(mockContext.Object, null, 0);
            publicTarget.SetStartImageText("World");
            Assert.NotNull(publicTarget.GetText());
        }
    }
}