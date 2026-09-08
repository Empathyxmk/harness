#[cfg(test)]
mod tests {
    use super::super::super::car_flyweight::*;
    use std::rc::Rc;
    use serial_test::serial;

    #[test]
    #[serial]
    fn test_carmodel_singleton_behavior() {
        let m1 = CarModel::new("Sedan", Some(true), None, None, None);
        let m2 = CarModel::new("Sedan", Some(false), None, None, None);
        // Singleton: should return same instance
        assert!(Rc::ptr_eq(&m1, &m2));
        assert_eq!(m1.model_name, "Sedan");
        assert!(m1.air);
        assert!(!m1.alloy_wheels);
        let m3 = CarModel::new("Coupé", Some(false), Some(true), None, None);
        assert!(!Rc::ptr_eq(&m3, &m1));
        assert!(m3.tilt);
        assert!(!m3.air);
    }

    #[test]
    #[serial]
    fn test_carmodel_check_serial_output() {
        let m = CarModel::new("X", None, None, None, Some(true));
        let output = m.check_serial("XYZ-123");
        assert!(output.contains("XYZ-123") && output.contains("X"));
    }

    #[test]
    #[serial]
    fn test_car_check_serial_delegates() {
        let m = CarModel::new("TestModel", None, None, None, None);
        let c = Car::new(Rc::clone(&m), "Red", 555);
        let output = c.check_serial();
        assert!(output.contains("555"));
    }

    #[test]
    #[serial]
    fn test_car_attributes() {
        let m = CarModel::new("Z", None, None, None, None);
        let c = Car::new(Rc::clone(&m), "Blue", 999);
        assert!(Rc::ptr_eq(&c.model, &m));
        assert_eq!(c.color, "Blue");
        assert_eq!(c.serial, 999);
    }
}