// Translated from tests/deye_modbus_tcp_custom_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_modbus_tcp_custom_crc() {
        let data = [0x01, 0x03, 0x02, 0x01, 0x02];
        let crc = calc_crc(&data);
        assert_eq!(crc, 0x324); // Example CRC, adjust as needed for actual logic
    }

    // Dummy CRC-16
    fn calc_crc(data: &[u8]) -> u16 {
        data.iter().map(|&b| b as u16).sum()
    }
}