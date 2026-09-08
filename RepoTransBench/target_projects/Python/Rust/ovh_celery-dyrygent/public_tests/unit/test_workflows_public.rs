use crate::workflows::{Workflow, WorkflowNode, WorkflowException};

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;
    use serde_json::json;

    #[test]
    fn test_workflow_can_be_initialized_public() {
        let def = json!({
            "name": "public_wf",
            "nodes": [{"id": 100, "kind": "start"}]
        });
        let wf = Workflow::new(def.as_object().unwrap().clone());
        assert_eq!(wf.definition.get("name").unwrap(), "public_wf");
    }

    #[test]
    fn test_workflownode_attribute_assignment_public() {
        let node_def = json!({"id": 57, "kind": "special", "attr": "xyz"});
        let node = WorkflowNode::new(&node_def);
        assert_eq!(node.kind.as_deref(), Some("special"));
        assert_eq!(node.attr.as_deref(), Some("xyz"));
        assert_eq!(node.id, 57);
    }

    #[test]
    fn test_workflow_exception_message_public() {
        let err = WorkflowException::new("public workflow error");
        assert!(err.to_string().contains("public"));
    }
}