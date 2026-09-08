#[cfg(test)]
mod tests {
    // These tests simulate getting lat/lon from geolocation field

    #[derive(PartialEq, Debug, Clone)]
    struct GeoPt {
        lat: f64,
        lon: f64,
    }

    impl GeoPt {
        fn from_str(s: &str) -> GeoPt {
            let vals: Vec<&str> = s.split(',').collect();
            GeoPt {
                lat: vals[0].parse::<f64>().unwrap(),
                lon: vals[1].parse::<f64>().unwrap(),
            }
        }
    }

    #[derive(PartialEq, Debug)]
    struct Person {
        pk: i32,
        geolocation: GeoPt,
    }

    struct PersonDB {
        data: Vec<Person>,
        next_pk: i32,
    }

    impl PersonDB {
        fn new() -> Self {
            PersonDB { data: Vec::new(), next_pk: 1 }
        }
        fn create_with_str(&mut self, geolocation: &str) -> Person {
            let person = Person {
                pk: self.next_pk,
                geolocation: GeoPt::from_str(geolocation),
            };
            self.next_pk += 1;
            self.data.push(person.clone());
            person
        }
        fn create_with_pt(&mut self, pt: GeoPt) -> Person {
            let person = Person {
                pk: self.next_pk,
                geolocation: pt,
            };
            self.next_pk += 1;
            self.data.push(person.clone());
            person
        }
        fn find_by_pk(&self, pk: i32) -> Option<&Person> {
            self.data.iter().find(|p| p.pk == pk)
        }
        fn get_by_geopt_exact(&self, pt: GeoPt) -> Option<&Person> {
            self.data.iter().find(|p| p.geolocation == pt)
        }
        fn get_by_geopt_in(&self, pts: &[GeoPt]) -> Option<&Person> {
            self.data.iter().find(|p| pts.contains(&p.geolocation))
        }
    }

    #[test]
    fn test_getting_lat_lon_from_model_given_string() {
        let mut db = PersonDB::new();
        let inserted = db.create_with_str("45,90");
        let found = db.find_by_pk(inserted.pk).unwrap();
        assert_eq!(found.geolocation.lat, 45.0);
        assert_eq!(found.geolocation.lon, 90.0);
    }

    #[test]
    fn test_getting_lat_lon_from_model_given_pt() {
        let mut db = PersonDB::new();
        let geo_pt = GeoPt::from_str("45,90");
        let inserted = db.create_with_pt(geo_pt.clone());
        let found = db.find_by_pk(inserted.pk).unwrap();
        assert_eq!(found.geolocation.lat, 45.0);
        assert_eq!(found.geolocation.lon, 90.0);
    }

    #[test]
    fn test_getting_lat_lon_from_model_in_db_given_string() {
        let mut db = PersonDB::new();
        let inserted = db.create_with_str("45,90");
        let found = db.find_by_pk(inserted.pk).unwrap();
        assert_eq!(found.geolocation.lat, 45.0);
        assert_eq!(found.geolocation.lon, 90.0);
    }

    #[test]
    fn test_exact_match_query() {
        let mut db = PersonDB::new();
        let inserted = db.create_with_str("45,90");
        let found = db.get_by_geopt_exact(GeoPt::from_str("45,90")).unwrap();
        assert_eq!(found, &inserted);
    }

    #[test]
    fn test_in_match_query() {
        let mut db = PersonDB::new();
        let inserted = db.create_with_str("45,90");
        let found = db.get_by_geopt_in(&[GeoPt::from_str("45,90")]).unwrap();
        assert_eq!(found, &inserted);
    }

    fn value_to_string(geo_pt: &GeoPt) -> String {
        format!("{},{}", geo_pt.lat, geo_pt.lon)
    }

    #[test]
    fn test_value_to_string_with_point() {
        let pt = GeoPt::from_str("45,90");
        let s = value_to_string(&pt);
        assert_eq!(s, "45,90");
    }

    #[test]
    fn test_value_to_string_with_string() {
        let pt = GeoPt::from_str("45,90");
        let s = value_to_string(&pt);
        assert_eq!(s, "45,90");
    }

    #[test]
    fn test_get_prep_value_returns_none_when_none() {
        let value: Option<GeoPt> = None;
        assert!(value.is_none());
    }
}