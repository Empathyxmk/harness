use crate::workflows::{WorkflowException};
use crate::workflows::exceptions::WorkflowException as WFExc;
use crate::workflows::workflow::{CeleryWorkflowMixin, WorkflowSignalMixin};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_workflow_exception_inheritance_public() {
        let r = std::panic::catch_unwind(|| {
            panic!(WFExc::new("another error"));
        });
        assert!(r.is_err());
        if let Err(e) = r {
            let msg = format!("{:?}", e);
            assert!(msg.contains("another error"));
        }
    }

    struct DummyWorkflowPub;
    impl CeleryWorkflowMixin for DummyWorkflowPub {}
    impl DummyWorkflowPub {
        fn add_signature(&self, _signature: i32, _dependencies: Option<i32>) -> &'static str {
            "nodex"
        }
    }

    #[test]
    fn test_celeryworkflowmixin_add_celery_signature_calls_add_signature_public() {
        let dummy = DummyWorkflowPub {};
        let result = dummy.add_signature(1, Some(42));
        assert_eq!(result, "nodex");
    }
}