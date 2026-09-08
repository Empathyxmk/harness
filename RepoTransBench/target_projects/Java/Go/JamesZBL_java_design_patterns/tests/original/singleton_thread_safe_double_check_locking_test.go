package original

import "jameszbl_java_design_patterns/singleton"
import "testing"

func TestThreadSafeDoubleCheckLockingSingleton(t *testing.T) {
	singletonTestSuite(t, singleton.GetThreadSafeDoubleCheckLockingInstance)
}