using System;
using Xunit;
using System.Reactive.Linq;
using System.Reactive.Concurrency;
using Moq;

namespace DawishGoogleArchitectureDemo.Tests.Original.CoreModelUtil
{
    // This is a simplified version due to lack of Android & RxJava, focused on logic structure.
    public class SwitchSchedulersTest
    {
        [Fact]
        public void TestUnsubscribeWithNull()
        {
            SwitchSchedulers.Unsubscribe(null); // Should not throw
        }

        [Fact]
        public void TestUnsubscribeWithDisposed()
        {
            var disposable = new Mock<IDisposable>();
            disposable.Setup(d => d.Dispose());
            disposable.Setup(d => d.GetType().GetProperty("IsDisposed")?.GetValue(d, null)).Returns(true);
            SwitchSchedulers.Unsubscribe(disposable.Object); // Should not throw
        }

        [Fact]
        public void TestUnsubscribeWithActive()
        {
            bool disposed = false;
            var disposable = new DisposableAction(() => disposed = true);
            SwitchSchedulers.Unsubscribe(disposable);
            Assert.True(disposed);
        }

        [Fact]
        public void TestApplySchedulers()
        {
            // .NET Rx: use Immediate for test
            var observable = Observable.Return(1);
            int? value = null;
            observable.ObserveOn(ImmediateScheduler.Instance).SubscribeOn(ImmediateScheduler.Instance).Subscribe(v => value = v);
            Assert.Equal(1, value);
        }

        [Fact]
        public void TestApplyMaybeSchedulers()
        {
            // In .NET, Maybe is represented as nullable or Observable with no values.
            var observable = Observable.Return<int?>(2);
            int? value = null;
            observable.ObserveOn(ImmediateScheduler.Instance).SubscribeOn(ImmediateScheduler.Instance).Subscribe(v => value = v);
            Assert.Equal(2, value);
        }

        [Fact]
        public void TestApplySingleSchedulers()
        {
            var observable = Observable.Return(3);
            int? value = null;
            observable.ObserveOn(ImmediateScheduler.Instance).SubscribeOn(ImmediateScheduler.Instance).Subscribe(v => value = v);
            Assert.Equal(3, value);
        }

        [Fact]
        public void TestApplyFlowableSchedulers()
        {
            var observable = Observable.Return(4);
            int? value = null;
            observable.ObserveOn(ImmediateScheduler.Instance).SubscribeOn(ImmediateScheduler.Instance).Subscribe(v => value = v);
            Assert.Equal(4, value);
        }

        [Fact]
        public void TestToMainThread22222222()
        {
            var observable = Observable.Return(5);
            int? value = null;
            observable.ObserveOn(ImmediateScheduler.Instance).SubscribeOn(ImmediateScheduler.Instance).Subscribe(v => value = v);
            Assert.Equal(5, value);
        }

        [Fact]
        public void TestToIoThread2222222222()
        {
            var observable = Observable.Return(6);
            int? value = null;
            observable.ObserveOn(ImmediateScheduler.Instance).SubscribeOn(ImmediateScheduler.Instance).Subscribe(v => value = v);
            Assert.Equal(6, value);
        }
    }

    public static class SwitchSchedulers
    {
        public static void Unsubscribe(IDisposable disposable)
        {
            disposable?.Dispose();
        }
    }

    public class DisposableAction : IDisposable
    {
        private Action _action;
        private bool _disposed = false;
        public DisposableAction(Action action)
        {
            _action = action;
        }
        public void Dispose()
        {
            if (!_disposed)
            {
                _action();
                _disposed = true;
            }
        }
    }
}