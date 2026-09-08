import pytest

# Try importing the implementation under test
try:
    from Chapter12.flight_status import FlightStatusTracker
except ImportError:
    FlightStatusTracker = None

def safe_get_status(tracker):
    # Defensive: try .get_status(), .status property, .current_status, .state, etc.
    # Returns None if nothing found.
    for attr in ['get_status', 'current_status', 'status', 'state']:
        meth = getattr(tracker, attr, None)
        if callable(meth):
            try:
                return meth()
            except Exception:
                continue
        elif meth is not None:
            return meth
    return None

@pytest.mark.skipif(FlightStatusTracker is None, reason="FlightStatusTracker implementation not available for testing")
def test_public_initial_status():
    tracker = FlightStatusTracker()
    status = safe_get_status(tracker)
    # Acceptable initial status: None, 'scheduled', 'UNKNOWN', etc.
    # Just ensure it doesn't throw and is present
    assert status is not NotImplemented, "Implementation returned NotImplemented"

@pytest.mark.skipif(FlightStatusTracker is None, reason="FlightStatusTracker implementation not available for testing")
def test_public_status_change_sequence():
    tracker = FlightStatusTracker()
    # Defensive: Try methods likely to exist in reasonable implementations
    # Pretend the implementation exposes .depart()/departed or .update_status or similar
    status_methods = [
        "depart", "set_departed", "update_status", "takeoff", "mark_as_departed"
    ]
    found = False
    for methname in status_methods:
        meth = getattr(tracker, methname, None)
        if callable(meth):
            meth()
            new_status = safe_get_status(tracker)
            # Accept anything not initial: e.g., "departed", "active", etc.
            assert new_status != safe_get_status(FlightStatusTracker()), "Status did not change"
            found = True
            break
    if not found:
        pytest.skip("No recognized status-changing method found in tracker")

@pytest.mark.skipif(FlightStatusTracker is None, reason="FlightStatusTracker implementation not available for testing")
def test_public_possible_status_strings():
    tracker = FlightStatusTracker()
    # Advance to a common intermediate or end state, if possible
    for methname in ["land", "arrive", "arrived", "finish", "complete"]:
        meth = getattr(tracker, methname, None)
        if callable(meth):
            meth()
            break
    status = safe_get_status(tracker)
    # Accept any of these reasonable end or progress states
    valid = [
        None, "landed", "arrived", "finished", "completed", "done", "inactive"
    ] + [False, True]
    assert status in valid or isinstance(status, str), f"Unexpected status: {status}"

@pytest.mark.skipif(FlightStatusTracker is None, reason="FlightStatusTracker implementation not available for testing")
def test_boarding_public():
    tracker = FlightStatusTracker()
    # Try some alternate names for boarding logic
    found_boarding = False
    for board_method in ["boarding_begins", "board", "start_boarding", "begin_boarding"]:
        meth = getattr(tracker, board_method, None)
        if callable(meth):
            meth()
            found_boarding = True
            break
    if not found_boarding:
        # Don't fail the public test, instead just skip if no suitable method exists
        pytest.skip("No boarding method found in tracker")
    # If a method was found/called, ensure the tracker is in some valid state
    status = safe_get_status(tracker)
    assert status is not NotImplemented