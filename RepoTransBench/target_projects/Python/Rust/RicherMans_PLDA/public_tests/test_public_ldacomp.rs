use richer_mans_plda::lda::LDA;
use ndarray::array;

#[test]
fn test_lda_fit_and_transform_public() {
    let x = array![[2.0,6.0,4.0],[1.0,5.0,8.0],[4.0,2.0,9.0]];
    let y = array![1,0,0];
    let mut lda = LDA::new(Some(2));
    lda.fit(&x, &y);
    let x_trans = lda.transform(&x);
    assert_eq!(x_trans.shape(), &[3,2]);
}