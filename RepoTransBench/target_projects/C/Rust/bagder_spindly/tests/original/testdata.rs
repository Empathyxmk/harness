// The C project defines these as string literals, but we'll use byte arrays in Rust
// NOTE: These would normally be loaded from actual data, but since we don't have access
// to the original binary data, we're defining empty placeholders

pub static TEST_CONTROL_SYN_STREAM_FRAME: &[u8] = &[];
pub static TEST_CONTROL_SYN_REPLY_FRAME: &[u8] = &[];
pub static TEST_CONTROL_RST_STREAM_FRAME: &[u8] = &[];
pub static TEST_DATA_FRAME_HEADER: &[u8] = &[];
pub static TEST_DATA_FRAME: &[u8] = &[];
pub static TEST_NV_BLOCK: &[u8] = &[];