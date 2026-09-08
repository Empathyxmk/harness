use analang_como_lang_ng::opcode::*;

#[test]
fn test_opcode_enum_public() {
    assert!(OpCode::LoadConst as i32 != OpCode::LoadName as i32);
    assert!(OpCode::IAdd as i32 != OpCode::ITimes as i32);
    assert!(OpCode::Label as i32 != OpCode::Halt as i32);
}

#[test]
fn test_opcode_max_public() {
    assert!(COMO_OPCODE_MAX > OpCode::Jz as usize);
    assert!(COMO_OPCODE_MAX > OpCode::IsNotEqual as usize);
}