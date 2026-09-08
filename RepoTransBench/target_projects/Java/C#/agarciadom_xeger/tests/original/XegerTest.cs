using System;
using System.Collections.Generic;
using Xunit;

namespace XegerLib.Tests.Original
{
    public class XegerTest
    {
        [Fact]
        public void ShouldGenerateTextCorrectly()
        {
            string regex = "[ab]{4,6}c";
            var generator = new Xeger(regex);
            for (int i = 0; i < 100; i++)
            {
                string text = generator.Generate();
                Assert.Matches(regex, text);
            }
        }

        [Fact]
        public void TestRepeatableRegex()
        {
            for (int x = 0; x < 1000; x++)
            {
                var generator = new Xeger("[ab]{4,6}c", new Random(1000));
                var generator2 = new Xeger("[ab]{4,6}c", new Random(1000));

                List<string> firstRegexList = GenerateRegex(generator, 100);
                List<string> secondRegexList = GenerateRegex(generator2, 100);

                AssertListEquals(firstRegexList, secondRegexList);
            }
        }

        [Fact]
        public void TestWalkRange()
        {
            for (int x = 0; x < 100; x++)
            {
                var generator = new Xeger("[ab]{0,100}c", new Random(1000));
                var generator2 = new Xeger("[ab]{0,100}c", new Random(1000));

                List<string> firstRegexList = GenerateRegex(generator, 100, 0, 100);
                List<string> secondRegexList = GenerateRegex(generator2, 100, 0, 100);
                AssertListEquals(firstRegexList, secondRegexList);
            }
        }

        private List<string> GenerateRegex(Xeger generator, int count, int minLength, int maxLength)
        {
            var regexList = new List<string>();
            for (int i = 0; i < count; i++)
            {
                try
                {
                    regexList.Add(generator.Generate(minLength, maxLength));
                }
                catch (Xeger.FailedRandomWalkException)
                {
                    regexList.Add(null);
                }
            }
            return regexList;
        }

        private void AssertListEquals<T>(List<T> firstRegexList, List<T> secondRegexList)
        {
            Assert.Equal(firstRegexList.Count, secondRegexList.Count);
            for (int i = 0; i < firstRegexList.Count; i++)
            {
                Assert.Equal(firstRegexList[i], secondRegexList[i]);
            }
        }

        private List<string> GenerateRegex(Xeger generator, int count)
        {
            var regexList = new List<string>();
            for (int i = 0; i < count; i++)
            {
                regexList.Add(generator.Generate());
            }
            return regexList;
        }
    }
}