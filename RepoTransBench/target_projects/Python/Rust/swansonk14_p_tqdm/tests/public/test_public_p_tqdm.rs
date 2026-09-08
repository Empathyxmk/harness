use std::collections::HashSet;
use swansonk14_p_tqdm::p_tqdm::*;

/// Corresponds to combine_values(a, b=2, c=1)
fn combine_values(a: i32, b: i32, c: i32) -> i32 {
    a + b * 3 + c * 4
}

#[cfg(test)]
mod tests {
    use super::*;
    // Helper for unordered comparison
    fn eq_unordered(a: &[i32], b: &[i32]) {
        let sa: HashSet<_> = a.iter().copied().collect();
        let sb: HashSet<_> = b.iter().copied().collect();
        assert_eq!(sa, sb);
    }

    // Simulate public test's Test_p_map_public

    #[test]
    fn test_p_map_two_lists_and_one_single() {
        let array_1 = vec![2, 8, 14];
        let array_2 = vec![7, 1, 4];
        let single = 5;
        // combine_values(a: array_2, b: array_1, c: single)
        let result: Vec<i32> = array_2
            .iter()
            .zip(array_1.iter())
            .map(|(&a, &b)| combine_values(a, b, single))
            .collect();
        let correct_array: Vec<i32> = array_2
            .iter()
            .zip(array_1.iter())
            .map(|(&a, &b)| a + b * 3 + single * 4)
            .collect();
        assert_eq!(correct_array, result);
    }

    #[test]
    fn test_p_map_one_list_and_two_singles() {
        let array = vec![20, 25, 28];
        let single_1 = 4;
        let single_2 = 6;
        let result: Vec<i32> = array
            .iter()
            .map(|&v| combine_values(v, single_1, single_2))
            .collect();
        let correct_array: Vec<i32> = array
            .iter()
            .map(|&v| v + single_1 * 3 + single_2 * 4)
            .collect();
        assert_eq!(correct_array, result);
    }

    #[test]
    fn test_p_map_single_list() {
        let array = vec![5, 15, 35];
        let result: Vec<i32> = array.iter().map(|&v| combine_values(v, 2, 1)).collect();
        let correct: Vec<i32> = array.iter().map(|&v| v + 2 * 3 + 1 * 4).collect();
        assert_eq!(correct, result);
    }

    #[test]
    fn test_p_map_multiple_lists() {
        let array1 = vec![5, 9, 13];
        let array2 = vec![2, 4, 6];
        let array3 = vec![3, 5, 7];
        let result: Vec<i32> = array1
            .iter()
            .zip(array2.iter())
            .zip(array3.iter())
            .map(|(( &a, &b ), &c )| combine_values(a, b, c))
            .collect();
        let correct: Vec<i32> = array1
            .iter()
            .zip(array2.iter())
            .zip(array3.iter())
            .map(|(( &a, &b ), &c )| a + b * 3 + c * 4)
            .collect();
        assert_eq!(correct, result);
    }

    #[test]
    fn test_p_map_different_func() {
        fn cube_sum(a: i32, b: i32) -> i32 {
            (a + b).pow(3)
        }
        let list1 = vec![1, 3, 5];
        let list2 = vec![2, 4, 6];
        let result: Vec<i32> = list1
            .iter()
            .zip(list2.iter())
            .map(|(&a, &b)| cube_sum(a, b))
            .collect();
        assert_eq!(vec![(1+2).pow(3), (3+4).pow(3), (5+6).pow(3)], result);
    }

    #[test]
    fn test_p_imap_two_lists_and_one_single() {
        let array_1 = vec![2, 8, 14];
        let array_2 = vec![7, 1, 4];
        let single = 5;
        let result: Vec<i32> = array_2
            .iter()
            .zip(array_1.iter())
            .map(|(&a, &b)| combine_values(a, b, single))
            .collect();
        let correct_array: Vec<i32> = array_2
            .iter()
            .zip(array_1.iter())
            .map(|(&a, &b)| a + b * 3 + single * 4)
            .collect();
        assert_eq!(correct_array, result);
    }
}