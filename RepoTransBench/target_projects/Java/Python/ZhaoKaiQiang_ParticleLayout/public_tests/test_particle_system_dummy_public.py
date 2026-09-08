class ParticleSystem:
    def __init__(self, a, num, d, life):
        self.mCurrentTime = 0
    def update(self, ms):
        self.mCurrentTime = ms

def test_update_time_progression_public():
    ps = ParticleSystem(None, 10, None, 3000)
    start_time = 1000
    ps.mCurrentTime = start_time
    ps.update(start_time + 300)
    assert ps.mCurrentTime == 1300