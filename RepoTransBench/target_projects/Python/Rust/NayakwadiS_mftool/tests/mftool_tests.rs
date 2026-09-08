use std::collections::HashMap;
use nayakwadis_mftool::{Mftool, is_holiday, get_friday, get_today};

fn json_to_hashmap(json_str: &str) -> HashMap<String, serde_json::Value> {
    serde_json::from_str(json_str).unwrap()
}

#[test]
fn test_get_scheme_codes() {
    let mftool = Mftool::new();
    let sc = mftool.get_scheme_codes();
    assert!(!sc.is_empty());
    // Check type
    assert!(sc.is_empty() == false);
    // Check as_json
    let sc_json = mftool.get_scheme_codes_json();
    assert!(sc_json.starts_with("{") && sc_json.ends_with("}"));
    // compare keys via serde
    let sc_json_map = json_to_hashmap(&sc_json);
    for (k, v) in &sc {
        assert_eq!(*v, sc_json_map.get(k).unwrap().as_str().unwrap());
    }
    let result = mftool.get_available_schemes("ICICI");
    // One arbitrary test, make sure "Axis" is not in the first value
    let (_, v) = result.iter().next().unwrap();
    assert!(!v.contains("Axis"));
}

#[test]
fn test_is_valid_code() {
    let mftool = Mftool::new();
    let code = "119598";
    assert!(mftool.is_valid_code(code));
}

#[test]
fn test_negative_is_valid_code() {
    let mftool = Mftool::new();
    let wrong_code = "1195";
    assert!(!mftool.is_valid_code(wrong_code));
}

#[test]
fn test_get_scheme_quote() {
    let mftool = Mftool::new();
    let code = "101305";
    let resp = mftool.get_scheme_quote(code, false);
    assert!(resp.is_some());
    assert!(resp.as_ref().unwrap().contains("nav"));

    let resp_json = mftool.get_scheme_quote(code, true);
    assert!(resp_json.is_some());
    assert!(resp_json.as_ref().unwrap().starts_with("{"));

    // wrong code
    let wrong = mftool.get_scheme_quote("wrong code", false);
    assert!(wrong.is_none());

    // code as integer
    let resp_int = mftool.get_scheme_quote(101305, false);
    assert!(resp_int.is_some());
    // verify data present
    let result = mftool.get_scheme_quote(code, false);
    assert!(result.is_some());
}

#[test]
fn test_get_scheme_historical_nav() {
    let mftool = Mftool::new();
    let code = "101305";
    let resp = mftool.get_scheme_historical_nav(code, false);
    assert!(resp.is_some());
    let resp_json = mftool.get_scheme_historical_nav(code, true);
    assert!(resp_json.is_some());

    let wrong = mftool.get_scheme_historical_nav("wrong code", false);
    assert!(wrong.is_none());

    let resp_int = mftool.get_scheme_historical_nav(101305, false);
    assert!(resp_int.is_some());
    // verify data present
    let result = mftool.get_scheme_historical_nav(code, false);
    assert!(result.is_some());
}

#[test]
fn test_get_scheme_details() {
    let mftool = Mftool::new();
    let code = "101305";
    let resp = mftool.get_scheme_details(code, false);
    assert!(resp.is_some());
    let resp_json = mftool.get_scheme_details(code, true);
    assert!(resp_json.is_some());

    let wrong = mftool.get_scheme_details("wrong code", false);
    assert!(wrong.is_none());

    let resp_int = mftool.get_scheme_details(101305, false);
    assert!(resp_int.is_some());

    let result = mftool.get_scheme_details(code, false);
    assert!(result.is_some());
}

#[test]
fn test_calculate_balance_units_value() {
    let mftool = Mftool::new();
    let code = "101305";
    let result = mftool.calculate_balance_units_value(code, 221);
    assert!(result.is_some());
}

#[test]
fn test_get_scheme_historical_nav_year() {
    let mftool = Mftool::new();
    let code = "101305";
    let resp = mftool.get_scheme_historical_nav_year(code, 2018, false);
    assert!(resp.is_some());
    let resp_json = mftool.get_scheme_historical_nav_year(code, 2018, true);
    assert!(resp_json.is_some());

    let wrong = mftool.get_scheme_historical_nav_year("wrong code", 2018, false);
    assert!(wrong.is_none());

    let resp_int = mftool.get_scheme_historical_nav_year(101305, 2018, false);
    assert!(resp_int.is_some());

    let result = mftool.get_scheme_historical_nav_year(code, 2018, false);
    assert!(result.is_some());
}

#[test]
fn test_get_day() {
    if is_holiday() {
        assert!(get_friday());
    } else {
        assert!(get_today());
    }
}

#[test]
fn test_get_scheme_historical_nav_for_dates() {
    let mftool = Mftool::new();
    let code = "101305";
    let resp = mftool.get_scheme_historical_nav_for_dates(code, "1-1-2018", "31-12-2018", false);
    assert!(resp.is_some());
    let resp_json = mftool.get_scheme_historical_nav_for_dates(code, "1-1-2018", "31-12-2018", true);
    assert!(resp_json.is_some());

    let wrong = mftool.get_scheme_historical_nav_for_dates("wrong code", "1-1-2018", "31-12-2018", false);
    assert!(wrong.is_none());

    let resp_int = mftool.get_scheme_historical_nav_for_dates(101305, "1-1-2018", "31-12-2018", false);
    assert!(resp_int.is_some());

    let result = mftool.get_scheme_historical_nav_for_dates(code, "1-1-2018", "31-12-2018", false);
    assert!(result.is_some());
}

#[test]
fn test_get_open_ended_equity_scheme_performance() {
    let mftool = Mftool::new();
    let resp = mftool.get_open_ended_equity_scheme_performance(false);
    assert!(!resp.is_empty());

    let empty_test: HashMap<&'static str, Vec<&'static str>> = [
        ("Large Cap", vec![]),("Large & Mid Cap", vec![]),("Multi Cap", vec![]),
        ("Mid Cap", vec![]),("Small Cap", vec![]),("Value", vec![]),
        ("ELSS", vec![]),("Contra", vec![]),("Dividend Yield", vec![]),("Focused", vec![])
    ].iter().cloned().collect();
    // At least one value should be not equal to the all-empties map (the dummy implementation does this)
    for (k, v) in &empty_test {
        assert!(!resp.get::<str>(k).unwrap_or(&vec![]).is_empty());
    }
}