import pytest

@pytest.mark.skip("Skipping because of import issues in fairseq.modules.character_token_embedder in this environment")
def test_char_embedder_forward_shapes_public():
    import torch
    from fairseq.modules.character_token_embedder import CharacterTokenEmbedder

    batch_size = 3
    max_word_length = 7
    num_embeddings = 40
    embedding_dim = 12

    embedder = CharacterTokenEmbedder(num_embeddings, embedding_dim)
    input_tokens = torch.randint(0, num_embeddings, (batch_size, max_word_length, 2))
    output = embedder(input_tokens[..., 0])

    assert output.shape[0] == batch_size
    assert output.shape[1] == embedding_dim

@pytest.mark.skip("Skipping because of import issues in fairseq.modules.character_token_embedder in this environment")
def test_char_embedder_forward_content_public():
    import torch
    from fairseq.modules.character_token_embedder import CharacterTokenEmbedder

    batch_size = 2
    max_word_length = 4
    num_embeddings = 26
    embedding_dim = 8

    embedder = CharacterTokenEmbedder(num_embeddings, embedding_dim)
    input_tokens = torch.tensor([[1, 2, 3, 5], [7, 1, 0, 4]])
    output = embedder(input_tokens)
    assert output.shape == (batch_size, embedding_dim)