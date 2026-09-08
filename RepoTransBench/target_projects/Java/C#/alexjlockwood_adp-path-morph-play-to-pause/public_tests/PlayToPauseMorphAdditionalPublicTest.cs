using Xunit;
using Adp.PathMorph;

namespace Adp.PathMorph.PublicTests
{
    public class PlayToPauseMorphAdditionalPublicTest
    {
        [Fact]
        public void TestMultipleTogglesPublic()
        {
            var morph = new PlayToPauseMorph(true);
            // Toggle 4 times, state should alternate each time
            bool expected = true;
            for (int i = 0; i < 4; i++)
            {
                morph.Toggle();
                expected = !expected;
                Assert.Equal(expected, morph.IsPlaying());
            }
        }

        [Fact]
        public void TestGetStateStringsPublic()
        {
            var morph = new PlayToPauseMorph(false);
            Assert.Equal("PAUSE", morph.GetState());
            morph.Toggle();
            Assert.Equal("PLAY", morph.GetState());
        }

        [Fact]
        public void TestEdgeCaseNoTogglePublic()
        {
            var morphPause = new PlayToPauseMorph(false);
            Assert.Equal("PAUSE", morphPause.GetState());
            var morphPlay = new PlayToPauseMorph(true);
            Assert.Equal("PLAY", morphPlay.GetState());
        }
    }
}