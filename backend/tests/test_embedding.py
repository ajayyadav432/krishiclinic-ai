import pytest
from app.ai.embedding import generate_embedding, get_mock_embedding, cosine_similarity

@pytest.mark.asyncio
async def test_mock_embedding_dimensions_and_norm():
    vec = await generate_embedding("Wheat: yellow rust symptoms")
    assert len(vec) == 768
    # Test normalization: norm should be ~1.0
    norm = sum(v * v for v in vec) ** 0.5
    assert abs(norm - 1.0) < 1e-4

@pytest.mark.asyncio
async def test_mock_embedding_semantic_cosine_similarity():
    # Similar agricultural texts with shared keywords
    t1 = "Wheat: yellow spots and rust symptoms on leaves"
    t2 = "Wheat: yellow rust lesions on leaf canopy"
    # Dissimilar text
    t3 = "Potato: tuber black scurf soil fungal disease"

    v1 = await generate_embedding(t1)
    v2 = await generate_embedding(t2)
    v3 = await generate_embedding(t3)

    sim_related = cosine_similarity(v1, v2)
    sim_unrelated = cosine_similarity(v1, v3)

    # Similar agricultural texts must have significantly higher similarity than unrelated texts
    assert sim_related > 0.4, f"Expected higher similarity for related texts, got {sim_related}"
    assert sim_related > sim_unrelated, f"Related similarity ({sim_related}) must exceed unrelated ({sim_unrelated})"

def test_cosine_similarity_edge_cases():
    assert cosine_similarity([], []) == 0.0
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == 0.0
    assert abs(cosine_similarity([1.0, 2.0], [1.0, 2.0]) - 1.0) < 1e-5
