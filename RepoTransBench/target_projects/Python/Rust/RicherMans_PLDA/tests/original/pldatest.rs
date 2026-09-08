use richer_mans_plda::plda::PLDA;
use ndarray::array;

#[test]
fn test_fit() {
    let x = array![[1.0,2.0],[3.0,4.0],[5.0,6.0]];
    let y = array![0,1,0];
    let mut plda = PLDA::new();
    let out = plda.fit(&x, &y);
    assert!(plda.trained);
    assert_eq!(out as *const _, &plda as *const _);
}

#[test]
fn test_predict() {
    let x = array![[1.0,2.0],[3.0,4.0],[5.0,6.0]];
    let y = array![0,1,0];
    let mut plda = PLDA::new();
    plda.fit(&x, &y);
    let pred = plda.predict(&x).unwrap();
    assert!(pred.iter().all(|&val| val == 0));
}

#[test]
fn test_predict_without_fit() {
    let x = array![[1.0,2.0],[3.0,4.0],[5.0,6.0]];
    let _y = array![0,1,0];
    let p = PLDA::new();
    let result = p.predict(&x);
    assert!(result.is_err());
}