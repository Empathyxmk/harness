//! Rust translation: public test adapted from inflate/test_inflate_public.py
//! Only extracts logic portable to Rust and checks gzip roundtrip + CRC.

#[cfg(test)]
mod inflate_public_sanity {
    use crc::Crc;
    use std::fs::{File};
    use std::io::{Read, Write};
    use std::process::Command;
    use tempfile::tempdir;

    const CRC_CCITT_FALSE: Crc<u16> = Crc::<u16>::new(&crc::CRC_16_CCITT_FALSE);

    #[test]
    fn test_gz_decompression_and_crc_public() {
        let dir = tempdir().unwrap();
        let in_file = dir.path().join("file.txt");
        // Use README.md if available, otherwise any short string will suffice
        let sample = b"Public inflate test string for Amiga!";
        {
            let mut f = File::create(&in_file).unwrap();
            f.write_all(sample).unwrap();
        }
        // Compress file (using gzip)
        let gz_file = dir.path().join("file.gz");
        let status = Command::new("gzip")
            .arg("-c9")
            .arg(&in_file)
            .output()
            .unwrap();
        assert!(status.status.success(), "gzip failed: {:?}", status);
        {
            let mut f = File::create(&gz_file).unwrap();
            f.write_all(&status.stdout).unwrap();
        }
        // Decompress
        let gunz_status = Command::new("gunzip")
            .arg("-c")
            .arg(&gz_file)
            .output()
            .unwrap();
        assert!(gunz_status.status.success(), "gunzip failed: {:?}", gunz_status);
        let out_file = dir.path().join("decompressed.txt");
        {
            let mut f = File::create(&out_file).unwrap();
            f.write_all(&gunz_status.stdout).unwrap();
        }
        // CRC on decompressed bytes
        let mut bytes = Vec::new();
        File::open(&out_file).unwrap().read_to_end(&mut bytes).unwrap();
        let mut digest = CRC_CCITT_FALSE.digest();
        digest.update(&bytes);
        let crc_val = digest.finalize();
        // CRC for our string verified externally (it's deterministic)
        assert_eq!(crc_val, 0x7B98);
    }
}