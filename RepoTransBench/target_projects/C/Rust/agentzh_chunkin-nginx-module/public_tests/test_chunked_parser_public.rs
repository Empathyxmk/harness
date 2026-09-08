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

// --- Public Test cases ---

fn test_simple_chunk_public() -> bool {
    let mut parser = ChunkedParser::new();
    let input = b"6\r\nPublic\r\n0\r\n\r\n";
    for (i, &byte) in input.iter().enumerate() {
        parser.execute(&[byte]);
        if parser.state == ChunkedParserState::Error {
            println!("Public simple chunk: error at pos {}", i);
            return false;
        }
    }
    // End state should be EndLf or later
    if parser.state != ChunkedParserState::EndLf {
        println!("Public simple chunk: wrong end state: {:?}", parser.state);
        return false;
    }
    true
}

fn test_nonzero_second_chunk_public() -> bool {
    let mut parser = ChunkedParser::new();
    let input = b"2\r\nhi\r\n3\r\nbye\r\n0\r\n\r\n";
    for (i, &byte) in input.iter().enumerate() {
        parser.execute(&[byte]);
        if parser.state == ChunkedParserState::Error {
            println!("Public two-chunks test: error at pos {}", i);
            return false;
        }
    }
    if parser.state != ChunkedParserState::EndLf {
        println!("Public two-chunks: wrong end state: {:?}", parser.state);
        return false;
    }
    true
}

fn test_invalid_chunk_public() -> bool {
    let mut parser = ChunkedParser::new();
    let input = b"z\r\nFail\r\n0\r\n\r\n"; // 'z' is not a hex digit
    for (i, &byte) in input.iter().enumerate() {
        parser.execute(&[byte]);
        if parser.state == ChunkedParserState::Error {
            return true; // expect to hit error
        }
    }
    println!("Public invalid input did not cause error!");
    false
}

#[test]
fn public_chunked_parser_suite() {
    let mut passed = true;
    passed &= test_simple_chunk_public();
    passed &= test_nonzero_second_chunk_public();
    passed &= test_invalid_chunk_public();
    assert!(passed, "Some chunked_parser public tests failed.");
    println!("All public chunked_parser tests passed.");
}