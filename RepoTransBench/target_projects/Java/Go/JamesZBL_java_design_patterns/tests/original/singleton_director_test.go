package original

import "jameszbl_java_design_patterns/singleton"
import "testing"

func TestDirectorSingleton(t *testing.T) {
	singletonTestSuite(t, singleton.GetDirectorInstance)
}