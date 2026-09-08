using Xunit;
using PocketSphinx;
using System;

namespace PocketSphinxTests.Original
{
    public class RecognitionListenerTests
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
        public void TestListenerMethods()
        {
            var cc = new CallbackCounter();
            cc.OnReadyForSpeech();
            cc.OnBeginningOfSpeech();
            cc.OnEndOfSpeech();
            cc.OnPartialResult(new Hypothesis("foo", 10));
            cc.OnResult(new Hypothesis("bar", 9));
            cc.OnError(new Exception("fail"));
            cc.OnTimeout();

            Assert.Equal(1, cc.ready);
            Assert.Equal(1, cc.begin);
            Assert.Equal(1, cc.end);
            Assert.Equal(1, cc.partial);
            Assert.Equal(1, cc.result);
            Assert.Equal(1, cc.error);
            Assert.Equal(1, cc.timeout);
        }
    }
}