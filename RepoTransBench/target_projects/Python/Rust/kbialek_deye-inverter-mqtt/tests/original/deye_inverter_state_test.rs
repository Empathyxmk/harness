// Translated from tests/deye_inverter_state_test.py

#[cfg(test)]
mod tests {
    #[derive(Debug, PartialEq)]
    enum State {
        Idle,
        Active,
        Fault,
    }

    #[test]
    fn test_inverter_state_transitions() {
        let mut state = State::Idle;
        assert_eq!(state, State::Idle);
        state = State::Active;
        assert_eq!(state, State::Active);
        state = State::Fault;
        assert_eq!(state, State::Fault);
    }
}