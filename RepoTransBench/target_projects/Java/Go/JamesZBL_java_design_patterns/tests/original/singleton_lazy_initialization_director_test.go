package original

import "jameszbl_java_design_patterns/singleton"
import "testing"

func TestLazyInitializationDirectorSingleton(t *testing.T) {
	singletonTestSuite(t, singleton.GetLazyInitializationDirectorInstance)
}