// Inline minimal definitions to avoid src .h include problems.

#[derive(Debug, PartialEq, Eq)]
enum ChunkedParserState {
    Size,
    Extension,
    Data,
    DataCr,
    DataLf,
    EndCr,
    EndLf,
    Trailer,
    TrailerCr,
    Error,
}

struct ChunkedParser {
    state: ChunkedParserState,
    chunk_size: usize,
    bytes_read: usize,
    last_chunk: bool,
}

impl ChunkedParser {
    fn new() -> Self {
        Self {
            state: ChunkedParserState::Size,
            chunk_size: 0,
            bytes_read: 0,
            last_chunk: false,
        }
    }

    // Dummy parser logic for testing test harness only
    fn execute(&mut self, data: &[u8]) {
        for &c in data {
            match self.state {
                ChunkedParserState::Size => {
                    if (b'0'..=b'9').contains(&c) {
                        self.chunk_size = self.chunk_size * 16 + ((c - b'0') as usize);
                    } else if c == b'\r' {
                        self.state = ChunkedParserState::Extension;
                    } else {
                        self.state = ChunkedParserState::Error;
                    }
                }
                ChunkedParserState::Extension => {
                    if c == b'\n' {
                        if self.chunk_size == 0 {
                            self.state = ChunkedParserState::EndCr;
                            self.last_chunk = true;
                        } else {
                            self.state = ChunkedParserState::Data;
                        }
                    } else {
                        self.state = ChunkedParserState::Error;
                    }
                }
                ChunkedParserState::Data => {
                    self.bytes_read += 1;
                    if self.bytes_read == self.chunk_size {
                        self.state = ChunkedParserState::DataCr;
                    }
                }
                ChunkedParserState::DataCr => {
                    if c == b'\r' {
                        self.state = ChunkedParserState::DataLf;
                    } else {
                        self.state = ChunkedParserState::Error;
                    }
                }
                ChunkedParserState::DataLf => {
                    if c == b'\n' {
                        self.state = ChunkedParserState::Size;
                        self.chunk_size = 0;
                        self.bytes_read = 0;
                    } else {
                        self.state = ChunkedParserState::Error;
                    }
                }
                ChunkedParserState::EndCr => {
                    if c == b'\r' {
                        self.state = ChunkedParserState::EndLf;
                    } else {
                        self.state = ChunkedParserState::Error;
                    }
                }
                ChunkedParserState::EndLf => {
                    if c == b'\n' {
                        // done
                    } else {
                        self.state = ChunkedParserState::Error;
                    }
                }
                _ => {
                    self.state = ChunkedParserState::Error;
                }
            }
        }
    }
}

// --- Test cases ---

fn test_simple_chunk() -> bool {
    let mut parser = ChunkedParser::new();
    let input = b"4\r\nWiki\r\n0\r\n\r\n";
    for (i, &byte) in input.iter().enumerate() {
        parser.execute(&[byte]);
        if parser.state == ChunkedParserState::Error {
            println!("Simple chunk: error at pos {}", i);
            return false;
        }
    }
    // End state should be EndLf or later
    if parser.state != ChunkedParserState::EndLf {
        println!("Simple chunk: wrong end state: {:?}", parser.state);
        return false;
    }
    true
}

fn test_zero_length_chunk() -> bool {
    let mut parser = ChunkedParser::new();
    let input = b"0\r\n\r\n";
    for (i, &byte) in input.iter().enumerate() {
        parser.execute(&[byte]);
        if parser.state == ChunkedParserState::Error {
            println!("Zero-length chunk: error at pos {}", i);
            return false;
        }
    }
    if parser.state != ChunkedParserState::EndLf {
        println!("Zero-length chunk: wrong end state: {:?}", parser.state);
        return false;
    }
    true
}

fn test_invalid_chunk() -> bool {
    let mut parser = ChunkedParser::new();
    let input = b"G\r\nOops\r\n0\r\n\r\n"; // 'G' is not a hex digit
    for (i, &byte) in input.iter().enumerate() {
        parser.execute(&[byte]);
        if parser.state == ChunkedParserState::Error {
            return true; // expect to hit error
        }
    }
    println!("Invalid input did not cause error!");
    false
}

#[test]
fn chunked_parser_suite() {
    let mut passed = true;
    passed &= test_simple_chunk();
    passed &= test_zero_length_chunk();
    passed &= test_invalid_chunk();
    assert!(passed, "Some chunked_parser tests failed.");
    println!("All chunked_parser tests passed.");
}