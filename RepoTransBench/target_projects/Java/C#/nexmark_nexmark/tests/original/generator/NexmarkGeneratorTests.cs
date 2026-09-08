using System;
using Xunit;
using NexmarkFlink.generator;
using NexmarkFlink;
using NexmarkFlink.model;

namespace OriginalTests.generator
{
    public class NexmarkGeneratorTests
    {
        [Fact]
        public void TestGenerate()
        {
            var nexmarkConfiguration = new NexmarkConfiguration { BidProportion = 46 };
            var generatorConfig = new GeneratorConfig(
                nexmarkConfiguration, DateTimeOffset.Now.ToUnixTimeMilliseconds(), 1, 100, 1);
            var generator = new NexmarkGenerator(generatorConfig);
            int count = 0;
            while (generator.HasNext())
            {
                Event e = generator.Next().Event;
                count++;
                Console.WriteLine(e);
            }
            Console.WriteLine($"Total event:{count}");
        }
    }
}