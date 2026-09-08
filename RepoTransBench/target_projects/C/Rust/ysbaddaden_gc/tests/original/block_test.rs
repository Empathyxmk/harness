use ysbaddaden_gc::block::Block;

#[test]
fn test_block_init() {
    let block = Block::new(1234);
    assert_eq!(block.size, 1234);
}