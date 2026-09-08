package original

import (
	"testing"

	"jameszbl_java_design_patterns/bridge"
)

func TestAncientWar(t *testing.T) {
	enemy := &bridge.MockIntrepidEnemy{}
	war := bridge.NewAncientWar(enemy)
	testWarEvents(t, war, enemy)
}