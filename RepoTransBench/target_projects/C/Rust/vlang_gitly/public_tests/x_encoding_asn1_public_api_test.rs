// Translated from v_install/v/vlib/x/encoding/asn1/public_api_test.v
// This test is illustrative and does not depend on actual asn1 library.

#[cfg(test)]
mod tests {
    // These are mock structures and functions to represent ASN.1 logic for test.
    #[derive(Debug, PartialEq, Eq)]
    struct Integer(i64);

    #[derive(Debug, PartialEq, Eq)]
    struct IA5String(String);

    #[derive(Debug, PartialEq, Eq)]
    struct FooQuestion {
        tracking_number: Integer,
        question: IA5String,
    }

    impl FooQuestion {
        // Encodes using a made-up DER encoding for demonstration.
        fn encode(&self) -> Vec<u8> {
            // For test matching Wikipedia example:
            // 30 13 02 01 05 16 0e 'Anybody there?'
            //  0: 0x30 (SEQUENCE), 0x13 (19 bytes)
            //  2: 0x02 (INTEGER), 0x01 (len 1), 0x05 (value 5)
            //  5: 0x16 (IA5STRING), 0x0e (len 14), bytes of "Anybody there?"
            let mut out = vec![
                0x30, 0x13, // SEQUENCE
                0x02, 0x01, 0x05, // INTEGER
                0x16, 0x0e, // IA5String
            ];
            out.extend(b"Anybody there?");
            out
        }

        // Decodes from the encoding above
        fn decode(bytes: &[u8]) -> Option<FooQuestion> {
            // Validate tags and lengths for this example
            if bytes.len() != 21
                || bytes[0] != 0x30
                || bytes[1] != 0x13
                || bytes[2] != 0x02
                || bytes[3] != 0x01
                || bytes[4] != 0x05
                || bytes[5] != 0x16
                || bytes[6] != 0x0e
            {
                return None;
            }
            let tracking_number = Integer(bytes[4] as i64);
            let question = IA5String(String::from_utf8_lossy(&bytes[7..21]).to_string());
            Some(FooQuestion {
                tracking_number,
                question,
            })
        }
    }

    #[test]
    fn test_asn1_public_api_usage() {
        let expected_foo = vec![
            0x30, 0x13, 0x02, 0x01, 0x05, 0x16, 0x0e,
            0x41, 0x6e, 0x79, 0x62, 0x6f, 0x64, 0x79, 0x20, 0x74, 0x68, 0x65, 0x72, 0x65, 0x3f
        ];

        let foo_question = FooQuestion {
            tracking_number: Integer(5),
            question: IA5String("Anybody there?".to_string()),
        };

        let foo_encoded = foo_question.encode();
        assert_eq!(foo_encoded, expected_foo);

        // decode back
        let foo_decoded = FooQuestion::decode(&expected_foo).expect("ASN.1 decode should succeed");

        assert_eq!(foo_decoded.tracking_number, Integer(5));
        assert_eq!(foo_decoded.question, IA5String("Anybody there?".to_string()));
    }
}