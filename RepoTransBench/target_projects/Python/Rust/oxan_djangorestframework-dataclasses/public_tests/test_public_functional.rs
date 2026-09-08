use std::collections::HashMap;
use std::str::FromStr;
use chrono::NaiveDate;
use rust_decimal::Decimal;
use uuid::Uuid;

use djangorestframework_dataclasses_rs::models::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pet_public_test() {
        let pet = Pet {
            animal: Animal::Dog,
            name: "Charlie".to_string(),
            weight: Some(Decimal::from_str("12.5").unwrap()),
        };
        let json = serde_json::to_string(&pet).unwrap();
        let pet2: Pet = serde_json::from_str(&json).unwrap();
        assert_eq!(pet, pet2);
    }

    #[test]
    fn building_public_test() {
        let b = Building {
            material: Material::Steel(Steel {
                alloy: "stainless".to_string()
            })
        };
        let json = serde_json::to_string(&b).unwrap();
        let b2: Building = serde_json::from_str(&json).unwrap();
        assert_eq!(b, b2);
    }

    #[test]
    fn person_public_test_full() {
        let id = Uuid::from_str("12345678-1234-5678-1234-567812345678").unwrap();
        let birth = NaiveDate::from_ymd_opt(2000, 6, 15).unwrap();
        let pet = Pet {
            animal: Animal::Dog,
            name: "Charlie".to_string(),
            weight: Some(Decimal::from_str("12.5").unwrap()),
        };
        let person = Person {
            id,
            name: "Bob".to_string(),
            email: "bob@example.org".to_string(),
            phone: vec!["+1-800-555-1234".to_string()],
            gender: Some(Gender::Male),
            length: Some(Decimal::from_str("1.75").unwrap()),
            pets: Some(vec![pet.clone()]),
            birth_date: Some(birth),
            favorite_pet: Some(pet.clone()),
            movie_ratings: Some({
                let mut m = HashMap::new();
                m.insert("Jaws".to_string(), 10);
                m.insert("Finding Nemo".to_string(), 7);
                m
            }),
        };

        let json = serde_json::to_string(&person).unwrap();
        let person2: Person = serde_json::from_str(&json).unwrap();
        assert_eq!(person, person2);
        // Custom fields tested here
        assert_eq!(person2.age(), Some(21));
        assert_eq!(person2.is_child(), Some(false));
    }

    #[test]
    fn empty_person_public_test() {
        let id = Uuid::from_str("12345678-1234-5678-1234-567812345678").unwrap();
        let person = Person {
            id,
            name: "Bob".to_string(),
            email: "bob@example.org".to_string(),
            phone: vec![],
            gender: None,
            length: None,
            pets: None,
            birth_date: None,
            favorite_pet: None,
            movie_ratings: None,
        };

        let json = serde_json::to_string(&person).unwrap();
        let p2: Person = serde_json::from_str(&json).unwrap();
        assert_eq!(person, p2);
        assert_eq!(p2.age(), None);
        assert_eq!(p2.is_child(), None);
    }
}