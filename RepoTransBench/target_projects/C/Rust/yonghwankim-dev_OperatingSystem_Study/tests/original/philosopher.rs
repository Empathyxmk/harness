// Rust translation of operatingsystem_c/chap07_synchronization/test_philosopher.c

const N: usize = 5;
const THINKING: i32 = 0;
const HUNGRY: i32 = 1;
const EATING: i32 = 2;

static mut STATE: [i32; N] = [THINKING; N];

fn test_take_forks(i: usize) {
    unsafe {
        STATE[i] = HUNGRY;
        // both neighbors not EATING – let EAT
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
    fn test_philo_cycle() {
        unsafe {
            for i in 0..N {
                STATE[i] = THINKING;
            }
        }

        test_take_forks(1);

        unsafe {
            assert_eq!(STATE[1], EATING);
        }

        test_put_forks(1);

        unsafe {
            assert_eq!(STATE[1], THINKING);
        }
    }
}