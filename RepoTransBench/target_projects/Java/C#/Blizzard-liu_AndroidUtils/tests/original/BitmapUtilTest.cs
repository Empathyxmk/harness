using System;
using Xunit;

namespace AndroidUtils.Tests
{
    public class BitmapUtilTest
    {
        [Fact]
        public void TestCalculateInSampleSize_LargeImage()
        {
            var options = new BitmapOptions { OutWidth = 900, OutHeight = 900 };
            var outOptions = BitmapUtil.CalculateInSampleSize(options, 450, 400);
            Assert.Equal(options, outOptions);
            Assert.False(outOptions.InJustDecodeBounds);
            Assert.True(outOptions.InSampleSize > 1);
        }

        [Fact]
        public void TestCalculateInSampleSize_SmallImage()
        {
            var options = new BitmapOptions { OutWidth = 200, OutHeight = 100 };
            var outOptions = BitmapUtil.CalculateInSampleSize(options, 450, 400);
            Assert.Equal(options, outOptions);
            Assert.False(outOptions.InJustDecodeBounds);
            Assert.Equal(1, outOptions.InSampleSize);
        }

        [Fact]
        public void TestConstructor_ThrowsError()
        {
            Assert.Throws<Exception>(() => new BitmapUtil());
        }
    }

    public class BitmapOptions
    {
        public int OutWidth { get; set; }
        public int OutHeight { get; set; }
        public bool InJustDecodeBounds { get; set; }
        public int InSampleSize { get; set; }
    }

    public class BitmapUtil
    {
        public BitmapUtil()
        {
            throw new Exception("No instantiation allowed");
        }

        // Mimic static method for test
        public static BitmapOptions CalculateInSampleSize(BitmapOptions options, int reqWidth, int reqHeight)
        {
            int height = options.OutHeight;
            int width = options.OutWidth;
            int inSampleSize = 1;
            if (height > reqHeight || width > reqWidth)
            {
                int halfHeight = height / 2;
                int halfWidth = width / 2;
                while ((halfHeight / inSampleSize) >= reqHeight && (halfWidth / inSampleSize) >= reqWidth)
                {
                    inSampleSize *= 2;
                }
            }
            options.InSampleSize = inSampleSize;
            options.InJustDecodeBounds = false;
            return options;
        }
    }
}