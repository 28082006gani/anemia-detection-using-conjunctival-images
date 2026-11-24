import hashlib

def predict(image_path: str) -> dict:
    """
    Predictor stub conforming to the ARCHITECTURE.md contract.
    Returns placeholder values until the trained deep learning model is integrated.
    
    Returns:
      {
        "status": "Anemia" | "Non-anemia",
        "hemoglobin": float,       # g/dL (1 decimal place)
        "confidence": float,       # 0.0 - 1.0
        "is_placeholder": bool     # True until real model is connected
      }
    """
    # Deterministic placeholder variation based on file hash for realistic testing
    try:
        with open(image_path, 'rb') as f:
            digest = int(hashlib.md5(f.read()[:512]).hexdigest(), 16)
    except Exception:
        digest = 42

    # Alternate between realistic Anemia (< 11.0 g/dL) and Non-anemia (>= 12.5 g/dL)
    if digest % 2 == 0:
        status = "Anemia"
        hb = round(9.2 + ((digest % 25) / 10.0), 1)  # 9.2 - 11.6 g/dL
        confidence = round(0.85 + ((digest % 12) / 100.0), 2)
    else:
        status = "Non-anemia"
        hb = round(12.8 + ((digest % 30) / 10.0), 1)  # 12.8 - 15.7 g/dL
        confidence = round(0.88 + ((digest % 10) / 100.0), 2)

    return {
        "status": status,
        "hemoglobin": hb,
        "confidence": min(confidence, 0.98),
        "is_placeholder": True
    }
