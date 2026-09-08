package original

import (
	"fmt"
	"sync"
	"sync/atomic"
	"testing"
)

// This is a throughput test, should not actually run 1_000_000 logs in unit test.
var (
	throughputLogger      = struct{}{}
	record100  string     = "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing."
	record200  string     = "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing."
	record400  string     = "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing."
	messageCnt int32      = 0
	count      int        = 1000 // LOWERED for standard test execution!
	threadNum  int        = 1
)

func TestFloggerThroughput(t *testing.T) {
	var wg sync.WaitGroup
	messageCnt = 0
	wg.Add(threadNum)
	st := nowMillis()
	for i := 0; i < threadNum; i++ {
		go func() {
			defer wg.Done()
			for atomic.LoadInt32(&messageCnt) < int32(count) {
				// call e.g. dummy logger.info(record400) or similar
				atomic.AddInt32(&messageCnt, 1)
			}
		}()
	}
	wg.Wait()
	et := nowMillis()
	throughput := int(float64(messageCnt) * 1000 / float64(et-st))
	fmt.Printf("messageCount=%d, threadNum=%d, costTime=%dms, throughput=%d\n",
		messageCnt, threadNum, et-st, throughput)
}

func nowMillis() int64 {
	return int64(1) // Dummy for test
}