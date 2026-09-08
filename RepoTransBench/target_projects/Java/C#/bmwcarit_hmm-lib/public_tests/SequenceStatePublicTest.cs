using System;
using Xunit;
using BmwcaritHmmLib;

namespace PublicTests
{
    public class SequenceStatePublicTest
    {
        [Fact]
        public void TestSequenceStateFieldsPublic()
        {
            string state = "state_2";
            int observation = 99;
            string transitionDesc = "public_desc";
            double smoothing = 0.75;

            var seqState = new SequenceState<string, int, string>(state, observation, transitionDesc, smoothing);

            Assert.Equal(state, seqState.State);
            Assert.Equal(observation, seqState.Observation);
            Assert.Equal(transitionDesc, seqState.TransitionDescriptor);
            Assert.Equal(smoothing, seqState.SmoothingProbability);
        }

        [Fact]
        public void TestSequenceStateNullsPublic()
        {
            var seqState = new SequenceState<string, int?, string>("public_state", null, null, null);

            Assert.Equal("public_state", seqState.State);
            Assert.Null(seqState.Observation);
            Assert.Null(seqState.TransitionDescriptor);
            Assert.Null(seqState.SmoothingProbability);
        }
    }
}