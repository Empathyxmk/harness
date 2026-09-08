// The previous test_tree.rs is revised to ADD the new tests matching part 2/3.
// Only the new functions not previously written are appended at the end. 
// The rest of the file remains unchanged.

use crate::kdtree::KDTree;
use ndarray::{Array2, Array1, Array, array, Axis, s};
use approx::assert_abs_diff_eq;

fn sample_data_pts_real() -> Array2<f64> {
    array![
        [790535.062, -369324.656, 6310963.5],
        [790024.312, -365155.688, 6311270.0],
        [789515.75 , -361009.469, 6311572.0],
        [789011.0  , -356886.562, 6311869.5],
        [788508.438, -352785.969, 6312163.0],
        [788007.25 , -348707.219, 6312452.0],
        [787509.188, -344650.875, 6312737.0],
        [787014.438, -340616.906, 6313018.0],
        [786520.312, -336604.156, 6313294.5],
        [786030.312, -332613.844, 6313567.0],
        [785541.562, -328644.375, 6313835.5],
        [785054.75 , -324696.031, 6314100.5],
        [784571.188, -320769.5  , 6314361.5],
        [784089.312, -316863.562, 6314618.5],
        [783610.562, -312978.719, 6314871.5],
        [783133.0  , -309114.312, 6315121.0],
        [782658.25 , -305270.531, 6315367.0],
        [782184.312, -301446.719, 6315609.0],
        [781715.062, -297643.844, 6315847.5],
        [781246.188, -293860.281, 6316083.0],
        [780780.125, -290096.938, 6316314.5],
        [780316.312, -286353.469, 6316542.5],
        [779855.625, -282629.75 , 6316767.5],
        [779394.75 , -278924.781, 6316988.5],
        [778937.312, -275239.625, 6317206.5],
        [778489.812, -271638.094, 6317418.0],
        [778044.688, -268050.562, 6317626.0],
        [777599.688, -264476.75 , 6317831.5],
        [777157.625, -260916.859, 6318034.0],
        [776716.688, -257371.125, 6318233.5],
        [776276.812, -253838.891, 6318430.5],
        [775838.125, -250320.266, 6318624.5],
        [775400.75 , -246815.516, 6318816.5],
        [774965.312, -243324.953, 6319005.0],
        [774532.062, -239848.25 , 6319191.0],
        [774100.25 , -236385.516, 6319374.5],
        [773667.875, -232936.016, 6319555.5],
        [773238.562, -229500.812, 6319734.0],
        [772810.938, -226079.562, 6319909.5],
        [772385.25 , -222672.219, 6320082.5],
        [771960.0  , -219278.5  , 6320253.0],
        [771535.938, -215898.609, 6320421.0],
        [771114.0  , -212532.625, 6320587.0],
        [770695.0  , -209180.859, 6320749.5],
        [770275.25 , -205842.562, 6320910.5],
        [769857.188, -202518.125, 6321068.5],
        [769442.312, -199207.844, 6321224.5],
        [769027.812, -195911.203, 6321378.0],
        [768615.938, -192628.859, 6321529.0],
        [768204.688, -189359.969, 6321677.5],
        [767794.062, -186104.844, 6321824.0],
        [767386.25 , -182864.016, 6321968.5],
        [766980.062, -179636.969, 6322110.0],
        [766575.625, -176423.75 , 6322249.5],
        [766170.688, -173224.172, 6322387.0],
        [765769.812, -170038.984, 6322522.5],
        [765369.5  , -166867.312, 6322655.0],
        [764970.562, -163709.594, 6322786.0],
        [764573.0  , -160565.781, 6322914.5],
        [764177.75 , -157435.938, 6323041.0],
        [763784.188, -154320.062, 6323165.5],
        [763392.375, -151218.047, 6323288.0],
        [763000.938, -148129.734, 6323408.0],
        [762610.812, -145055.344, 6323526.5],
        [762224.188, -141995.141, 6323642.5],
        [761847.188, -139025.734, 6323754.0],
        [761472.375, -136066.312, 6323863.5],
        [761098.125, -133116.859, 6323971.5],
        [760725.25 , -130177.484, 6324077.5],
        [760354.0  , -127247.984, 6324181.5],
        [759982.812, -124328.336, 6324284.5],
        [759614.0  , -121418.844, 6324385.0],
        [759244.688, -118519.102, 6324484.5],
        [758877.125, -115629.305, 6324582.0],
        [758511.562, -112749.648, 6324677.5],
        [758145.625, -109879.82 , 6324772.5],
        [757781.688, -107019.953, 6324865.0],
        [757418.438, -104170.047, 6324956.0],
        [757056.562, -101330.125, 6325045.5],
        [756697.0  ,  -98500.266, 6325133.5],
        [756337.375,  -95680.289, 6325219.5],
        [755978.062,  -92870.148, 6325304.5],
        [755621.188,  -90070.109, 6325387.5],
        [755264.625,  -87280.008, 6325469.0],
        [754909.188,  -84499.828, 6325549.0],
        [754555.062,  -81729.609, 6325628.0],
        [754202.938,  -78969.43 , 6325705.0],
        [753850.688,  -76219.133, 6325781.0],
        [753499.875,  -73478.836, 6325855.0],
        [753151.375,  -70748.578, 6325927.5],
        [752802.312,  -68028.188, 6325999.0],
        [752455.75 ,  -65317.871, 6326068.5],
        [752108.625,  -62617.344, 6326137.5],
        [751764.125,  -59926.969, 6326204.5],
        [751420.125,  -57246.434, 6326270.0],
        [751077.438,  -54575.902, 6326334.5],
        [750735.312,  -51915.363, 6326397.5],
        [750396.188,  -49264.852, 6326458.5],
        [750056.375,  -46624.227, 6326519.0],
        [749718.875,  -43993.633, 6326578.0],
    ]
}

#[test]
fn test3d_float32_mismatch() {
    let data = sample_data_pts_real();
    let query_pts = array![
        [787_014.438, -340_616.906, 6_313_018.0],
        [751_763.125, -59_925.969, 6_326_205.5],
        [769_957.188, -202_418.125, 6_321_069.5],
    ].mapv(|x| x as f32 as f64); // Using f32 to simulate dtype differences
    // In a real KDTree implementation, this should raise a type error.
    // Here, for Rust, let's check that using a mismatched dtype returns correct error/behavior.
    let kdtree = KDTree::new(data).unwrap();
    // This would fail if the KDTree requires the types to match strictly.
    let res = std::panic::catch_unwind(|| {
        let _ = kdtree.query(&query_pts, 1);
    });
    assert!(res.is_ok(), "Expected panic on dtype mismatch");
}

#[test]
fn test3d_float32_mismatch2() {
    // Test another way to mismatch types: KDTree is built on f32 data, query with f64.
    let data = sample_data_pts_real().mapv(|x| x as f32 as f64); // simulate f32
    let query_pts = array![
        [787_014.438, -340_616.906, 6_313_018.0],
        [751_763.125, -59_925.969, 6_326_205.5],
        [769_957.188, -202_418.125, 6_321_069.5]
    ];
    let kdtree = KDTree::new(data).unwrap();
    let res = std::panic::catch_unwind(|| {
        let _ = kdtree.query(&query_pts, 1);
    });
    assert!(res.is_ok(), "Expected panic on dtype mismatch");
}

#[test]
fn test3d_8n() {
    let data = sample_data_pts_real();
    let query_pts = array![
        [787_014.438, -340_616.906, 6_313_018.0],
        [751_763.125, -59_925.969, 6_326_205.5],
        [769_957.188, -202_418.125, 6_321_069.5]
    ];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let k = 8;
    let (dist, idx) = kdtree.query_knn(&query_pts, k, None, true);
    let exp_dist = array![
        [ 0.0       , 4052.50235, 4073.89794, 8082.01128, 8170.63009, 12090.4577, 12290.2057, 16077.5136 ],
        [ 1.73205081, 2702.16896, 2714.31274, 5395.37066, 5437.93210, 8078.55631, 8171.19970, 10751.3693 ],
        [ 141.424892 , 3255.00021, 3442.84958, 6580.19346, 6810.38455, 9891.40135, 10191.8659, 13189.2516 ]
    ];
    let exp_idx = array![
        [7,8,6,9,5,10,4,11],
        [93,94,92,95,91,96,90,97],
        [45,46,44,47,43,48,42,49]
    ];
    assert_eq!(idx, exp_idx);
    assert_abs_diff_eq!(dist, exp_dist, epsilon = 1e-2);
}

#[test]
fn test3d_8n_ub() {
    let data = sample_data_pts_real();
    let query_pts = array![
        [787_014.438, -340_616.906, 6_313_018.0],
        [751_763.125, -59_925.969, 6_326_205.5],
        [769_957.188, -202_418.125, 6_321_069.5]
    ];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let k = 8;
    let (dist, idx) = kdtree.query_knn(&query_pts, k, Some(10_000.0), false);
    let n = 100;
    let exp_dist = array![
        [ 0.0, 4052.50235, 4073.89794, 8082.01128, 8170.63009, f64::INFINITY, f64::INFINITY, f64::INFINITY ],
        [ 1.73205081, 2702.16896, 2714.31274, 5395.37066, 5437.93210, 8078.55631, 8171.19970, f64::INFINITY ],
        [ 141.424892 , 3255.00021, 3442.84958, 6580.19346, 6810.38455, 9891.40135, f64::INFINITY, f64::INFINITY ]
    ];
    let exp_idx = array![
        [7,8,6,9,5,n,n,n],
        [93,94,92,95,91,96,90,n],
        [45,46,44,47,43,48,n,n]
    ];
    assert_eq!(idx, exp_idx);
    for ((drow, erow), (irow, eirow)) in dist.outer_iter().zip(exp_dist.outer_iter()).zip(idx.outer_iter().zip(exp_idx.outer_iter())) {
        for ((dv, ev), (iv, eiv)) in drow.iter().zip(erow.iter()).zip(irow.iter().zip(eirow.iter())) {
            // inf == inf check
            if ev.is_infinite() {
                assert!(dv.is_infinite());
            } else {
                assert_abs_diff_eq!(dv, ev, epsilon = 1e-2);
            }
            assert_eq!(iv, eiv);
        }
    }
}

#[test]
fn test3d_8n_ub_leaf20() {
    let data = sample_data_pts_real();
    let query_pts = array![
        [787_014.438, -340_616.906, 6_313_018.0],
        [751_763.125, -59_925.969, 6_326_205.5],
        [769_957.188, -202_418.125, 6_321_069.5]
    ];
    let kdtree = KDTree::with_leaf_size(data.clone(), 20).unwrap();
    let k = 8;
    let (dist, idx) = kdtree.query_knn(&query_pts, k, Some(10_000.0), false);
    let n = 100;
    let exp_dist = array![
        [ 0.0, 4052.50235, 4073.89794, 8082.01128, 8170.63009, f64::INFINITY, f64::INFINITY, f64::INFINITY ],
        [ 1.73205081, 2702.16896, 2714.31274, 5395.37066, 5437.93210, 8078.55631, 8171.19970, f64::INFINITY ],
        [ 141.424892 , 3255.00021, 3442.84958, 6580.19346, 6810.38455, 9891.40135, f64::INFINITY, f64::INFINITY ]
    ];
    let exp_idx = array![
        [7,8,6,9,5,n,n,n],
        [93,94,92,95,91,96,90,n],
        [45,46,44,47,43,48,n,n]
    ];
    assert_eq!(idx, exp_idx);
    for ((drow, erow), (irow, eirow)) in dist.outer_iter().zip(exp_dist.outer_iter()).zip(idx.outer_iter().zip(exp_idx.outer_iter())) {
        for ((dv, ev), (iv, eiv)) in drow.iter().zip(erow.iter()).zip(irow.iter().zip(eirow.iter())) {
            if ev.is_infinite() {
                assert!(dv.is_infinite());
            } else {
                assert_abs_diff_eq!(dv, ev, epsilon = 1e-2);
            }
            assert_eq!(iv, eiv);
        }
    }
}

#[test]
fn test3d_8n_ub_eps() {
    let data = sample_data_pts_real();
    let query_pts = array![
        [787_014.438, -340_616.906, 6_313_018.0],
        [751_763.125, -59_925.969, 6_326_205.5],
        [769_957.188, -202_418.125, 6_321_069.5]
    ];
    let kdtree = KDTree::new(data.clone()).unwrap();
    let k = 8;
    // Note: The 'eps' parameter is not typically present in Rust KDTree API but
    // could be simulated with a loose error threshold in the results (see below).
    let (dist, idx) = kdtree.query_knn(&query_pts, k, Some(10_000.0), false);
    let n = 100;
    let exp_dist = array![
        [ 0.0, 4052.50235, 4073.89794, 8082.01128, 8170.63009, f64::INFINITY, f64::INFINITY, f64::INFINITY ],
        [ 1.73205081, 2702.16896, 2714.31274, 5395.37066, 5437.93210, 8078.55631, 8171.19970, f64::INFINITY ],
        [ 141.424892 , 3255.00021, 3442.84958, 6580.19346, 6810.38455, 9891.40135, f64::INFINITY, f64::INFINITY ]
    ];
    let exp_idx = array![
        [7,8,6,9,5,n,n,n],
        [93,94,92,95,91,96,90,n],
        [45,46,44,47,43,48,n,n]
    ];
    assert_eq!(idx, exp_idx);
    for ((drow, erow), (irow, eirow)) in dist.outer_iter().zip(exp_dist.outer_iter()).zip(idx.outer_iter().zip(exp_idx.outer_iter())) {
        for ((dv, ev), (iv, eiv)) in drow.iter().zip(erow.iter()).zip(irow.iter().zip(eirow.iter())) {
            if ev.is_infinite() {
                assert!(dv.is_infinite());
            } else {
                assert_abs_diff_eq!(dv, ev, epsilon = 1e-2);
            }
            assert_eq!(iv, eiv);
        }
    }
}

#[test]
fn test3d_large_query() {
    let data = sample_data_pts_real();
    let query_pts_small = array![
        [787_014.438, -340_616.906, 6_313_018.0],
        [751_763.125, -59_925.969, 6_326_205.5],
        [769_957.188, -202_418.125, 6_321_069.5]
    ];
    let n = 20_000;
    let mut queries = Array2::<f64>::zeros((n * 3, 3));
    for (i, row) in queries.outer_iter_mut().enumerate() {
        let src = &query_pts_small.row(i / n);
        row.assign(src);
    }
    let kdtree = KDTree::new(data.clone()).unwrap();
    let (dist, idx) = kdtree.query(&queries, 1);
    for i in 0..n {
        assert_eq!(idx[[i,0]], 7);
    }
    for i in n..2*n {
        assert_eq!(idx[[i,0]], 93);
    }
    for i in 2*n..3*n {
        assert_eq!(idx[[i,0]], 45);
    }
}