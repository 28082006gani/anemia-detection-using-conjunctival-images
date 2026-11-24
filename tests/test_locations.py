from app.services.locations import search_locations

def test_search_locations_prefix_examples():
    # Test "Dav"
    dav_results = search_locations("Dav")
    assert len(dav_results) >= 2
    cities = [r["city"] for r in dav_results]
    assert "Davangere" in cities
    assert "Davorlim" in cities
    
    # Test format
    davangere = next(r for r in dav_results if r["city"] == "Davangere")
    assert davangere["state"] == "Karnataka"
    assert davangere["country"] == "India"
    assert davangere["display"] == "Davangere, Karnataka, India"

    davorlim = next(r for r in dav_results if r["city"] == "Davorlim")
    assert davorlim["state"] == "Goa"
    assert davorlim["country"] == "India"
    assert davorlim["display"] == "Davorlim, Goa, India"

    # Test "Ban"
    ban_results = search_locations("Ban")
    assert len(ban_results) >= 1
    assert any("Bengaluru" in r["city"] for r in ban_results)

    # Test "Mum"
    mum_results = search_locations("Mum")
    assert len(mum_results) >= 1
    assert any("Mumbai" in r["city"] for r in mum_results)

    # Test "Hyd"
    hyd_results = search_locations("Hyd")
    assert len(hyd_results) >= 1
    assert any("Hyderabad" in r["city"] for r in hyd_results)

    # Test "Vil"
    vil_results = search_locations("Vil")
    assert len(vil_results) >= 1
    assert any("Viluppuram" in r["city"] or "Village" in r["city"] for r in vil_results)

def test_search_locations_minimum_characters():
    assert search_locations("") == []
    assert search_locations("D") == []
    assert len(search_locations("Da")) > 0

def test_api_locations_search_endpoint(client):
    # Minimum length enforcement
    res_short = client.get('/api/locations/search?q=a')
    assert res_short.status_code == 200
    assert res_short.get_json() == []

    # Successful search
    res = client.get('/api/locations/search?q=Dav')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert any(item["city"] == "Davangere" for item in data)
    assert any(item["city"] == "Davorlim" for item in data)
    assert all("display" in item and "state" in item and "country" in item for item in data)
