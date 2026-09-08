#[cfg(test)]
mod tests {
    use super::super::super::src::execution_plan::*;
    #[test]
    fn test_profile_stats_fields() {
        let ps = ProfileStats::new(10, 1.23);
        assert_eq!(ps.records_produced, 10);
        assert_eq!(ps.execution_time, 1.23);
    }

    #[test]
    fn test_operation_eq_and_str() {
        let op1 = Operation::new("Filter");
        let op2 = Operation::new("Filter");
        let op3 = Operation::new("Scan");
        let mut op4 = Operation::new("Filter");
        op4.args = Some("x > 1".to_string());
        assert_eq!(op1, op2);
        assert_ne!(op1, op3);
        assert_ne!(op1, op4);
        assert_eq!(op1.to_string(), "Filter");
        assert_eq!(op4.to_string(), "Filter | x > 1");
    }

    #[test]
    fn test_operation_append_and_child_count() {
        let mut op = Operation::new("Root");
        let child = Operation::new("Child");
        op.append_child(child.clone());
        assert_eq!(op.child_count(), 1);
        // Since Rust uses ownership, we check existence
        assert_eq!(op.children[0].name, "Child");
        // For error cases, we cannot append self
        let result = std::panic::catch_unwind(|| { op.append_child(op.clone()); });
        assert!(result.is_err());
    }

    #[test]
    fn test_execution_plan_eq_and_str_patch_tree() {
        let root = Operation::new("Root").append_child(Operation::new("Child")).clone();
        let plan1 = ExecutionPlan::new(vec![], Some(root.clone()));
        let plan2 = ExecutionPlan::new(vec![], Some(root.clone()));
        assert_eq!(plan1, plan1.clone());
        assert_eq!(plan1, plan2);

        let diff_root = Operation::new("DifferentRoot");
        let plan3 = ExecutionPlan::new(vec![], Some(diff_root));
        assert_ne!(plan1, plan3);
        assert_eq!(format!("{}", plan1), "Root");
    }

    #[test]
    fn test_operation_traverse_manual_tree() {
        fn traverse(op: &Operation) -> String {
            let mut s = op.name.clone();
            if !op.children.is_empty() {
                s = format!("{}>{}", s, op.children.iter().map(|c| c.name.clone()).collect::<Vec<_>>().join(","));
            }
            s
        }
        let mut op = Operation::new("A");
        let opb = Operation::new("B");
        let opc = Operation::new("C");
        op.append_child(opb);
        op.append_child(opc);
        let s = traverse(&op);
        assert_eq!(s, "A>B,C");
    }
}