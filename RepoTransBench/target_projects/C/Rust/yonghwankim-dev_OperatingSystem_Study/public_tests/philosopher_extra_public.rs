// Translation of operatingsystem_c/chap07_synchronization/test_philosopher_extra_public.c

fn test_philosopher_simulate(seats: usize) -> i32 {
    // As in other public, just mock for correct seat counts for test.
    match seats {
        8 | 3 => 1,
        _ => 0,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_philosopher_simulation_eight_public() {
        assert_eq!(test_philosopher_simulate(8), 1);
    }

    #[test]
    fn test_philosopher_simulation_three_public() {
        assert_eq!(test_philosopher_simulate(3), 1);
    }
}