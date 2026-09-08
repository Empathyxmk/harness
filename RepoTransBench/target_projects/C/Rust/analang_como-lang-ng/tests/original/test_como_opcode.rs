use analang_como_lang_ng::opcode::*;

#[test]
fn test_instrstr_no_operand() {
    let op = ComoOpCode { op_code: OpCode::INone, operand: None };
    let s = instrstr(&op);
    assert!(s.starts_with("INONE "));
}

#[test]
fn test_instrstr_with_operand() {
    let dummy: usize = 0x112233;
    let op = ComoOpCode { op_code: OpCode::LoadConst, operand: Some(dummy) };
    let s = instrstr(&op);
    assert!(s.contains(&format!("LOAD_CONST OBJ")));
}