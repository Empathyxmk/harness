#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[tokio::test]
    async fn test_caa_get_image() {
        let image_data = json!({
            "thumbnails": {
                "small": "http://example.com/small.jpg",
                "large": "http://example.com/large.jpg"
            },
            "image": "http://example.com/image.jpg"
        });

        // Simulate API response for an image
        let response = get_image(image_data).await.unwrap();
        assert_eq!(response.thumbnails.small, "http://example.com/small.jpg");
        assert_eq!(response.image, "http://example.com/image.jpg");
    }

    async fn get_image(data: serde_json::Value) -> Result<Image, reqwest::Error> {
        Ok(Image {
            thumbnails: Thumbnails {
                small: data["thumbnails"]["small"].to_string(),
                large: data["thumbnails"]["large"].to_string(),
            },
            image: data["image"].to_string(),
        })
    }

    struct Image {
        thumbnails: Thumbnails,
        image: String,
    }
    struct Thumbnails {
        small: String,
        large: String,
    }
}