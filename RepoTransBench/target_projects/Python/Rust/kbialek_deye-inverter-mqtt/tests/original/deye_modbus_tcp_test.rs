// Translated from tests/deye_modbus_tcp_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_modbus_tcp_frame_formation() {
        let addr = 0x01u8;
        let func = 0x03u8;
        let reg = 0x0020u16;
        let length = 2u16;
        let request = form_modbus_tcp_frame(addr, func, reg, length);
        assert_eq!(request[0], addr);
        assert_eq!(request[1], func);
    }

    fn form_modbus_tcp_frame(addr: u8, func: u8, reg: u16, length: u16) -> Vec<u8> {
        let mut frame = Vec::new();
        frame.push(addr);
        frame.push(func);
        frame.push((reg >> 8) as u8);
        frame.push((reg & 0xFF) as u8);
        frame.push((length >> 8) as u8);
        frame.push((length & 0xFF) as u8);
        frame
    }
}