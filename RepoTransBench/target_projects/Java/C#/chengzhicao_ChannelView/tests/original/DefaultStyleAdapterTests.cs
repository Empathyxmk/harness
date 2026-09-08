using Xunit;

namespace Tests.Original
{
    // Minimal substitutes for Android Views and Adapter pattern
    public class TextView
    {
        public object Text { get; set; }
        private int textColor = 0;
        private float textSize = 0;
        public int CurrentTextColor => textColor;
        public float TextSize => textSize;

        public void SetTextColor(int color) { textColor = color; }
        public void SetTextSize(float size) { textSize = size; }
        public void SetBackgroundResource(int resourceId) { /* no-op for this test */ }
    }

    public class ViewGroup {}

    public class DefaultStyleAdapter
    {
        private int channelNormalTextColor, channelNormalBackground, channelFixedTextColor, channelFixedBackground, channelEditBackground, channelFocusedBackground, channelFocusedTextColor;
        private float channelTextSize;

        public class DefaultViewHolder
        {
            public TextView ItemView;
            public DefaultViewHolder(TextView itemView) { ItemView = itemView; }
        }

        public virtual DefaultViewHolder CreateStyleView(ViewGroup parent, string channelName)
        {
            var textView = new TextView { Text = channelName };
            return new DefaultViewHolder(textView);
        }

        public void SetTextColor(TextView view, int color)
        {
            view.SetTextColor(color);
        }

        public void SetTextSize(TextView view, float size)
        {
            view.SetTextSize(size);
        }

        public void SetBackgroundResource(TextView view, int resId)
        {
            view.SetBackgroundResource(resId);
        }

        public void SetChannelNormalTextColor(int val) { channelNormalTextColor = val; }
        public void SetChannelNormalBackground(int val) { channelNormalBackground = val; }
        public void SetChannelFixedTextColor(int val) { channelFixedTextColor = val; }
        public void SetChannelFixedBackground(int val) { channelFixedBackground = val; }
        public void SetChannelEditBackground(int val) { channelEditBackground = val; }
        public void SetChannelFocusedBackground(int val) { channelFocusedBackground = val; }
        public void SetChannelFocusedTextColor(int val) { channelFocusedTextColor = val; }
        public void SetChannelTextSize(float val) { channelTextSize = val; }

        public void SetNormalStyle(DefaultViewHolder holder) { /* Would set styles in UI, no-op for now */ }
        public void SetFixedStyle(DefaultViewHolder holder) { }
        public void SetEditStyle(DefaultViewHolder holder) { }
        public void SetFocusedStyle(DefaultViewHolder holder) { }
    }

    public class TestAdapter : DefaultStyleAdapter
    {
        public TestViewGroup Parent { get; private set; }

        public override DefaultViewHolder CreateStyleView(ViewGroup parent, string channelName)
        {
            this.Parent = (TestViewGroup)parent;
            return base.CreateStyleView(parent, channelName);
        }
    }

    public class TestViewGroup : ViewGroup {}

    public class DefaultStyleAdapterTests
    {
        [Fact]
        public void TestCreateStyleView()
        {
            var adapter = new TestAdapter();
            var parent = new TestViewGroup();
            var holder = adapter.CreateStyleView(parent, "MyChannel");
            Assert.IsType<TextView>(holder.ItemView);
            Assert.Equal("MyChannel", holder.ItemView.Text);
        }

        [Fact]
        public void TestSetters()
        {
            var adapter = new TestAdapter();
            var view = new TextView();
            adapter.SetTextColor(view, 0xff112233);
            Assert.Equal(0xff112233, view.CurrentTextColor);

            adapter.SetTextSize(view, 18f);
            Assert.Equal(18f, view.TextSize, 2);

            adapter.SetBackgroundResource(view, 0);
        }

        [Fact]
        public void TestSetStyleMethods()
        {
            var adapter = new TestAdapter();
            var view = new TextView();
            var holder = new DefaultStyleAdapter.DefaultViewHolder(view);

            adapter.SetChannelNormalTextColor(0xf1);
            adapter.SetChannelNormalBackground(0xa1);
            adapter.SetChannelFixedTextColor(0xf2);
            adapter.SetChannelFixedBackground(0xa2);
            adapter.SetChannelEditBackground(0xa3);
            adapter.SetChannelFocusedBackground(0xa4);
            adapter.SetChannelFocusedTextColor(0xf3);

            // Call these to ensure they do not throw
            adapter.SetNormalStyle(holder);
            adapter.SetFixedStyle(holder);
            adapter.SetEditStyle(holder);
            adapter.SetFocusedStyle(holder);
        }

        [Fact]
        public void TestSetChannelTextSize()
        {
            var adapter = new TestAdapter();
            adapter.SetChannelTextSize(123f);
        }
    }
}