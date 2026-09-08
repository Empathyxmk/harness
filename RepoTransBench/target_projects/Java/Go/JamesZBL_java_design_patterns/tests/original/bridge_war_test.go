package original

import (
	"testing"
	"jameszbl_java_design_patterns/bridge"
)

// Helper reused by bridge_ancientwar_test.go, bridge_mordernwar_test.go
func testWarEvents(t *testing.T, war bridge.War, enemy *bridge.MockIntrepidEnemy) {
	if war == nil {
		t.Error("war must not be nil")
	}
	if war.GetEnemy() == nil {
		t.Error("war's enemy must not be nil")
	}
	war.StartWar()
	if !enemy.CalledStartWar {
		t.Error("enemy.onStartWar should be called")
	}
	war.Combatting()
	if !enemy.CalledCombatting {
		t.Error("enemy.onCombatting should be called")
	}
	war.StopWar()
	if !enemy.CalledStopWar {
		t.Error("enemy.onStopWar should be called")
	}
}