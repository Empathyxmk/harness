package original

import (
	"testing"

	"jameszbl_java_design_patterns/bridge"
)

func TestMordernWar(t *testing.T) {
	enemy := &bridge.MockIntrepidEnemy{}
	war := bridge.NewMordernWar(enemy)
	testWarEvents(t, war, enemy)
}