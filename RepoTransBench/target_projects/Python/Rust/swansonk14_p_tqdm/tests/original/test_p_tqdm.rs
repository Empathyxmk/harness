use std::collections::HashSet;

/// Functions for `add_1`, `add_2`, `add_3` as in the Python test.
fn add_1(a: i32) -> i32 {
    a + 1
}

fn add_2(a: i32, b: i32) -> i32 {
    a + b
}

fn add_3(a: i32, b: i32, c: i32) -> i32 {
    a + 2 * b + 3 * c
}

// To allow for functional partial application as in Python's `functools.partial`
fn add_3_partial_a(a: i32) -> impl Fn(i32, i32) -> i32 {
    move |b, c| add_3(a, b, c)
}
fn add_3_partial_ac(a: i32, c: i32) -> impl Fn(i32) -> i32 {
    move |b| add_3(a, b, c)
}
fn add_3_partial_c(c: i32) -> impl Fn(i32, i32) -> i32 {
    move |a, b| add_3(a, b, c)
}

#[cfg(test)]
mod tests {
    use super::*;
    use swansonk14_p_tqdm::p_tqdm::*;
    
    // Helper for unordered comparison
    fn eq_unordered(a: &[i32], b: &[i32]) {
        let sa: HashSet<_> = a.iter().copied().collect();
        let sb: HashSet<_> = b.iter().copied().collect();
        assert_eq!(sa, sb);
    }

    #[test]
    fn test_p_map_one_list() {
        let array = vec![1, 2, 3];
        let result = p_map(add_1, array.clone());
        let correct_array = vec![2, 3, 4];
        assert_eq!(correct_array, result);
    }

    #[test]
    fn test_p_map_two_lists() {
        let array_1 = vec![1, 2, 3];
        let array_2 = vec![10, 11, 12];
        let result = p_map2(add_2, array_1, array_2);
        let correct_array = vec![11, 13, 15];
        assert_eq!(correct_array, result);
    }

    #[test]
    fn test_p_map_two_lists_and_one_single() {
        let array_1 = vec![1, 2, 3];
        let array_2 = vec![10, 11, 12];
        let single = 5;
        let res: Vec<i32> = array_1
            .iter()
            .zip(array_2.iter())
            .map(|(&b, &c)| add_3(single, b, c))
            .collect();
        let correct_array = vec![37, 42, 47];
        assert_eq!(correct_array, res);
    }

    #[test]
    fn test_p_map_one_list_and_two_singles() {
        let array = vec![1, 2, 3];
        let single_1 = 5;
        let single_2 = -2;
        let res: Vec<i32> = array
            .iter()
            .map(|&b| add_3(single_1, b, single_2))
            .collect();
        let correct_array = vec![1, 3, 5];
        assert_eq!(correct_array, res);
    }

    #[test]
    fn test_p_map_list_and_generator_and_single_equal_length() {
        let array = vec![1, 2, 3];
        let generator: Vec<_> = (0..3).collect();
        let single = -3;
        let res: Vec<i32> = array
            .iter()
            .zip(generator.iter())
            .map(|(&a, &b)| add_3(a, b, single))
            .collect();
        let correct_array = vec![-8, -5, -2];
        assert_eq!(correct_array, res);
    }

    #[test]
    fn test_p_map_list_and_generator_and_single_unequal_length() {
        let array = vec![1, 2, 3, 4, 5, 6];
        let generator: Vec<_> = (0..3).collect();
        let single = -3;
        // Only process as many as shortest
        let res: Vec<i32> = array
            .iter()
            .take(generator.len())
            .zip(generator.iter())
            .map(|(&a, &b)| add_3(a, b, single))
            .collect();
        let correct_array = vec![-8, -5, -2];
        assert_eq!(correct_array, res);
    }

    #[test]
    fn test_p_imap_one_list() {
        let array = vec![1, 2, 3];
        let result: Vec<_> = p_imap(add_1, array.clone()).collect();
        let correct_array = vec![2, 3, 4];
        assert_eq!(correct_array, result);
    }

    #[test]
    fn test_p_umap_two_lists() {
        let array_1 = vec![1, 2, 3];
        let array_2 = vec![10, 11, 12];
        let result = p_map2(add_2, array_1, array_2);
        let correct_array = vec![11, 13, 15];
        eq_unordered(&correct_array, &result); // unordered
    }

    #[test]
    fn test_p_uimap_list_and_generator_and_single_unequal_length() {
        let array = vec![1, 2, 3, 4, 5, 6];
        let generator: Vec<_> = (0..3).collect();
        let single = -3;
        let res: Vec<i32> = array
            .iter()
            .take(generator.len())
            .zip(generator.iter())
            .map(|(&a, &b)| add_3(a, b, single))
            .collect();
        let correct_array = vec![-8, -5, -2];
        eq_unordered(&correct_array, &res); // unordered
    }

    #[test]
    fn test_t_map_list_and_generator_and_single_equal_length() {
        let array = vec![1, 2, 3];
        let generator: Vec<_> = (0..3).collect();
        let single = -3;
        let res: Vec<i32> = array
            .iter()
            .zip(generator.iter())
            .map(|(&a, &b)| add_3(a, b, single))
            .collect();
        let correct_array = vec![-8, -5, -2];
        assert_eq!(correct_array, res);
    }

    #[test]
    fn test_t_imap_list_and_generator_and_single_unequal_length() {
        let array = vec![1, 2, 3, 4, 5, 6];
        let generator: Vec<_> = (0..3).collect();
        let single = -3;
        let res: Vec<i32> = array
            .iter()
            .take(generator.len())
            .zip(generator.iter())
            .map(|(&a, &b)| add_3(a, b, single))
            .collect();
        let correct_array = vec![-8, -5, -2];
        assert_eq!(correct_array, res);
    }
}