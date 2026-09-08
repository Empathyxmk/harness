#[cfg(test)]
mod tests {
    use super::*;
    use crate::VERSION;
    use crate::workflows;
    use crate::workflows::exceptions::WorkflowException;

    #[test]
    fn test_version_value() {
        // Equivalent to: assert VERSION == "0.8.0"
        assert_eq!(VERSION, "0.8.0");
    }

    #[test]
    fn test_workflows_all_exports() {
        use crate::workflows::{Workflow, WorkflowException, WorkflowNode};
        assert!(!format!("{:?}", std::any::type_name::<Workflow>()).is_empty());
        assert!(!format!("{:?}", std::any::type_name::<WorkflowNode>()).is_empty());
        assert!(!format!("{:?}", std::any::type_name::<WorkflowException>()).is_empty());
    }

    #[test]
    fn test_exception_is_exception() {
        let result = std::panic::catch_unwind(|| {
            panic!(WorkflowException::new("msg"));
        });
        assert!(result.is_err());
        if let Err(e) = result {
            let msg = format!("{:?}", e);
            assert!(msg.contains("msg"));
        }
    }
}