use richer_mans_plda::lda::LDA;
use ndarray::array;

#[test]
fn test_fit_public() {
    let x = array![[3.0,8.0,1.0],[6.0,2.0,7.0],[5.0,4.0,0.0],[9.0,1.0,2.0]];
    let y = array![2,2,1,1];
    let mut lda = LDA::new(Some(2));
    let model = lda.fit(&x, &y);
    // Check same pointer
    assert_eq!(model as *const _, &lda as *const _);
    // model[0][0] == n_samples
    assert_eq!(lda.model.as_ref().unwrap()[0][0], 4);
}

#[test]
fn test_transform_public() {
    let x = array![[3.0,8.0,1.0],[6.0,2.0,7.0],[5.0,4.0,0.0],[9.0,1.0,2.0]];
    let y = array![2,2,1,1];
    let mut lda = LDA::new(Some(2));
    lda.fit(&x, &y);
    let x_new = lda.transform(&x);
    assert_eq!(x_new.shape()[1], 2);
}

#[test]
fn test_fit_transform_public() {
    let x = array![[3.0,8.0,1.0],[6.0,2.0,7.0],[5.0,4.0,0.0],[9.0,1.0,2.0]];
    let y = array![2,2,1,1];
    let mut lda = LDA::new(Some(2));
    let x_new = lda.fit_transform(&x, &y);
    assert_eq!(x_new.shape()[1], 2);
}

#[test]
fn test_transform_n_components_none_public() {
    let x = array![[3.0,8.0,1.0],[6.0,2.0,7.0],[5.0,4.0,0.0],[9.0,1.0,2.0]];
    let y = array![2,2,1,1];
    let mut lda2 = LDA::new(None);
    lda2.fit(&x, &y);
    let x_new = lda2.transform(&x);
    assert_eq!(x_new.shape(), x.shape());
}