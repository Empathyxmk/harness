using Xunit;
using PocketSphinx;
using System;

namespace PocketSphinxTests.Original
{
    public class SpeechRecognizerTests
    {
        private class DummyListener : RecognitionListener
        {
            public bool ready = false;
            public void OnReadyForSpeech() { ready = true; }
            public void OnBeginningOfSpeech() { }
            public void OnEndOfSpeech() { }
            public void OnPartialResult(Hypothesis hypothesis) { }
            public void OnResult(Hypothesis hypothesis) { }
            public void OnError(Exception e) { }
            public void OnTimeout() { }
        }

        [Fact]
        public void TestAddAndRemoveListener()
        {
            var recognizer = new SpeechRecognizer();
            var l = new DummyListener();
            recognizer.AddListener(l);
            recognizer.RemoveListener(l);
            // Should not cause exceptions
        }

        [Fact]
        public void TestStartListeningFiresReady()
        {
            var recognizer = new SpeechRecognizer();
            var l = new DummyListener();
            recognizer.AddListener(l);
            recognizer.StartListening("search");
            Assert.True(l.ready);
        }

        [Fact]
        public void TestStopAndCancelNoErrors()
        {
            var recognizer = new SpeechRecognizer();
            recognizer.Stop();
            recognizer.Cancel();
            // Just for coverage, no state to assert
        }
    }
}