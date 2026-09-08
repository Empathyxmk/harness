using System;
using System.Collections.Generic;
using Xunit;
using BmwcaritHmmLib;

namespace PublicTests
{
    public class ForwardBackwardAlgorithmPublicTest
    {
        private class CoinState
        {
            public static readonly CoinState H = new CoinState();
            public static readonly CoinState T = new CoinState();

            public override string ToString()
            {
                if (ReferenceEquals(this, H)) return "Heads";
                if (ReferenceEquals(this, T)) return "Tails";
                throw new InvalidOperationException();
            }
        }

        private class FlipEvent
        {
            public static readonly FlipEvent YES = new FlipEvent();
            public static readonly FlipEvent NO = new FlipEvent();

            public override string ToString()
            {
                if (ReferenceEquals(this, YES)) return "CoinFlip";
                if (ReferenceEquals(this, NO)) return "NoCoinFlip";
                throw new InvalidOperationException();
            }
        }

        [Fact]
        public void TestForwardBackwardPublic()
        {
            var candidates = new List<CoinState> { CoinState.H, CoinState.T };

            var initialStateProbabilities = new Dictionary<CoinState, double>
            {
                { CoinState.H, 0.6 },
                { CoinState.T, 0.4 }
            };

            var emissionProbabilitiesFlip = new Dictionary<CoinState, double>
            {
                { CoinState.H, 0.8 },
                { CoinState.T, 0.3 }
            };

            var emissionProbabilitiesNoFlip = new Dictionary<CoinState, double>
            {
                { CoinState.H, 0.2 },
                { CoinState.T, 0.7 }
            };

            var transitionProbabilities = new Dictionary<Transition<CoinState>, double>
            {
                { new Transition<CoinState>(CoinState.H, CoinState.H), 0.6 },
                { new Transition<CoinState>(CoinState.H, CoinState.T), 0.4 },
                { new Transition<CoinState>(CoinState.T, CoinState.H), 0.5 },
                { new Transition<CoinState>(CoinState.T, CoinState.T), 0.5 }
            };

            var fw = new ForwardBackwardAlgorithm<CoinState, FlipEvent>();
            fw.StartWithInitialStateProbabilities(candidates, initialStateProbabilities);
            fw.NextStep(FlipEvent.YES, candidates, emissionProbabilitiesFlip, transitionProbabilities);
            fw.NextStep(FlipEvent.NO, candidates, emissionProbabilitiesNoFlip, transitionProbabilities);
            fw.NextStep(FlipEvent.YES, candidates, emissionProbabilitiesFlip, transitionProbabilities);

            var result = fw.ComputeSmoothingProbabilities();
            Assert.Equal(4, result.Count);
            double DELTA = 1e-4;
            Assert.Equal(0.7315, result[0][CoinState.H], 4);
            Assert.Equal(0.2685, result[0][CoinState.T], 4);
            Assert.Equal(0.5732, result[1][CoinState.H], 4);
            Assert.Equal(0.4268, result[1][CoinState.T], 4);
            Assert.Equal(0.4575, result[2][CoinState.H], 4);
            Assert.Equal(0.5425, result[2][CoinState.T], 4);
            Assert.Equal(0.6586, result[3][CoinState.H], 4);
            Assert.Equal(0.3414, result[3][CoinState.T], 4);
        }
    }
}