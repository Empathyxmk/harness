using System;
using System.IO;
using Xunit;
using MeituanDianpingWalle;

namespace MeituanDianpingWalle.Tests
{
    public class ApkUtilTest
    {
        [Fact]
        public void TestGetApkSigningBlock_NullInput()
        {
            Assert.Throws<ArgumentNullException>(() => ApkUtil.GetApkSigningBlock(null));
        }

        [Fact]
        public void TestGetMapIdValue_EmptyArray()
        {
            Assert.Null(ApkUtil.GetMapIdValue(new ApkUtil.Pair[0], 0L));
        }

        [Fact]
        public void TestFindApkSignatureSchemeV2BlockId()
        {
            var dummy = new FileInfo("non-existent.apk");
            var ex = Record.Exception(() => ApkUtil.FindApkSignatureSchemeV2BlockId(dummy));
            Assert.NotNull(ex);
            Assert.True(ex is IOException);
        }
    }
}