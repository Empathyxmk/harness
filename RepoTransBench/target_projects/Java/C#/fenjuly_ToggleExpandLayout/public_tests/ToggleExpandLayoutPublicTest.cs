using Xunit;
using Moq;
using Fenjuly.ToggleExpandLayout;

namespace Fenjuly.ToggleExpandLayout.Tests.Public
{
    public class ToggleExpandLayoutPublicTest
    {
        private ToggleExpandLayout layout;
        private Context context;
        private AttributeSet attrs;

        public ToggleExpandLayoutPublicTest()
        {
            context = new Context();
            attrs = new AttributeSet();
            layout = new ToggleExpandLayout(context, attrs, 123);
        }

        [Fact]
        public void TestConstructorWithDifferentDataPublic()
        {
            var layout2 = new ToggleExpandLayout(context, attrs, 789);
            Assert.NotNull(layout2);
        }

        [Fact]
        public void TestOpenCloseNoCrash()
        {
            layout.Open();
            layout.Close();
        }

        [Fact]
        public void TestSetOnToggleTouchListenerNoCrash()
        {
            var listener = new TestListener();
            layout.SetOnToggleTouchListener(listener);
            layout.Open();
            layout.Close();
        }

        private class TestListener : ToggleExpandLayout.IOnToggleTouchListener
        {
            public void OnStartOpen(int h, int oh) { }
            public void OnOpen() { }
            public void OnStartClose(int h, int oh) { }
            public void OnClosed() { }
        }
    }
}