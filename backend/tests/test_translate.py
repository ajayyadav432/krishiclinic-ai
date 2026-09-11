import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_translate_offline_fallback():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "text": "Early Blight",
            "target_language": "hi"
        }
        response = await client.post("/api/v1/translate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert len(data["translated_text"]) > 0
    assert "अगेती झुलसा" in data["translated_text"]

@pytest.mark.asyncio
async def test_translate_english_passthrough():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "text": "Powdery Mildew",
            "target_language": "en"
        }
        response = await client.post("/api/v1/translate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["translated_text"] == "Powdery Mildew"

@pytest.mark.asyncio
async def test_translate_full_advisory_sentences_offline():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Hindi sentence translation
        hi_rec = "Apply propiconazole fungicide at 0.1% concentration. Monitor field edges where infection typically initiates."
        resp_hi = await client.post("/api/v1/translate", json={"text": hi_rec, "target_language": "hi"})
        assert resp_hi.status_code == 200
        data_hi = resp_hi.json()
        assert "प्रोपिकोनाज़ोल" in data_hi["translated_text"]

        # Telugu reason translation
        te_rec = "Good agricultural practices and favorable weather conditions."
        resp_te = await client.post("/api/v1/translate", json={"text": te_rec, "target_language": "te"})
        assert resp_te.status_code == 200
        assert len(resp_te.json()["translated_text"]) > 0
        assert "వ్యవసాయ పద్ధతులు" in resp_te.json()["translated_text"]

        # Spanish recommendation translation
        es_rec = "Continue current agricultural practices. Monitor regularly for early signs of pest or disease pressure."
        resp_es = await client.post("/api/v1/translate", json={"text": es_rec, "target_language": "es"})
        assert resp_es.status_code == 200
        assert "prácticas" in resp_es.json()["translated_text"]

        # Marathi sentence translation
        mr_rec = "Apply propiconazole fungicide at 0.1% concentration. Monitor field edges where infection typically initiates."
        resp_mr = await client.post("/api/v1/translate", json={"text": mr_rec, "target_language": "mr"})
        assert resp_mr.status_code == 200
        assert "प्रोपिकोनाझोल" in resp_mr.json()["translated_text"]

@pytest.mark.asyncio
async def test_translate_all_languages_crops_and_severities():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test crops in all supported target languages
        crop_expectations = {
            "hi": "गेहूं",
            "te": "గోధుమ",
            "mr": "गहू",
            "es": "Trigo",
        }
        for lang, expected in crop_expectations.items():
            resp = await client.post("/api/v1/translate", json={"text": "Wheat", "target_language": lang})
            assert resp.status_code == 200
            assert resp.json()["translated_text"] == expected

        # Test severity translation
        severity_expectations = {
            "hi": "उच्च",
            "te": "ఎక్కువ",
            "mr": "जास्त",
            "es": "Alto",
        }
        for lang, expected in severity_expectations.items():
            resp = await client.post("/api/v1/translate", json={"text": "High", "target_language": lang})
            assert resp.status_code == 200
            assert resp.json()["translated_text"] == expected

@pytest.mark.asyncio
async def test_translate_dynamic_reason_template():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        text = "Fungal spore transmission, high relative humidity (above 85%), and prolonged wetness on the leaves of the Tomato crop."
        # Hindi template
        resp_hi = await client.post("/api/v1/translate", json={"text": text, "target_language": "hi"})
        assert resp_hi.status_code == 200
        assert "टमाटर" in resp_hi.json()["translated_text"]
        assert "कवक बीजाणु" in resp_hi.json()["translated_text"]

        # Telugu template
        resp_te = await client.post("/api/v1/translate", json={"text": text, "target_language": "te"})
        assert resp_te.status_code == 200
        assert "టమోటా" in resp_te.json()["translated_text"]
        assert "శిలీంద్ర" in resp_te.json()["translated_text"]

        # Marathi template
        resp_mr = await client.post("/api/v1/translate", json={"text": text, "target_language": "mr"})
        assert resp_mr.status_code == 200
        assert "टोमॅटो" in resp_mr.json()["translated_text"]
        assert "बुरशीजन्य" in resp_mr.json()["translated_text"]

        # Spanish template
        resp_es = await client.post("/api/v1/translate", json={"text": text, "target_language": "es"})
        assert resp_es.status_code == 200
        assert "Tomate" in resp_es.json()["translated_text"]
        assert "esporas" in resp_es.json()["translated_text"]

@pytest.mark.asyncio
async def test_translate_empty_and_unknown_text():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Empty text
        resp_empty = await client.post("/api/v1/translate", json={"text": "   ", "target_language": "hi"})
        assert resp_empty.status_code == 200
        assert resp_empty.json()["translated_text"] == ""
