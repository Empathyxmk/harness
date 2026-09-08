// Translation of operatingsystem_c/chap07_synchronization/test_bounded_buffer_public.c

// We're mocking a buffer type as might be defined in 7.1_bounded_buffer.c's public interface

static mut BUFFER: [i32; 5] = [0; 5];
static mut IN: usize = 0;
static mut OUT: usize = 0;

fn buffer_init() {
    unsafe {
        IN = 0;
        OUT = 0;
        BUFFER = [0; 5];
    }
}

fn buffer_push(item: i32) {
    unsafe {
        BUFFER[IN] = item;
        IN = (IN + 1) % 5;
    }
}

fn buffer_pop() -> i32 {
    unsafe {
        let result = BUFFER[OUT];
        OUT = (OUT + 1) % 5;
        result
    }
}

fn buffer_is_empty() -> bool {
    unsafe { IN == OUT }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_push_and_pop_public() {
        buffer_init();
        buffer_push(42);
        buffer_push(777);
        assert_eq!(buffer_pop(), 42);
        buffer_push(31);
        assert_eq!(buffer_pop(), 777);
        assert_eq!(buffer_pop(), 31);
        assert!(buffer_is_empty());
    }

    #[test]
    fn test_interleaved_push_pop_public() {
        buffer_init();
        buffer_push(1001);
        assert_eq!(buffer_pop(), 1001);
        buffer_push(2022);
        buffer_push(2023);
        assert_eq!(buffer_pop(), 2022);
        buffer_push(3033);
        assert_eq!(buffer_pop(), 2023);
        assert_eq!(buffer_pop(), 3033);
        assert!(buffer_is_empty());
    }
}