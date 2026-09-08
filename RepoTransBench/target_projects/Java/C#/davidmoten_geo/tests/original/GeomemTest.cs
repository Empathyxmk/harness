using Xunit;
using System;
using System.Collections.Generic;

namespace DavidMoten.Geo.Tests
{
    public class GeomemTest
    {
        private static readonly double topLeftLat = -5;
        private static readonly double topLeftLong = 100;
        private static readonly double bottomRightLat = -45;
        private static readonly double bottomRightLong = 170;
        private static readonly double PRECISION = 1e-5;

        private Info<string, string> CreateInfo(double lat, double lon)
        {
            return new Info<string, string>(lat, lon, 100, "A", Optional<string>.Of("A"));
        }

        [Fact]
        public void TestGeomemFindWhenNoData()
        {
            var g = new Geomem<string, string>();
            var result = g.Find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000);
            // Should not throw, but may be empty
        }

        [Fact]
        public void TestRegionFilter()
        {
            var g = new Geomem<string, string>();
            Predicate<Info<string, string>> predicate = g.CreateRegionFilter(
                topLeftLat, topLeftLong, bottomRightLat, bottomRightLong);
            // inside
            Assert.True(predicate(CreateInfo(topLeftLat - 1, topLeftLong + 1)));
            // outside north
            Assert.False(predicate(CreateInfo(topLeftLat + 1, topLeftLong + 1)));
            // outside west
            Assert.False(predicate(CreateInfo(topLeftLat - 1, topLeftLong - 1)));
            // outside east
            Assert.False(predicate(CreateInfo(topLeftLat - 1, bottomRightLong + 1)));
            // outside south
            Assert.False(predicate(CreateInfo(bottomRightLat - 1, bottomRightLong - 1)));
        }

        [Fact]
        public void TestGeomemFindWhenOneEntryInsideRegion()
        {
            var g = new Geomem<string, string>();
            g.Add(-15, 120, 500, "A1", "a1");
            var list = new List<Info<string, string>>(g.Find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000));
            Assert.Single(list);
            Assert.Equal(-15, list[0].Lat, PRECISION);
            Assert.Equal(120, list[0].Lon, PRECISION);
            Assert.Equal(500L, list[0].Time);
            Assert.Equal("A1", list[0].Value);
            Assert.Equal("a1", list[0].Id.Get());
            Console.WriteLine(list[0]);
        }

        [Fact]
        public void TestGeomemFindWhenOneEntryInsideRegionUsingAlternativeAddMethod()
        {
            var g = new Geomem<string, string>();
            g.Add(-15, 120, 500, "A1");
            var list = new List<Info<string, string>>(g.Find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000));
            Assert.Single(list);
            Assert.Equal(-15, list[0].Lat, PRECISION);
            Assert.Equal(120, list[0].Lon, PRECISION);
            Assert.Equal(500L, list[0].Time);
            Assert.Equal("A1", list[0].Value);
            Assert.Equal("A1", list[0].Id.Get());
            Console.WriteLine(list[0]);
        }

        [Fact]
        public void TestGeomemFindWhenOneEntryInsideRegionUsingAlternativeAddMethod2()
        {
            var g = new Geomem<string, string>();
            g.Add(-15, 120, 500, "A1", Optional<string>.Absent());
            var list = new List<Info<string, string>>(g.Find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000));
            Assert.Single(list);
            Assert.Equal(-15, list[0].Lat, PRECISION);
            Assert.Equal(120, list[0].Lon, PRECISION);
            Assert.Equal(500L, list[0].Time);
            Assert.Equal("A1", list[0].Value);
            Assert.False(list[0].Id.IsPresent());
            Console.WriteLine(list[0]);
        }

        [Fact]
        public void TestGeomemFindWhenOneEntryOutsideRegion()
        {
            var g = new Geomem<string, string>();
            g.Add(15, 120, 500, "A1", "a1");
            var list = new List<Info<string, string>>(g.Find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000));
            Assert.Empty(list);
        }

        [Fact(Skip = "Long-running benchmark")]
        public void TestGeomemManyEntries()
        {
            Console.WriteLine($"maxMemory={GC.GetTotalMemory(false) / 1048576}MB");
            var g = new Geomem<string, string>();
            GC.Collect();
            System.Threading.Thread.Sleep(100);
            ReportMemoryUsage();
            for (int i = 0; i < 10000; i++)
            {
                if (i % 1000 == 0)
                {
                    Console.WriteLine($"count={i}");
                    ReportMemoryUsage();
                }
                AddRandomEntry(g);
            }
            ReportMemoryUsage();
            GC.Collect();
            System.Threading.Thread.Sleep(100);
            ReportMemoryUsage();
            var list = new List<Info<string, string>>(g.Find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000));
            Console.WriteLine(list.Count);
        }

        private void ReportMemoryUsage()
        {
            Console.WriteLine($"memUsed={(GC.GetTotalMemory(false) / 1048576)}MB");
        }

        private void AddRandomEntry(Geomem<string, string> g)
        {
            double lat = topLeftLat + 5 - new Random().NextDouble() * 40;
            double lon = topLeftLong - 5 + new Random().NextDouble() * 80;
            long t = (long)(new Random().NextDouble() * 1200);
            string id = Guid.NewGuid().ToString().Substring(0, 2);
            g.Add(lat, lon, t, id, id);
        }
    }
}