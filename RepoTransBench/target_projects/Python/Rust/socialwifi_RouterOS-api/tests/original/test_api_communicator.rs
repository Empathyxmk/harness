use mockall::{automock, mock, predicate::*};
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

#[derive(Debug, Clone, PartialEq)]
pub struct RouterOsApiCommunicationError;

pub struct DummyBase {
    pub receive_sentence: Rc<RefCell<Vec<Vec<Vec<u8>>>>>,
    pub send_sentences: Rc<RefCell<Vec<Vec<Vec<u8>>>>>,
}

impl DummyBase {
    pub fn new() -> Self {
        Self {
            receive_sentence: Rc::new(RefCell::new(vec![])),
            send_sentences: Rc::new(RefCell::new(vec![])),
        }
    }
    pub fn receive_sentence_once(&self) -> Vec<Vec<u8>> {
        self.receive_sentence.borrow_mut().remove(0)
    }
    pub fn send_sentence(&self, sentence: Vec<Vec<u8>>) {
        self.send_sentences.borrow_mut().push(sentence);
    }
}

// We will stub ApiCommunicator as very simple for test, not as full feature.
pub struct ApiCommunicator {
    base: Rc<DummyBase>,
}

impl ApiCommunicator {
    pub fn new(base: Rc<DummyBase>) -> Self {
        Self { base }
    }
    pub fn call(&self, _path: &str, _action: &str) -> CommunicatorResult {
        // In actual code, implement call logic.
        CommunicatorResult {
            result: self.base.receive_sentence_once(),
        }
    }
    pub fn call_with_args(&self, _path: &str, _action: &str, _args: Option<HashMap<&str, &str>>) -> CommunicatorResult {
        // Only for demonstration purpose
        self.base.send_sentence(vec![]);
        CommunicatorResult { result: vec![] }
    }
}

pub struct CommunicatorResult {
    pub result: Vec<Vec<u8>>,
}

impl CommunicatorResult {
    pub fn get(&self) -> Vec<HashMap<String, Vec<u8>>> {
        // Simulate the parsing into HashMap, stub test logic
        // For the actual logic, would parse 'result' member.
        vec![]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_login_call() {
        let base = Rc::new(DummyBase::new());
        base.receive_sentence.borrow_mut().push(vec![
            b"!done".to_vec(),
            b"=ret=some-hex".to_vec(),
            b".tag=1".to_vec()
        ]);
        let communicator = ApiCommunicator::new(base.clone());
        let response = communicator.call("/", "login");
        let result = response.result;
        // In Python, response.done_message['ret'] == b'some-hex'
        assert_eq!(result[1], b"=ret=some-hex".to_vec());
    }
    // Remaining tests would follow the same pattern:
    // - Setup mock base responses
    // - Call communicator
    // - Assert on results or that Error is returned where needed

    // ... etc. (see rest of ported suite)
}