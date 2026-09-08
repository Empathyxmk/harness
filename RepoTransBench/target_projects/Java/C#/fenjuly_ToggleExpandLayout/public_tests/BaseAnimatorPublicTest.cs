using Xunit;
using Moq;
using Fenjuly.ToggleExpandLayout;

namespace Fenjuly.ToggleExpandLayout.Tests.Public
{
    public class BaseAnimatorPublicTest
    {
        private class DummyAnimator : BaseAnimator
        {
            public bool Prepared { get; set; }

            protected override void Prepare(View target)
            {
                Prepared = true;
            }
        }

        private DummyAnimator animator;
        private View target;

        public BaseAnimatorPublicTest()
        {
            animator = new DummyAnimator();
            target = new Mock<View>().Object;
        }

        [Fact]
        public void TestDurationsAreDifferentPublic()
        {
            Assert.Equal(BaseAnimator.DURATION, animator.GetDuration());
            animator.SetDuration(456);
            Assert.Equal(456, animator.GetDuration());
            animator.SetDuration(880);
            Assert.Equal(880, animator.GetDuration());
        }

        [Fact]
        public void TestAnimatorSetPublic()
        {
            var newSet = new AnimatorSet();
            animator.SetAnimatorSet(newSet);
            Assert.Equal(newSet, animator.GetAnimatorSet());
        }

        [Fact]
        public void TestAnimatePreparesPublic()
        {
            animator.Prepared = false;
            animator.Animate(target);
            Assert.True(animator.Prepared);
        }
    }
}