using Xunit;
using Adp.PathMorph;

namespace Adp.PathMorph.PublicTests
{
    public class PlayToPauseMorphPublicTest
    {
        [Fact]
        public void TestInitialStateIsPausePublic()
        {
            var morph = new PlayToPauseMorph(false);
            Assert.False(morph.IsPlaying());
            Assert.Equal("PAUSE", morph.GetState());
        }

        [Fact]
        public void TestInitialStateIsPlayingPublic()
        {
            var morph = new PlayToPauseMorph(true);
            Assert.True(morph.IsPlaying());
            Assert.Equal("PLAY", morph.GetState());
        }

        [Fact]
        public void TestDoubleToggleFunctionalityPublic()
        {
            var morph = new PlayToPauseMorph(false);
            morph.Toggle();
            Assert.True(morph.IsPlaying());
            Assert.Equal("PLAY", morph.GetState());
            morph.Toggle();
            Assert.False(morph.IsPlaying());
            Assert.Equal("PAUSE", morph.GetState());
        }
    }
}