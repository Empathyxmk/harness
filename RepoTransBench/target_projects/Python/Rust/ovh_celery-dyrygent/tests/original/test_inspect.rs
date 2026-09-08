#[cfg(test)]
mod tests {
    use super::*;
    use crate::celery::entities::{AsyncResult, WorkerLostError};
    use crate::celery::inspect::{ResultState, ResultStateType};

    #[test]
    fn test_result_state_success() {
        let dummy_result = AsyncResult::new();
        let state = ResultState::new(&dummy_result);
        assert!(state.success);
        assert!(state.is_successful());
    }

    #[test]
    fn test_is_done_and_is_final() {
        let dummy_result = AsyncResult::new();
        let mut state = ResultState::new(&dummy_result);
        state.state = ResultStateType::DONE;
        assert!(state.is_done());
        assert!(state.is_final());
        state.state = ResultStateType::RUNNING;
        assert!(!state.is_final());
    }

    #[test]
    fn test_needs_reschedule_logic() {
        let dummy_result = AsyncResult::new();
        let mut state = ResultState::new(&dummy_result);
        state.state = ResultStateType::RESCHEDULE;
        assert!(state.needs_reschedule());
        state.state = ResultStateType::DONE;
        assert!(!state.needs_reschedule());
    }
}