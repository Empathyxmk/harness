using System;
using System.IO;
using Xunit;
using ArCpText;

namespace ArCpText.PublicTests
{
    public class ImageUtilsPublicTests : IDisposable
    {
        private string tempFile;

        [Fact]
        public void TestGetYUVByteSize_Public()
        {
            Assert.Equal(8 * 8 + 4 * 4 * 2, ImageUtils.getYUVByteSize(8, 8));
            Assert.Equal(5 * 7 + 3 * 4 * 2, ImageUtils.getYUVByteSize(5, 7));
        }

        [Fact]
        public void TestConvertImageToBitmapCallsConvertYUV420ToARGB8888_Public()
        {
            int[] output = new int[16];
            var result = ImageUtils.convertImageToBitmap(new object(), output, new byte[3][]);
            Assert.NotNull(result);
            Assert.Equal(16, result.Length);
        }

        [Fact]
        public void TestSaveBitmapToDiskCreatesFile_Public()
        {
            tempFile = Path.GetTempFileName();
            byte[] data = new byte[] { 7, 9, 11, 13, 21, 0, 42, 99, 121 };
            ImageUtils.saveBitmapToDisk(data, tempFile);
            Assert.True(File.Exists(tempFile));
            Assert.Equal(9, new FileInfo(tempFile).Length);
        }

        [Fact]
        public void TestYUV2RGBClamping_Public()
        {
            int rgb = ImageUtils.CallPrivateYUV2RGB(-50, 0, 300);
            Assert.Equal(0xFF000000, rgb & unchecked((int)0xFF000000));
        }

        public void Dispose()
        {
            if (!string.IsNullOrEmpty(tempFile) && File.Exists(tempFile))
            {
                File.Delete(tempFile);
            }
        }
    }
}