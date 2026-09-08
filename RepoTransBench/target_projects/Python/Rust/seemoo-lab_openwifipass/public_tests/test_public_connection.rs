struct DummyPWSHandlerPublic {
    calls: Vec<(String, Vec<u8>)>,
}
impl DummyPWSHandlerPublic {
    fn new() -> Self { Self { calls: Vec::new() } }
    fn receive_pws2(&mut self, x: Vec<u8>) { self.calls.push(("pws2".to_string(), x)); }
    fn receive_m2(&mut self, x: Vec<u8>) { self.calls.push(("m2".to_string(), x)); }
    fn receive_m4(&mut self, x: Vec<u8>) { self.calls.push(("m4".to_string(), x)); }
    fn receive_pws4(&mut self, x: Vec<u8>) { self.calls.push(("pws4".to_string(), x)); }
}

#[test]
fn test_handle_notification_main_paths_public() {
    let ft_exp = vec![
        (25u8, 0, "pws2"),
        (20u8, 1, "m2"),
        (20u8, 2, "m4"),
        (7u8, 3, "pws4"),
    ];
    for (ft, _state, exp) in ft_exp {
        let mut handler = DummyPWSHandlerPublic::new();
        handler.receive_pws2(vec![ft]);
        assert!(!handler.calls.is_empty());
        assert_eq!(handler.calls[0].0, exp);
    }
}