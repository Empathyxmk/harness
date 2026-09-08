package original

import "jameszbl_java_design_patterns/singleton"
import "testing"

func TestThreadSafeLazyLoadDirectorSingleton(t *testing.T) {
	singletonTestSuite(t, singleton.GetThreadSafeLazyLoadDirectorInstance)
}