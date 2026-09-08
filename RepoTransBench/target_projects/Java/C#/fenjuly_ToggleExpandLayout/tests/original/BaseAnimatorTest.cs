using Xunit;
using Moq;
using Fenjuly.ToggleExpandLayout;
using System;

namespace Fenjuly.ToggleExpandLayout.Tests.Original
{
    public class BaseAnimatorTest
    {
        private class TestAnimator : BaseAnimator
        {
            public bool Prepared { get; set; }
            protected override void Prepare(View target)
            {
                Prepared = true;
            }
        }

        private TestAnimator animator;

        public BaseAnimatorTest()
        {
            animator = new TestAnimator();
        }

        [Fact]
        public void TestDefaultDuration()
        {
            Assert.Equal(BaseAnimator.DURATION, animator.GetDuration());
        }

        [Fact]
        public void TestSetAnimatorSet()
        {
            var set = new AnimatorSet();
            animator.SetAnimatorSet(set);
            Assert.Equal(set, animator.GetAnimatorSet());
        }

        [Fact]
        public void TestSetGetDuration()
        {
            animator.SetDuration(500);
            Assert.Equal(500, animator.GetDuration());
        }

        [Fact]
        public void TestPrepareAndAnimate()
        {
            var view = new Mock<View>().Object;
            animator.Prepared = false;
            animator.Animate(view);
            Assert.True(animator.Prepared);
        }

        [Fact]
        public void TestAddAnimatorListener_andStart()
        {
            var listener = Mock.Of<Animator.IAnimatorListener>();
            animator.AddAnimatorListener(listener);
            animator.Start();
        }
    }
}