using Xunit;
using System.Drawing;
using Hankkin.Library;

namespace Hankkin.TaoBaoDetailDemo.Original.Tests
{
    public class CircleImageViewTests
    {
        private object context = new object();

        [Fact]
        public void Test_ConstructorsAndInit()
        {
            var civ1 = new CircleImageView(context);
            Assert.Equal("CENTER_CROP", civ1.ScaleType);

            var cimAttrs = new object();
            var civ2 = new CircleImageView(context, cimAttrs);
            Assert.Equal("CENTER_CROP", civ2.ScaleType);
        }

        [Fact]
        public void Test_SetScaleTypeThrows()
        {
            var civ = new CircleImageView(context);
            var ex = Assert.Throws<System.ArgumentException>(() => civ.SetScaleType("FIT_XY"));
            Assert.Contains("CENTER_CROP", ex.Message);
        }

        [Fact]
        public void Test_SetAdjustViewBoundsThrows()
        {
            var civ = new CircleImageView(context);
            Assert.Throws<System.ArgumentException>(() => civ.SetAdjustViewBounds(true));
        }

        [Fact]
        public void Test_OnDrawWithNoBitmap()
        {
            var civ = new CircleImageView(context);
            civ.OnDraw(new object());
            // Nothing to assert, just should not throw
        }

        [Fact]
        public void Test_SetBorderAndFillColor()
        {
            var civ = new CircleImageView(context);
            civ.SetBorderColor(Color.Blue.ToArgb());
            civ.SetBorderWidth(5);
            civ.SetFillColor(Color.Yellow.ToArgb());
            Assert.Equal(Color.Blue.ToArgb(), civ.GetBorderColor());
            Assert.Equal(5, civ.GetBorderWidth());
            Assert.Equal(Color.Yellow.ToArgb(), civ.GetFillColor());
        }

        [Fact]
        public void Test_SetDisableCircularTransformation()
        {
            var civ = new CircleImageView(context);
            civ.SetDisableCircularTransformation(true);
            Assert.True(civ.IsDisableCircularTransformation());
            civ.SetDisableCircularTransformation(false);
            Assert.False(civ.IsDisableCircularTransformation());
        }
    }
}