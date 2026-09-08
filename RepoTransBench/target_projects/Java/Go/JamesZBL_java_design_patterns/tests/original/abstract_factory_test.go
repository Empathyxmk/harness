package original

import "testing"
import "jameszbl_java_design_patterns/abstractfactory"

func TestAbstractFactoryCreateYoungTeam(t *testing.T) {
	app := abstractfactory.NewApplication()
	permanentFactory := abstractfactory.NewPermanentTeamFactory()
	youngFactory := abstractfactory.NewYoungTeamFactory()

	app.CreateTeam(youngFactory)
	ship := app.GetShip()
	captain := app.GetCaptain()
	sailor := app.GetSailor()

	if !ship.IsNewShip() {
		t.Errorf("ship not instance of NewShip")
	}
	if !captain.IsYoungCaptain() {
		t.Errorf("captain not instance of YoungCaptain")
	}
	if !sailor.IsYoungSailor() {
		t.Errorf("sailor not instance of YoungSailor")
	}

	if ship.Description() != abstractfactory.NewShipDescription {
		t.Errorf("ship description = %q, want %q", ship.Description(), abstractfactory.NewShipDescription)
	}
	if captain.Description() != abstractfactory.YoungCaptainDescription {
		t.Errorf("captain description = %q, want %q", captain.Description(), abstractfactory.YoungCaptainDescription)
	}
	if sailor.Description() != abstractfactory.YoungSailorDescription {
		t.Errorf("sailor description = %q, want %q", sailor.Description(), abstractfactory.YoungSailorDescription)
	}
}

func TestAbstractFactoryApplicationMain(t *testing.T) {
	abstractfactory.Main()
}