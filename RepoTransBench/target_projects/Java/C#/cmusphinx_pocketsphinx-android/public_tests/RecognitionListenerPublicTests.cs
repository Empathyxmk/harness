using Xunit;
using PocketSphinx;
using System;

namespace PocketSphinxTests.Public
{
    public class RecognitionListenerPublicTests
    {
        private class CallbackCounter : RecognitionListener
        {
            public int ready, begin, end, partial, result, error, timeout;
            public void OnReadyForSpeech() { ready++; }
            public void OnBeginningOfSpeech() { begin++; }
            public void OnEndOfSpeech() { end++; }
            public void OnPartialResult(Hypothesis hypothesis) { partial++; }
            public void OnResult(Hypothesis hypothesis) { result++; }
            public void OnError(Exception e) { error++; }
            public void OnTimeout() { timeout++; }
        }

        [Fact]
        public void TestListenerMethodsWithDifferentData()
        {
            var cc = new CallbackCounter();
            cc.OnReadyForSpeech();
            cc.OnReadyForSpeech(); // Call twice
            cc.OnBeginningOfSpeech();
            cc.OnPartialResult(new Hypothesis("different_partial", 100));
            cc.OnEndOfSpeech();
            cc.OnEndOfSpeech(); // Call twice
            cc.OnResult(new Hypothesis("different_result", 99));
            cc.OnResult(new Hypothesis("result_again", -5));
            cc.OnError(new Exception("different_fail"));
            cc.OnError(new Exception("another_fail"));
            cc.OnTimeout();
            cc.OnTimeout(); // Call twice

            Assert.Equal(2, cc.ready);
            Assert.Equal(1, cc.begin);
            Assert.Equal(2, cc.end);
            Assert.Equal(1, cc.partial);
            Assert.Equal(2, cc.result);
            Assert.Equal(2, cc.error);
            Assert.Equal(2, cc.timeout);
        }
    }
}