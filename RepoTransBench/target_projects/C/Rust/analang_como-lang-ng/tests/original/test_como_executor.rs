use analang_como_lang_ng::executor::*;

#[test]
fn test_opcode_handlers_table() {
    // Just call several handlers to confirm they are callable (do nothing, don't panic)
    for i in 0..crate::opcode::COMO_OPCODE_MAX {
        let h = COMO_OPCODE_HANDLER_TABLE[i];
        h(None, None, None);
    }
}