using System;
using TwigNetbeans;
using Xunit;

namespace TwigNetbeans.PublicTests
{
    public class TwigStructureScannerPublicTests
    {
        [Fact]
        public void TestScanEmptyReturnsListPublic()
        {
            var scanner = new TwigStructureScanner();
            Assert.Empty(scanner.Scan("", null));
        }

        [Fact]
        public void TestGetHeaderReturnsNullPublic()
        {
            var scanner = new TwigStructureScanner();
            Assert.Null(scanner.GetHeader(""));
        }
    }
}