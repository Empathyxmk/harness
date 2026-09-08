use analang_como_lang_ng::executor::*;
use analang_como_lang_ng::opcode::OpCode;

#[test]
fn test_handler_table_public() {
    assert_ne!(crate::executor::COMO_OPCODE_HANDLER_TABLE[OpCode::IAdd as usize] as usize, 0);
    assert_ne!(crate::executor::COMO_OPCODE_HANDLER_TABLE[OpCode::IDiv as usize] as usize, 0);
    assert_ne!(crate::executor::COMO_OPCODE_HANDLER_TABLE[OpCode::JMP as usize] as usize, 0);
}