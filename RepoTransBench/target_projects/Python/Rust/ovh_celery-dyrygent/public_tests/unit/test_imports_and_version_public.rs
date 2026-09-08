use crate::VERSION;
use crate::workflows;
use crate::workflows::exceptions::WorkflowException;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version_value_public() {
        let parts: Vec<&str> = VERSION.split(".").collect();
        assert_eq!(parts, vec!["0", "8", "0"]);
    }

    #[test]
    fn test_workflows_all_exports_public() {
        use crate::workflows::{Workflow, WorkflowException, WorkflowNode};
        let t1 = std::any::type_name::<Workflow>();
        let t2 = std::any::type_name::<WorkflowNode>();
        assert!(!t1.is_empty());
        assert!(!t2.is_empty());
        // Ensure it is an error struct.
        assert!(std::any::type_name::<WorkflowException>().contains("WorkflowException"));
    }

    #[test]
    fn test_exception_is_exception_public() {
        let r = std::panic::catch_unwind(|| {
            panic!(WorkflowException::new("different message"));
        });
        assert!(r.is_err());
    }
}