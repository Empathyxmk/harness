// Translated from tests/deye_sensor_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_sensor_scale() {
        let sensor = Sensor { scale: 10.0 };
        let reading = sensor.read_value(3.0);
        assert_eq!(reading, 30.0);
    }

    struct Sensor {
        scale: f64,
    }
    impl Sensor {
        fn read_value(&self, input: f64) -> f64 {
            input * self.scale
        }
    }
}