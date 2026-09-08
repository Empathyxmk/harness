using Xunit;
using Adp.PathMorph;

namespace Adp.PathMorph.Tests.Original
{
    public class PlayToPauseMorphAdditionalTest
    {
        [Fact]
        public void TestMultipleToggles()
        {
            var morph = new PlayToPauseMorph(false);
            // Toggle 5 times, state should alternate each time
            bool expected = false;
            for (int i = 0; i < 5; i++)
            {
                morph.Toggle();
                expected = !expected;
                Assert.Equal(expected, morph.IsPlaying());
            }
        }

        [Fact]
        public void TestGetStateStrings()
        {
            var morph = new PlayToPauseMorph(true);
            Assert.Equal("PLAY", morph.GetState());
            morph.Toggle();
            Assert.Equal("PAUSE", morph.GetState());
        }

        [Fact]
        public void TestEdgeCaseNoToggle()
        {
            var morphPlay = new PlayToPauseMorph(true);
            Assert.Equal("PLAY", morphPlay.GetState());
            var morphPause = new PlayToPauseMorph(false);
            Assert.Equal("PAUSE", morphPause.GetState());
        }
    }
}