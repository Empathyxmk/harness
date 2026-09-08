using System;
using System.Collections.Generic;
using Xunit;
using BmwcaritHmmLib;

namespace OriginalTests
{
    public class ForwardBackwardAlgorithmTest
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

        [Fact]
        public void TestForwardBackward()
        {
            var candidates = new List<Rain> { Rain.T, Rain.F };

            var initialStateProbabilities = new Dictionary<Rain, double>
            {
                { Rain.T, 0.5 },
                { Rain.F, 0.5 }
            };

            var emissionProbabilitiesForUmbrella = new Dictionary<Rain, double>
            {
                { Rain.T, 0.9 },
                { Rain.F, 0.2 }
            };

            var emissionProbabilitiesForNoUmbrella = new Dictionary<Rain, double>
            {
                { Rain.T, 0.1 },
                { Rain.F, 0.8 }
            };

            var transitionProbabilities = new Dictionary<Transition<Rain>, double>
            {
                { new Transition<Rain>(Rain.T, Rain.T), 0.7 },
                { new Transition<Rain>(Rain.T, Rain.F), 0.3 },
                { new Transition<Rain>(Rain.F, Rain.T), 0.3 },
                { new Transition<Rain>(Rain.F, Rain.F), 0.7 }
            };

            var fw = new ForwardBackwardAlgorithm<Rain, Umbrella>();
            fw.StartWithInitialStateProbabilities(candidates, initialStateProbabilities);
            fw.NextStep(Umbrella.T, candidates, emissionProbabilitiesForUmbrella, transitionProbabilities);
            fw.NextStep(Umbrella.T, candidates, emissionProbabilitiesForUmbrella, transitionProbabilities);
            fw.NextStep(Umbrella.F, candidates, emissionProbabilitiesForNoUmbrella, transitionProbabilities);
            fw.NextStep(Umbrella.T, candidates, emissionProbabilitiesForUmbrella, transitionProbabilities);
            fw.NextStep(Umbrella.T, candidates, emissionProbabilitiesForUmbrella, transitionProbabilities);

            var result = fw.ComputeSmoothingProbabilities();
            Assert.Equal(6, result.Count);

            double DELTA = 1e-4;
            Assert.Equal(0.6469, result[0][Rain.T], 4);
            Assert.Equal(0.3531, result[0][Rain.F], 4);
            Assert.Equal(0.8673, result[1][Rain.T], 4);
            Assert.Equal(0.1327, result[1][Rain.F], 4);
            Assert.Equal(0.8204, result[2][Rain.T], 4);
            Assert.Equal(0.1796, result[2][Rain.F], 4);
            Assert.Equal(0.3075, result[3][Rain.T], 4);
            Assert.Equal(0.6925, result[3][Rain.F], 4);
            Assert.Equal(0.8204, result[4][Rain.T], 4);
            Assert.Equal(0.1796, result[4][Rain.F], 4);
            Assert.Equal(0.8673, result[5][Rain.T], 4);
            Assert.Equal(0.1327, result[5][Rain.F], 4);
        }
    }
}