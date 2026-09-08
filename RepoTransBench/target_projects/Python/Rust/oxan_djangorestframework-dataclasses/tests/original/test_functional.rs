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
    fn test_pet_serialize_and_deserialize() {
        let pet = Pet {
            animal: Animal::Cat,
            name: "Milo".to_string(),
            weight: None,
        };

        // simulate serialization and deserialization
        let json = serde_json::to_string(&pet).unwrap();
        let pet2: Pet = serde_json::from_str(&json).unwrap();
        assert_eq!(pet, pet2);
    }

    #[test]
    fn test_building_union_material_wood() {
        let b = Building {
            material: Material::Wood(Wood {
                species: "oak".to_string(),
            }),
        };
        let json = serde_json::to_string(&b).unwrap();
        let b2: Building = serde_json::from_str(&json).unwrap();
        assert_eq!(b, b2);
    }

    #[test]
    fn test_building_union_material_steel() {
        let b = Building {
            material: Material::Steel(Steel {
                alloy: "carbon".to_string(),
            }),
        };
        let json = serde_json::to_string(&b).unwrap();
        let b2: Building = serde_json::from_str(&json).unwrap();
        assert_eq!(b, b2);
    }

    #[test]
    fn test_person_full() {
        let id = Uuid::from_str("28ee3ae5-480b-46bd-9ae4-c61cf8341b95").unwrap();
        let birth = NaiveDate::from_ymd_opt(1980, 4, 1).unwrap();
        let p = Person {
            id,
            name: "Alice".to_string(),
            email: "alice@example.com".to_string(),
            phone: vec!["+31-6-1234-5678".to_string(), "+31-20-123-4567".to_string()],
            gender: Some(Gender::Female),
            length: Some(Decimal::from_str("1.68").unwrap()),
            pets: Some(vec![
                Pet {
                    animal: Animal::Cat,
                    name: "Milo".to_string(),
                    weight: Some(Decimal::from_str("10.8").unwrap()),
                },
                Pet {
                    animal: Animal::Dog,
                    name: "Max".to_string(),
                    weight: Some(Decimal::from_str("123.4").unwrap()),
                }
            ]),
            birth_date: Some(birth),
            favorite_pet: Some(Pet {
                animal: Animal::Cat,
                name: "Luna".to_string(),
                weight: None,
            }),
            movie_ratings: Some(
                {
                    let mut m = HashMap::new();
                    m.insert("Star Wars".to_string(), 8);
                    m.insert("Titanic".to_string(), 4);
                    m
                }
            ),
        };

        let json = serde_json::to_string(&p).unwrap();
        let p2: Person = serde_json::from_str(&json).unwrap();
        assert_eq!(p, p2);
        assert_eq!(p2.age(), Some(40));
        assert_eq!(p2.is_child(), Some(false));
    }

    #[test]
    fn test_person_minimal() {
        let id = Uuid::from_str("28ee3ae5-480b-46bd-9ae4-c61cf8341b95").unwrap();
        let p = Person {
            id,
            name: "Alice".to_string(),
            email: "alice@example.com".to_string(),
            phone: vec![],
            gender: None,
            length: None,
            pets: None,
            birth_date: None,
            favorite_pet: None,
            movie_ratings: None,
        };

        let json = serde_json::to_string(&p).unwrap();
        let p2: Person = serde_json::from_str(&json).unwrap();
        assert_eq!(p, p2);
        assert_eq!(p2.age(), None);
        assert_eq!(p2.is_child(), None);
    }

    #[test]
    fn test_obscure_struct() {
        let mut o = Obscure { name: "".to_string() };
        o.name = "Bob".to_string();
        let json = serde_json::to_string(&o).unwrap();
        let o2: Obscure = serde_json::from_str(&json).unwrap();
        assert_eq!(o, o2);
    }

    #[test]
    fn test_person_pet_embedding() {
        let pet = Pet {
            animal: Animal::Cat,
            name: "Katsu".to_string(),
            weight: None,
        };
        let person_pet = PersonPet {
            name: "Milo".to_string(),
            pet: pet.clone(),
        };
        // Simulate embedding: Test key fields exist in child struct
        let json = serde_json::to_string(&person_pet).unwrap();
        let pp2: PersonPet = serde_json::from_str(&json).unwrap();
        assert_eq!(pp2.name, "Milo");
        assert_eq!(pp2.pet.name, "Katsu");
        assert_eq!(pp2.pet.animal, Animal::Cat);
    }
}