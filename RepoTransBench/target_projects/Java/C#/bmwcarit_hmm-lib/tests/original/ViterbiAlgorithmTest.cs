using System;
using System.Collections.Generic;
using Xunit;
using BmwcaritHmmLib;
using static System.Math;

namespace OriginalTests
{
    public class ViterbiAlgorithmTest
    {
        private class Rain
        {
            public static readonly Rain T = new Rain();
            public static readonly Rain F = new Rain();

            public override string ToString()
            {
                if (ReferenceEquals(this, T)) return "Rain";
                if (ReferenceEquals(this, F)) return "Sun";
                throw new InvalidOperationException();
            }
        }

        private class Umbrella
        {
            public static readonly Umbrella T = new Umbrella();
            public static readonly Umbrella F = new Umbrella();

            public override string ToString()
            {
                if (ReferenceEquals(this, T)) return "Umbrella";
                if (ReferenceEquals(this, F)) return "No umbrella";
                throw new InvalidOperationException();
            }
        }

        private class Descriptor
        {
            public static readonly Descriptor R2R = new Descriptor();
            public static readonly Descriptor R2S = new Descriptor();
            public static readonly Descriptor S2R = new Descriptor();
            public static readonly Descriptor S2S = new Descriptor();

            public override string ToString()
            {
                if (ReferenceEquals(this, R2R)) return "R2R";
                if (ReferenceEquals(this, R2S)) return "R2S";
                if (ReferenceEquals(this, S2R)) return "S2R";
                if (ReferenceEquals(this, S2S)) return "S2S";
                throw new InvalidOperationException();
            }
        }

        private static double DELTA = 1e-8;

        private List<Rain> States(List<SequenceState<Rain, Umbrella, Descriptor>> sequenceStates)
        {
            var result = new List<Rain>();
            foreach (var ss in sequenceStates)
                result.Add(ss.State);
            return result;
        }

        [Fact]
        public void TestComputeMostLikelySequence()
        {
            var candidates = new List<Rain> { Rain.T, Rain.F };

            var emissionLogProbabilitiesForUmbrella = new Dictionary<Rain, double>
            {
                { Rain.T, Log(0.9) },
                { Rain.F, Log(0.2) }
            };

            var emissionLogProbabilitiesForNoUmbrella = new Dictionary<Rain, double>
            {
                { Rain.T, Log(0.1) },
                { Rain.F, Log(0.8) }
            };

            var transitionLogProbabilities = new Dictionary<Transition<Rain>, double>
            {
                { new Transition<Rain>(Rain.T, Rain.T), Log(0.7) },
                { new Transition<Rain>(Rain.T, Rain.F), Log(0.3) },
                { new Transition<Rain>(Rain.F, Rain.T), Log(0.3) },
                { new Transition<Rain>(Rain.F, Rain.F), Log(0.7) }
            };

            var transitionDescriptors = new Dictionary<Transition<Rain>, Descriptor>
            {
                { new Transition<Rain>(Rain.T, Rain.T), Descriptor.R2R },
                { new Transition<Rain>(Rain.T, Rain.F), Descriptor.R2S },
                { new Transition<Rain>(Rain.F, Rain.T), Descriptor.S2R },
                { new Transition<Rain>(Rain.F, Rain.F), Descriptor.S2S }
            };

            var viterbi = new ViterbiAlgorithm<Rain, Umbrella, Descriptor>()
                .SetKeepMessageHistory(true)
                .SetComputeSmoothingProbabilities(true);
            viterbi.StartWithInitialObservation(Umbrella.T, candidates, emissionLogProbabilitiesForUmbrella);
            viterbi.NextStep(Umbrella.T, candidates, emissionLogProbabilitiesForUmbrella, transitionLogProbabilities, transitionDescriptors);
            viterbi.NextStep(Umbrella.F, candidates, emissionLogProbabilitiesForNoUmbrella, transitionLogProbabilities, transitionDescriptors);
            viterbi.NextStep(Umbrella.T, candidates, emissionLogProbabilitiesForUmbrella, transitionLogProbabilities, transitionDescriptors);

            var result = viterbi.ComputeMostLikelySequence();

            Assert.Equal(4, result.Count);
            Assert.Equal(Rain.T, result[0].State);
            Assert.Equal(Rain.T, result[1].State);
            Assert.Equal(Rain.F, result[2].State);
            Assert.Equal(Rain.T, result[3].State);

            Assert.Equal(Umbrella.T, result[0].Observation);
            Assert.Equal(Umbrella.T, result[1].Observation);
            Assert.Equal(Umbrella.F, result[2].Observation);
            Assert.Equal(Umbrella.T, result[3].Observation);

            Assert.Null(result[0].TransitionDescriptor);
            Assert.Equal(Descriptor.R2R, result[1].TransitionDescriptor);
            Assert.Equal(Descriptor.R2S, result[2].TransitionDescriptor);
            Assert.Equal(Descriptor.S2R, result[3].TransitionDescriptor);

            Assert.False(viterbi.IsBroken());

            // Check message history
            var expectedMessageHistory = new List<Dictionary<Rain, double>>
            {
                new Dictionary<Rain, double> { { Rain.T, 0.9 }, { Rain.F, 0.2 } },
                new Dictionary<Rain, double> { { Rain.T, 0.567 }, { Rain.F, 0.054 } },
                new Dictionary<Rain, double> { { Rain.T, 0.03969 }, { Rain.F, 0.13608 } },
                new Dictionary<Rain, double> { { Rain.T, 0.0367416 }, { Rain.F, 0.0190512 } }
            };
            var actualMessageHistory = viterbi.MessageHistory();
            CheckMessageHistory(expectedMessageHistory, actualMessageHistory);
        }

        [Fact]
        public void TestSetParams()
        {
            var viterbi = new ViterbiAlgorithm<Rain, Umbrella, Descriptor>();
            Assert.False(viterbi.IsKeepMessageHistory());
            viterbi.SetKeepMessageHistory(true);
            Assert.True(viterbi.IsKeepMessageHistory());
            viterbi.SetKeepMessageHistory(false);
            Assert.False(viterbi.IsKeepMessageHistory());

            Assert.False(viterbi.IsComputeSmoothingProbabilities());
            viterbi.SetComputeSmoothingProbabilities(true);
            Assert.True(viterbi.IsComputeSmoothingProbabilities());
            viterbi.SetComputeSmoothingProbabilities(false);
            Assert.False(viterbi.IsComputeSmoothingProbabilities());
        }

        private void CheckMessageHistory(IList<Dictionary<Rain, double>> expected, IList<Dictionary<Rain, double>> actual)
        {
            Assert.Equal(expected.Count, actual.Count);
            for (int i = 0; i < expected.Count; i++)
            {
                CheckMessage(expected[i], actual[i]);
            }
        }

        private void CheckMessage(Dictionary<Rain, double> expected, Dictionary<Rain, double> actual)
        {
            Assert.Equal(expected.Count, actual.Count);
            foreach (var entry in expected)
            {
                // The Java version checks actual[entry.Key] as exp(actual[x]): we assume actual stores log-probs.
                Assert.Equal(entry.Value, Math.Exp(actual[entry.Key]), 8);
            }
        }

        [Fact]
        public void TestEmptySequence()
        {
            var viterbi = new ViterbiAlgorithm<Rain, Umbrella, Descriptor>();
            var result = viterbi.ComputeMostLikelySequence();
            Assert.Empty(result);
            Assert.False(viterbi.IsBroken());
        }

        [Fact]
        public void TestBreakAtInitialMessage()
        {
            var viterbi = new ViterbiAlgorithm<Rain, Umbrella, Descriptor>();
            var candidates = new List<Rain> { Rain.T, Rain.F };
            var emissionLogProbabilities = new Dictionary<Rain, double>
            {
                { Rain.T, Log(0.0) },
                { Rain.F, Log(0.0) }
            };
            viterbi.StartWithInitialObservation(Umbrella.T, candidates, emissionLogProbabilities);
            Assert.True(viterbi.IsBroken());
            Assert.Empty(viterbi.ComputeMostLikelySequence());
        }

        [Fact]
        public void TestEmptyInitialMessage()
        {
            var viterbi = new ViterbiAlgorithm<Rain, Umbrella, Descriptor>();
            viterbi.StartWithInitialObservation(Umbrella.T, new List<Rain>(), new Dictionary<Rain, double>());
            Assert.True(viterbi.IsBroken());
            Assert.Empty(viterbi.ComputeMostLikelySequence());
        }

        [Fact]
        public void TestBreakAtFirstTransition()
        {
            var viterbi = new ViterbiAlgorithm<Rain, Umbrella, Descriptor>();
            var candidates = new List<Rain> { Rain.T, Rain.F };
            var emissionLogProbabilities = new Dictionary<Rain, double>
            {
                { Rain.T, Log(0.9) },
                { Rain.F, Log(0.2) }
            };
            viterbi.StartWithInitialObservation(Umbrella.T, candidates, emissionLogProbabilities);
            Assert.False(viterbi.IsBroken());

            var transitionLogProbabilities = new Dictionary<Transition<Rain>, double>
            {
                { new Transition<Rain>(Rain.T, Rain.T), Log(0.0) },
                { new Transition<Rain>(Rain.T, Rain.F), Log(0.0) },
                { new Transition<Rain>(Rain.F, Rain.T), Log(0.0) },
                { new Transition<Rain>(Rain.F, Rain.F), Log(0.0) }
            };
            viterbi.NextStep(Umbrella.T, candidates, emissionLogProbabilities, transitionLogProbabilities);
            Assert.True(viterbi.IsBroken());
            Assert.Equal(new List<Rain> { Rain.T }, States(viterbi.ComputeMostLikelySequence()));
        }

        [Fact]
        public void TestBreakAtFirstTransitionWithNoCandidates()
        {
            var viterbi = new ViterbiAlgorithm<Rain, Umbrella, Descriptor>();
            var candidates = new List<Rain> { Rain.T, Rain.F };
            var emissionLogProbabilities = new Dictionary<Rain, double>
            {
                { Rain.T, Log(0.9) },
                { Rain.F, Log(0.2) }
            };
            viterbi.StartWithInitialObservation(Umbrella.T, candidates, emissionLogProbabilities);
            Assert.False(viterbi.IsBroken());

            viterbi.NextStep(Umbrella.T, new List<Rain>(), new Dictionary<Rain, double>(), new Dictionary<Transition<Rain>, double>());
            Assert.True(viterbi.IsBroken());
            Assert.Equal(new List<Rain> { Rain.T }, States(viterbi.ComputeMostLikelySequence()));
        }

        [Fact]
        public void TestBreakAtSecondTransition()
        {
            var viterbi = new ViterbiAlgorithm<Rain, Umbrella, Descriptor>();
            var candidates = new List<Rain> { Rain.T, Rain.F };
            var emissionLogProbabilities = new Dictionary<Rain, double>
            {
                { Rain.T, Log(0.9) },
                { Rain.F, Log(0.2) }
            };
            viterbi.StartWithInitialObservation(Umbrella.T, candidates, emissionLogProbabilities);
            Assert.False(viterbi.IsBroken());

            var transitionLogProbabilities = new Dictionary<Transition<Rain>, double>
            {
                { new Transition<Rain>(Rain.T, Rain.T), Log(0.5) },
                { new Transition<Rain>(Rain.T, Rain.F), Log(0.5) },
                { new Transition<Rain>(Rain.F, Rain.T), Log(0.5) },
                { new Transition<Rain>(Rain.F, Rain.F), Log(0.5) }
            };
            viterbi.NextStep(Umbrella.T, candidates, emissionLogProbabilities, transitionLogProbabilities);
            Assert.False(viterbi.IsBroken());

            transitionLogProbabilities = new Dictionary<Transition<Rain>, double>
            {
                { new Transition<Rain>(Rain.T, Rain.T), Log(0.0) },
                { new Transition<Rain>(Rain.T, Rain.F), Log(0.0) },
                { new Transition<Rain>(Rain.F, Rain.T), Log(0.0) },
                { new Transition<Rain>(Rain.F, Rain.F), Log(0.0) }
            };
            viterbi.NextStep(Umbrella.T, candidates, emissionLogProbabilities, transitionLogProbabilities);
            Assert.True(viterbi.IsBroken());
            Assert.Equal(new List<Rain> { Rain.T, Rain.T }, States(viterbi.ComputeMostLikelySequence()));
        }

        [Fact]
        public void TestDeterministicCandidateOrder()
        {
            var candidates = new List<Rain> { Rain.T, Rain.F };

            // Reverse usual order of emission and transition probabilities keys
            var emissionLogProbabilitiesForUmbrella = new Dictionary<Rain, double>
            {
                { Rain.F, Log(0.5) },
                { Rain.T, Log(0.5) }
            };

            var emissionLogProbabilitiesForNoUmbrella = new Dictionary<Rain, double>
            {
                { Rain.F, Log(0.5) },
                { Rain.T, Log(0.5) }
            };

            var transitionLogProbabilities = new Dictionary<Transition<Rain>, double>
            {
                { new Transition<Rain>(Rain.F, Rain.T), Log(0.5) },
                { new Transition<Rain>(Rain.F, Rain.F), Log(0.5) },
                { new Transition<Rain>(Rain.T, Rain.T), Log(0.5) },
                { new Transition<Rain>(Rain.T, Rain.F), Log(0.5) }
            };

            var viterbi = new ViterbiAlgorithm<Rain, Umbrella, Descriptor>();
            viterbi.StartWithInitialObservation(Umbrella.T, candidates, emissionLogProbabilitiesForUmbrella);
            viterbi.NextStep(Umbrella.T, candidates, emissionLogProbabilitiesForUmbrella, transitionLogProbabilities);
            viterbi.NextStep(Umbrella.F, candidates, emissionLogProbabilitiesForNoUmbrella, transitionLogProbabilities);
            viterbi.NextStep(Umbrella.T, candidates, emissionLogProbabilitiesForUmbrella, transitionLogProbabilities);

            var result = viterbi.ComputeMostLikelySequence();
            Assert.Equal(4, result.Count);
            Assert.Equal(Rain.T, result[0].State);
            Assert.Equal(Rain.T, result[1].State);
            Assert.Equal(Rain.T, result[2].State);
            Assert.Equal(Rain.T, result[3].State);
        }
    }
}