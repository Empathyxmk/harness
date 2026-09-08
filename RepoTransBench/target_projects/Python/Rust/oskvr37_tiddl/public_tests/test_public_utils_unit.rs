#[cfg(test)]
mod tests {
    use crate::utils::{is_url, slugify, clean_filename};

    #[test]
    fn test_is_url_public() {
        assert!(is_url("https://www.example.com/music/track/999"));
        assert!(is_url("ftp://server.com/download/track"));
        assert!(!is_url("not a url at all"));
        assert!(!is_url("songname.mp3"));
    }

    #[test]
    fn test_slugify_public() {
        assert_eq!(slugify("Hello World Public! 123"), "hello-world-public-123");
        assert_eq!(slugify("Another_Party V2"), "another-party-v2");
        assert_eq!(slugify("spëcïäl_chär$"), "special-char");
    }

    #[test]
    fn test_clean_filename_public() {
        assert_eq!(clean_filename("Song:Best*Of*2018?.mp3"), "SongBestOf2018.mp3");
        assert_eq!(clean_filename(" Album|New <Mix>.wav "), " AlbumNew Mix.wav ");
        assert_eq!(clean_filename("A/B\\C<D>E|F*G:H?I"), "ABCDEFGHI");
    }
}