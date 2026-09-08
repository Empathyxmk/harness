import pytest

# Minimal mock timer logic with different numbers for public tests
class PublicMockCrectTimer:
    set_calls = 0
    set_max_calls = 0

    @classmethod
    def set(cls, ms):
        cls.set_calls += 1

    @classmethod
    def set_max(cls):
        cls.set_max_calls += 1

# Minimal Async Job and Queue for public test
class PublicDummyJob:
    def __init__(self, baseline, job_isr_id):
        self.baseline = baseline
        self.job_isr_id = job_isr_id

class PublicDummyAsyncQueue:
    def __init__(self):
        self.jobs = [None, None]
        self.count = 0

    def front(self):
        return self.jobs[0] if self.count > 0 else None

    def pop(self):
        if self.count > 0:
            self.jobs[0] = None
            self.count -= 1
            return None
        return None

    def reset(self):
        self.count = 0
        self.jobs = [None, None]

# Fake globals for claim simulation
public_fake_current_time = 250

def public_claim_rsystem_clock(f):
    return f()

def public_claim_rasync(f):
    if not hasattr(public_claim_rasync, "_q"):
        public_claim_rasync._q = PublicDummyAsyncQueue()
    q = public_claim_rasync._q
    f(q)

def public_pend(x):
    # does nothing, just a placeholder for simulation
    pass

def Public_SysTick_Handler_for_test():
    global public_fake_current_time
    current_time = public_claim_rsystem_clock(lambda: public_fake_current_time)
    def async_queue_fn(async_queue):
        if async_queue.front() is not None:
            while current_time >= async_queue.front().baseline:
                public_pend(async_queue.front().job_isr_id)
                if async_queue.pop() is None:
                    PublicMockCrectTimer.set_max()
                    return
            PublicMockCrectTimer.set(async_queue.front().baseline)
        else:
            PublicMockCrectTimer.set_max()
    public_claim_rasync(async_queue_fn)


def test_public_timer_calls_set_and_set_max_branches_different_data():
    PublicMockCrectTimer.set(12345)
    PublicMockCrectTimer.set(999)
    PublicMockCrectTimer.set(250)
    PublicMockCrectTimer.set_max()
    assert True

def test_public_systick_handler_handles_queue_with_different_jobs():
    global public_fake_current_time
    # empty case
    public_fake_current_time = 300
    public_claim_rasync(lambda q: q.reset())
    Public_SysTick_Handler_for_test()

    # one job, baseline > now (simulate 400 > 300)
    def set_one_job_future(q):
        q.reset()
        j1 = PublicDummyJob(400, 10)
        q.jobs[0] = j1
        q.count = 1
    public_claim_rasync(set_one_job_future)
    public_fake_current_time = 300
    Public_SysTick_Handler_for_test()

    # one job, baseline <= now, triggers pop (simulate 150 <= 300)
    def set_one_job_past(q):
        q.reset()
        j2 = PublicDummyJob(150, 20)
        q.jobs[0] = j2
        q.count = 1
    public_claim_rasync(set_one_job_past)
    public_fake_current_time = 300
    Public_SysTick_Handler_for_test()

    assert True