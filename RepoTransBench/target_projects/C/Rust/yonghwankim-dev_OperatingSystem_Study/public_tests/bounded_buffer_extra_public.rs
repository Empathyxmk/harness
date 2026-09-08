// Translation of operatingsystem_c/chap07_synchronization/test_bounded_buffer_extra_public.c

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
        let value = BUFFER[OUT];
        OUT = (OUT + 1) % 5;
        value
    }
}

fn buffer_is_empty() -> bool {
    unsafe { IN == OUT }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_more_pushes_than_pops_public() {
        buffer_init();
        buffer_push(100);
        buffer_push(200);
        buffer_push(300);
        buffer_push(400);
        assert_eq!(buffer_pop(), 100);
        assert_eq!(buffer_pop(), 200);
        assert_eq!(buffer_pop(), 300);
        assert_eq!(buffer_pop(), 400);
        assert!(buffer_is_empty());
    }

    #[test]
    fn test_push_pop_alternate_public() {
        buffer_init();
        buffer_push(11);
        assert_eq!(buffer_pop(), 11);
        buffer_push(21);
        assert_eq!(buffer_pop(), 21);
        buffer_push(31);
        buffer_push(41);
        assert_eq!(buffer_pop(), 31);
        assert_eq!(buffer_pop(), 41);
        assert!(buffer_is_empty());
    }
}