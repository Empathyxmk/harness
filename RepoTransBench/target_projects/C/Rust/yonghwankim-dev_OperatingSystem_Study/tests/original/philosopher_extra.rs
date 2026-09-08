// Rust translation of operatingsystem_c/chap07_synchronization/test_philosopher_extra.c

const N: usize = 5;
const THINKING: i32 = 0;
const HUNGRY: i32 = 1;
const EATING: i32 = 2;

static mut STATE: [i32; N] = [THINKING; N];

fn test_take_forks(i: usize) {
    unsafe {
        STATE[i] = HUNGRY;
        STATE[i] = EATING;
    }
}

fn test_put_forks(i: usize) {
    unsafe {
        STATE[i] = THINKING;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_independent_philosophers() {
        unsafe {
            for i in 0..N {
                STATE[i] = THINKING;
            }
        }

        test_take_forks(0);
        test_take_forks(4);

        unsafe {
            assert_eq!(STATE[0], EATING);
            assert_eq!(STATE[4], EATING);
        }

        test_put_forks(0);
        test_put_forks(4);

        unsafe {
            assert_eq!(STATE[0], THINKING);
            assert_eq!(STATE[4], THINKING);
        }
    }

    #[test]
    fn test_rapid_cycle() {
        unsafe {
            STATE[2] = THINKING;
        }
        test_take_forks(2);

        unsafe {
            assert_eq!(STATE[2], EATING);
        }

        test_put_forks(2);

        unsafe {
            assert_eq!(STATE[2], THINKING);
        }

        test_take_forks(2);

        unsafe {
            assert_eq!(STATE[2], EATING);
        }
    }
}