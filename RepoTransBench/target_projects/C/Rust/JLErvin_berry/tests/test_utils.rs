use std::ffi::CString;
use std::ptr;
use berry::utils::{safe_strncpy, berry_asprintf};

#[test]
fn test_safe_strncpy_normal_fn() {
    unsafe {
        let mut dest = [0u8; 10];
        let src = CString::new("hello").unwrap();
        
        // Test that the function exists
        assert!(!safe_strncpy as *const () == ptr::null());
        
        safe_strncpy(dest.as_mut_ptr(), src.as_ptr() as *const u8, dest.len());
        
        let dest_str = CString::from_raw(CString::from_vec_unchecked(dest.to_vec()).into_raw())
            .to_string_lossy()
            .to_string();
        
        assert_eq!(dest_str, "hello");
    }
}

#[test]
fn test_safe_strncpy_src_longer_than_dest_fn() {
    unsafe {
        let mut dest = [0u8; 5];
        let src = CString::new("longerstring").unwrap();
        
        safe_strncpy(dest.as_mut_ptr(), src.as_ptr() as *const u8, dest.len());
        
        // Check that the last byte is null
        assert_eq!(dest[dest.len() - 1], 0);
    }
}

#[test]
fn test_safe_strncpy_empty_src_fn() {
    unsafe {
        let mut dest = [0u8; 4];
        let src = CString::new("").unwrap();
        
        safe_strncpy(dest.as_mut_ptr(), src.as_ptr() as *const u8, dest.len());
        
        let dest_str = CString::from_raw(CString::from_vec_unchecked(dest.to_vec()).into_raw())
            .to_string_lossy()
            .to_string();
        
        assert_eq!(dest_str, "");
    }
}

#[test]
fn test_asprintf_basic_fn() {
    unsafe {
        let mut str_ptr: *mut u8 = ptr::null_mut();
        let fmt = CString::new("The answer is %d").unwrap();
        
        let ret = berry_asprintf(&mut str_ptr as *mut *mut u8, fmt.as_ptr() as *const u8);
        
        assert!(ret > 0);
        assert!(!str_ptr.is_null());
        
        let result_str = CString::from_raw(str_ptr as *mut i8)
            .to_string_lossy()
            .to_string();
        
        assert_eq!(result_str, "The answer is 42");
    }
}

#[test]
fn test_asprintf_null_ptr_fn() {
    unsafe {
        let fmt = CString::new("Nothing here").unwrap();
        
        let ret = berry_asprintf(ptr::null_mut(), fmt.as_ptr() as *const u8);
        
        assert_eq!(ret, -1);
    }
}

#[test]
fn test_asprintf_empty_format_fn() {
    unsafe {
        let mut str_ptr: *mut u8 = ptr::null_mut();
        let fmt = CString::new("").unwrap();
        
        let ret = berry_asprintf(&mut str_ptr as *mut *mut u8, fmt.as_ptr() as *const u8);
        
        assert_eq!(ret, 0);
        assert!(!str_ptr.is_null());
        
        let result_str = CString::from_raw(str_ptr as *mut i8)
            .to_string_lossy()
            .to_string();
        
        assert_eq!(result_str, "");
    }
}