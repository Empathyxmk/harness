package original

import (
	"fmt"
	"testing"
	"time"
)

func TestAccessSpeedLimitTest1(t *testing.T) {
	// Simulate: every 100ms, try to access a resource 5 times/second
	cnt := 0
	sec := 1
	limit := 5
	duration := time.Second
	start := time.Now()
	for time.Since(start) < duration {
		if cnt < limit {
			t.Logf("yes %v", time.Now().Format("04:05"))
			cnt++
		} else {
			t.Logf("no %v", time.Now().Format("04:05"))
		}
		time.Sleep(100 * time.Millisecond)
	}
}

func TestAccessSpeedLimitTest2(t *testing.T) {
	// every 100ms, try to access with lock after limit exceeded
	cnt := 0
	limit := 5
	lockCount := 7
	lockTime := 2 // seconds
	seconds := 1
	duration := 3 * time.Second

	start := time.Now()
	lockStart := time.Time{}
	lockHold := false
	for time.Since(start) < duration {
		now := time.Now()
		elapsed := now.Sub(start).Seconds()
		if lockHold {
			if now.Sub(lockStart).Seconds() > float64(lockTime) {
				lockHold = false
				cnt = 0 // simulate unlock
			}
		}
		if !lockHold {
			if cnt < limit {
				t.Logf("yes %v", now.Format("04:05"))
				cnt++
			} else if cnt >= lockCount {
				lockHold = true
				lockStart = now
				t.Logf("no + lock engaged %v for %ds", now.Format("04:05"), lockTime)
			} else {
				t.Logf("no %v", now.Format("04:05"))
				cnt++
			}
		} else {
			t.Logf("no (locked) %v", now.Format("04:05"))
		}
		time.Sleep(100 * time.Millisecond)
	}
}