using System;
using Xunit;
using BmwcaritHmmLib;

namespace OriginalTests
{
    public class SequenceStateTest
    {
        [Fact]
        public void TestSequenceStateFields()
        {
            string state = "state_1";
            int observation = 42;
            string transitionDesc = "desc";
            double smoothing = 0.5;

            var seqState = new SequenceState<string, int, string>(state, observation, transitionDesc, smoothing);

            Assert.Equal(state, seqState.State);
            Assert.Equal(observation, seqState.Observation);
            Assert.Equal(transitionDesc, seqState.TransitionDescriptor);
            Assert.Equal(smoothing, seqState.SmoothingProbability);
        }

        [Fact]
        public void TestSequenceStateNulls()
        {
            var seqState = new SequenceState<string, int?, string>("state", null, null, null);

            Assert.Equal("state", seqState.State);
            Assert.Null(seqState.Observation);
            Assert.Null(seqState.TransitionDescriptor);
            Assert.Null(seqState.SmoothingProbability);
        }
    }
}