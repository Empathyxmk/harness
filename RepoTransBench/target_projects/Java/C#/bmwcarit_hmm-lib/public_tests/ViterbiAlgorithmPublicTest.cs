using System;
using System.Collections.Generic;
using Xunit;
using BmwcaritHmmLib;

namespace PublicTests
{
    public class ViterbiAlgorithmPublicTest
    {
        static readonly string S1 = "X";
        static readonly string S2 = "Y";
        static readonly string S3 = "Z";

        [Fact]
        public void TestSimpleMostLikelySequencePublic()
        {
            var states = new List<string> { S1, S2, S3 };

            var initialProbs = new Dictionary<string, double>
            {
                { S1, 0.3 },
                { S2, 0.6 },
                { S3, 0.1 }
            };

            var transitions = new Dictionary<Transition<string>, double>
            {
                { new Transition<string>(S1, S1), 0.5 },
                { new Transition<string>(S1, S2), 0.2 },
                { new Transition<string>(S1, S3), 0.3 },
                { new Transition<string>(S2, S1), 0.1 },
                { new Transition<string>(S2, S2), 0.7 },
                { new Transition<string>(S2, S3), 0.2 },
                { new Transition<string>(S3, S1), 0.4 },
                { new Transition<string>(S3, S2), 0.3 },
                { new Transition<string>(S3, S3), 0.3 }
            };

            var emission1 = new Dictionary<string, double>
            {
                { S1, 0.5 },
                { S2, 0.4 },
                { S3, 0.1 }
            };

            var emission2 = new Dictionary<string, double>
            {
                { S1, 0.1 },
                { S2, 0.8 },
                { S3, 0.1 }
            };

            var emission3 = new Dictionary<string, double>
            {
                { S1, 0.6 },
                { S2, 0.3 },
                { S3, 0.1 }
            };

            var observations = new List<string> { "ObsA", "ObsB", "ObsC" };
            var emissions = new List<Dictionary<string, double>> { emission1, emission2, emission3 };

            var viterbi = new ViterbiAlgorithm<string, string>();
            viterbi.StartWithInitialStateProbabilities(states, initialProbs);

            for (int i = 0; i < observations.Count; i++)
            {
                viterbi.NextStep(observations[i], states, emissions[i], transitions, "t" + i);
            }

            var result = viterbi.ComputeMostLikelySequence();
            Assert.Equal(4, result.Count);
            Assert.Equal(S2, result[0].State);
            Assert.Equal(S2, result[1].State);
            Assert.Equal(S2, result[2].State);
            Assert.Equal(S2, result[3].State);
        }

        [Fact]
        public void TestNullTransitionDescriptorPublic()
        {
            var states = new List<string> { S1, S2 };

            var initialProbs = new Dictionary<string, double>
            {
                { S1, 0.5 },
                { S2, 0.5 }
            };

            var transitions = new Dictionary<Transition<string>, double>
            {
                { new Transition<string>(S1, S1), 0.5 },
                { new Transition<string>(S1, S2), 0.5 },
                { new Transition<string>(S2, S1), 0.5 },
                { new Transition<string>(S2, S2), 0.5 }
            };

            var emission1 = new Dictionary<string, double>
            {
                { S1, 1.0 },
                { S2, 0.0 }
            };

            var viterbi = new ViterbiAlgorithm<string, int>();
            viterbi.StartWithInitialStateProbabilities(states, initialProbs);
            viterbi.NextStep(1, states, emission1, transitions, null);

            var result = viterbi.ComputeMostLikelySequence();
            Assert.Null(result[1].TransitionDescriptor);
        }
    }
}