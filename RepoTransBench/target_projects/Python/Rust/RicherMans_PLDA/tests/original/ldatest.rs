use richer_mans_plda::lda::LDA;
use ndarray::array;

#[test]
fn test_fit() {
    let x = array![[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0],[2.0,3.0,4.0]];
    let y = array![0,1,0,1];
    let mut lda = LDA::new(Some(2));
    let model = lda.fit(&x, &y);
    assert_eq!(model as *const _, &lda as *const _);
    assert_eq!(lda.model.as_ref().unwrap()[0][0], 4);
}

#[test]
fn test_transform() {
    let x = array![[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0],[2.0,3.0,4.0]];
    let y = array![0,1,0,1];
    let mut lda = LDA::new(Some(2));
    lda.fit(&x, &y);
    let x_new = lda.transform(&x);
    assert_eq!(x_new.shape()[1], 2);
}

#[test]
fn test_fit_transform() {
    let x = array![[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0],[2.0,3.0,4.0]];
    let y = array![0,1,0,1];
    let mut lda = LDA::new(Some(2));
    let x_new = lda.fit_transform(&x, &y);
    assert_eq!(x_new.shape()[1], 2);
}

#[test]
fn test_transform_n_components_none() {
    let x = array![[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0],[2.0,3.0,4.0]];
    let y = array![0,1,0,1];
    let mut lda = LDA::new(None);
    lda.fit(&x, &y);
    let x_new = lda.transform(&x);
    assert_eq!(x_new.shape(), x.shape());
}