use crate::tasks;
use crate::workflows::Workflow;
use mockall::mock;

#[cfg(test)]
mod tests {
    use super::*;
    use mockall::{predicate::*, *};

    mock! {
        pub TaskObj {}
        impl TaskObj {
            pub fn retry(&self, kwargs: std::collections::HashMap<String, String>, countdown: i32) {}
            pub fn tick(&self) -> bool;
            pub fn to_dict(&self) -> std::collections::HashMap<String, String>;
            pub fn get_retry_countdown(&self) -> i32;
        }
    }

    mock! {
        pub Workflow {}
        impl Workflow {
            pub fn to_dict(&self) -> std::collections::HashMap<String, String>;
            pub fn get_retry_countdown(&self) -> i32;
            pub fn tick(&self) -> bool;
        }
    }

    #[test]
    fn test_workflow_processor_with_different_ids() {
        let mut task_obj = MockTaskObj::new();
        let mut wf = MockWorkflow::new();
        wf.expect_tick().return_const(false);
        wf.expect_to_dict().return_const(std::collections::HashMap::<String, String>::new());
        wf.expect_get_retry_countdown().return_const(123);
        tasks::workflow_processor(&mut task_obj, &mut wf);
    }
}