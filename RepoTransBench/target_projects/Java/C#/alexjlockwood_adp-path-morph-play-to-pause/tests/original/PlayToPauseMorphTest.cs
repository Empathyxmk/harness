using Xunit;
using Adp.PathMorph;

namespace Adp.PathMorph.Tests.Original
{
    public class PlayToPauseMorphTest
    {
        [Fact]
        public void TestInitialStateIsPlaying()
        {
            var morph = new PlayToPauseMorph(true);
            Assert.True(morph.IsPlaying());
            Assert.Equal("PLAY", morph.GetState());
        }

        [Fact]
        public void TestInitialStateIsPause()
        {
            var morph = new PlayToPauseMorph(false);
            Assert.False(morph.IsPlaying());
            Assert.Equal("PAUSE", morph.GetState());
        }

        [Fact]
        public void TestToggleFunctionality()
        {
            var morph = new PlayToPauseMorph(true);
            morph.Toggle();
            Assert.False(morph.IsPlaying());
            Assert.Equal("PAUSE", morph.GetState());
            morph.Toggle();
            Assert.True(morph.IsPlaying());
            Assert.Equal("PLAY", morph.GetState());
        }
    }
}