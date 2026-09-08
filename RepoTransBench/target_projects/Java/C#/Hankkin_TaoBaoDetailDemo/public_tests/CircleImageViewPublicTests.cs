using Xunit;
using System.Drawing;
using Hankkin.Library;

namespace Hankkin.TaoBaoDetailDemo.Public.Tests
{
    public class CircleImageViewPublicTests
    {
        private class MockContext { }

        [Fact]
        public void Test_BorderColorChange()
        {
            var context = new MockContext();
            var civ = new CircleImageView(context);
            civ.SetBorderColor(Color.Red.ToArgb());
            Assert.Equal(Color.Red.ToArgb(), civ.GetBorderColor());

            civ.SetBorderColor(Color.Green.ToArgb());
            Assert.Equal(Color.Green.ToArgb(), civ.GetBorderColor());
        }

        [Fact]
        public void Test_BorderWidthChange()
        {
            var context = new MockContext();
            var civ = new CircleImageView(context);
            civ.SetBorderWidth(8);
            Assert.Equal(8, civ.GetBorderWidth());

            civ.SetBorderWidth(0);
            Assert.Equal(0, civ.GetBorderWidth());
        }

        [Fact]
        public void Test_FillColorChange()
        {
            var context = new MockContext();
            var civ = new CircleImageView(context);
            civ.SetFillColor(Color.Yellow.ToArgb());
            Assert.Equal(Color.Yellow.ToArgb(), civ.GetFillColor());

            civ.SetFillColor(Color.Cyan.ToArgb());
            Assert.Equal(Color.Cyan.ToArgb(), civ.GetFillColor());
        }

        [Fact]
        public void Test_BorderOverlayChange()
        {
            var context = new MockContext();
            var civ = new CircleImageView(context);
            civ.SetBorderOverlay(true);
            Assert.True(civ.IsBorderOverlay());

            civ.SetBorderOverlay(false);
            Assert.False(civ.IsBorderOverlay());
        }
    }
}