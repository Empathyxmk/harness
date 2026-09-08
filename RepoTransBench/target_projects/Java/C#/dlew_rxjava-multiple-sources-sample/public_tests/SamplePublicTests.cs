using System.Threading;
using Xunit;
using MultipleSourcesSample;

namespace MultipleSourcesSample.PublicTests
{
    public class SamplePublicTests
    {
        [Fact]
        public void TestSampleMainRunsPublic()
        {
            // Just call sleep, as Sample.main is not implemented fully
            Sample.Sleep(10);
        }
    }
}