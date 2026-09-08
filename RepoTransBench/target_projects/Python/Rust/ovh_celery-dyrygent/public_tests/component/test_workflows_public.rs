use crate::workflows::workflow::WorkflowSignalMixin;

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_connect_and_emit_public() {
        struct MyWF;
        impl WorkflowSignalMixin for MyWF {}
        let w = MyWF;
        // Just smoke test; in real code you'd test hook/emit behavior with side effects.
        w.emit("on_custom", Some(&serde_json::json!(1001)));
    }
}