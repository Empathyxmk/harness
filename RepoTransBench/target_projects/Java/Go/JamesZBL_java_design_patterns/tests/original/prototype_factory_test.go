package original

import (
	"testing"

	"jameszbl_java_design_patterns/prototype"
)

func TestFactoryCreateDriverPassengerVehicle(t *testing.T) {
	driver := &prototype.MockDriver{}
	passenger := &prototype.MockPassenger{}
	vehicle := &prototype.MockVehicle{}

	driver.ShouldErrorOnClone = true
	passenger.ShouldErrorOnClone = true
	vehicle.ShouldErrorOnClone = true

	factory := prototype.NewTeamFactoryImpl(driver, passenger, vehicle)
	if got := factory.CreateDriver(); got != nil {
		t.Error("expected nil driver when clone error")
	}
	if got := factory.CreatePassenger(); got != nil {
		t.Error("expected nil passenger when clone error")
	}
	if got := factory.CreateVehicle(); got != nil {
		t.Error("expected nil vehicle when clone error")
	}

	if !driver.CalledClone {
		t.Error("expected driver.Clone() to be called")
	}
	if !passenger.CalledClone {
		t.Error("expected passenger.Clone() to be called")
	}
	if !vehicle.CalledClone {
		t.Error("expected vehicle.Clone() to be called")
	}
}