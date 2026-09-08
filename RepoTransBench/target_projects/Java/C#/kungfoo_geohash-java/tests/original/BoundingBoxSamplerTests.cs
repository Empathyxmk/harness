using Xunit;
using GeoHashLib;
using GeoHashLib.util;
using System.Collections.Generic;

namespace GeoHashLib.OriginalTests.util
{
    public class BoundingBoxSamplerTests
    {
        [Fact]
        public void SamplerTest()
        {
            // Corresponds to src/test/java/ch/hsr/geohash/util/BoundingBoxSamplerTest.java
            var bbox = new BoundingBox(37.7, 37.84, -122.52, -122.35);
            var sampler = new BoundingBoxSampler(TwoGeoHashBoundingBox.WithBitPrecision(bbox, 35), 1179);

            bbox = sampler.GetBoundingBox().GetBoundingBox();
            GeoHash gh = sampler.Next();
            var hashes = new HashSet<string>();
            int sumOfComp = 0;
            int crossingZero = 0;

            GeoHash prev = null;
            while (gh != null)
            {
                Assert.True(bbox.Contains(gh.GetOriginatingPoint()));
                Assert.False(hashes.Contains(gh.ToBase32()));
                hashes.Add(gh.ToBase32());
                if (prev != null)
                {
                    sumOfComp += prev.CompareTo(gh);
                }
                prev = gh;
                if (sumOfComp == 0)
                {
                    crossingZero++;
                }
                gh = sampler.Next();
            }
            Assert.Equal(12875, hashes.Count);
            // The expected value of the sum should be zero. This checks that it is
            // at least close. Worst case is 12875 or -12875 so -40 is sufficiently
            // close
            Assert.Equal(-40, sumOfComp);
            // Check that the sum is zero a number of times, to make sure values are
            // increasing and decreasing.
            Assert.Equal(123, crossingZero);
        }
    }
}