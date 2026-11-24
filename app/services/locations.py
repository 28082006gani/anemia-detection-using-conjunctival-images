import re
import json
import urllib.request
import urllib.parse
from functools import lru_cache

# Curated high-coverage dataset of Indian Cities, Towns, Taluks, and Villages
# Covering major metros, tier-2/3 cities, and towns across all states and union territories.
INDIAN_LOCATIONS = [
    # Karnataka
    {"city": "Davangere", "state": "Karnataka", "country": "India"},
    {"city": "Davanagere Rural", "state": "Karnataka", "country": "India"},
    {"city": "Davalapur", "state": "Karnataka", "country": "India"},
    {"city": "Davaleshwar", "state": "Karnataka", "country": "India"},
    {"city": "Bengaluru (Bangalore)", "state": "Karnataka", "country": "India"},
    {"city": "Bengaluru Rural", "state": "Karnataka", "country": "India"},
    {"city": "Bantwal", "state": "Karnataka", "country": "India"},
    {"city": "Bangarapet", "state": "Karnataka", "country": "India"},
    {"city": "Ballari", "state": "Karnataka", "country": "India"},
    {"city": "Belagavi", "state": "Karnataka", "country": "India"},
    {"city": "Bhadravati", "state": "Karnataka", "country": "India"},
    {"city": "Bidar", "state": "Karnataka", "country": "India"},
    {"city": "Chikkamagaluru", "state": "Karnataka", "country": "India"},
    {"city": "Chitradurga", "state": "Karnataka", "country": "India"},
    {"city": "Dharwad", "state": "Karnataka", "country": "India"},
    {"city": "Gadag", "state": "Karnataka", "country": "India"},
    {"city": "Hassan", "state": "Karnataka", "country": "India"},
    {"city": "Haveri", "state": "Karnataka", "country": "India"},
    {"city": "Hubballi", "state": "Karnataka", "country": "India"},
    {"city": "Kalaburagi", "state": "Karnataka", "country": "India"},
    {"city": "Karwar", "state": "Karnataka", "country": "India"},
    {"city": "Kolar", "state": "Karnataka", "country": "India"},
    {"city": "Koppal", "state": "Karnataka", "country": "India"},
    {"city": "Mandya", "state": "Karnataka", "country": "India"},
    {"city": "Mangaluru", "state": "Karnataka", "country": "India"},
    {"city": "Mysuru", "state": "Karnataka", "country": "India"},
    {"city": "Raichur", "state": "Karnataka", "country": "India"},
    {"city": "Ramanagara", "state": "Karnataka", "country": "India"},
    {"city": "Shivamogga", "state": "Karnataka", "country": "India"},
    {"city": "Tumakuru", "state": "Karnataka", "country": "India"},
    {"city": "Udupi", "state": "Karnataka", "country": "India"},
    {"city": "Vijayapura", "state": "Karnataka", "country": "India"},
    {"city": "Yadgir", "state": "Karnataka", "country": "India"},

    # Goa
    {"city": "Davorlim", "state": "Goa", "country": "India"},
    {"city": "Panaji", "state": "Goa", "country": "India"},
    {"city": "Margao", "state": "Goa", "country": "India"},
    {"city": "Vasco da Gama", "state": "Goa", "country": "India"},
    {"city": "Mapusa", "state": "Goa", "country": "India"},
    {"city": "Ponda", "state": "Goa", "country": "India"},
    {"city": "Bicholim", "state": "Goa", "country": "India"},
    {"city": "Curchorem", "state": "Goa", "country": "India"},
    {"city": "Cuncolim", "state": "Goa", "country": "India"},

    # Maharashtra
    {"city": "Mumbai", "state": "Maharashtra", "country": "India"},
    {"city": "Mumbai Suburban", "state": "Maharashtra", "country": "India"},
    {"city": "Mumbra", "state": "Maharashtra", "country": "India"},
    {"city": "Pune", "state": "Maharashtra", "country": "India"},
    {"city": "Nagpur", "state": "Maharashtra", "country": "India"},
    {"city": "Thane", "state": "Maharashtra", "country": "India"},
    {"city": "Nashik", "state": "Maharashtra", "country": "India"},
    {"city": "Kalyan", "state": "Maharashtra", "country": "India"},
    {"city": "Navi Mumbai", "state": "Maharashtra", "country": "India"},
    {"city": "Aurangabad (Chhatrapati Sambhaji Nagar)", "state": "Maharashtra", "country": "India"},
    {"city": "Solapur", "state": "Maharashtra", "country": "India"},
    {"city": "Kolhapur", "state": "Maharashtra", "country": "India"},
    {"city": "Amravati", "state": "Maharashtra", "country": "India"},
    {"city": "Nanded", "state": "Maharashtra", "country": "India"},
    {"city": "Sangli", "state": "Maharashtra", "country": "India"},
    {"city": "Jalgaon", "state": "Maharashtra", "country": "India"},
    {"city": "Akola", "state": "Maharashtra", "country": "India"},
    {"city": "Latur", "state": "Maharashtra", "country": "India"},
    {"city": "Dhule", "state": "Maharashtra", "country": "India"},
    {"city": "Ahmednagar", "state": "Maharashtra", "country": "India"},
    {"city": "Chandrapur", "state": "Maharashtra", "country": "India"},
    {"city": "Parbhani", "state": "Maharashtra", "country": "India"},
    {"city": "Satara", "state": "Maharashtra", "country": "India"},
    {"city": "Ratnagiri", "state": "Maharashtra", "country": "India"},
    {"city": "Vile Parle", "state": "Maharashtra", "country": "India"},
    {"city": "Village Khed", "state": "Maharashtra", "country": "India"},

    # Telangana
    {"city": "Hyderabad", "state": "Telangana", "country": "India"},
    {"city": "Hyderabad Rural", "state": "Telangana", "country": "India"},
    {"city": "Hyderguda", "state": "Telangana", "country": "India"},
    {"city": "Warangal", "state": "Telangana", "country": "India"},
    {"city": "Nizamabad", "state": "Telangana", "country": "India"},
    {"city": "Karimnagar", "state": "Telangana", "country": "India"},
    {"city": "Ramagundam", "state": "Telangana", "country": "India"},
    {"city": "Khammam", "state": "Telangana", "country": "India"},
    {"city": "Mahbubnagar", "state": "Telangana", "country": "India"},
    {"city": "Nalgonda", "state": "Telangana", "country": "India"},
    {"city": "Adilabad", "state": "Telangana", "country": "India"},
    {"city": "Suryapet", "state": "Telangana", "country": "India"},
    {"city": "Miryalaguda", "state": "Telangana", "country": "India"},
    {"city": "Siddipet", "state": "Telangana", "country": "India"},

    # Tamil Nadu
    {"city": "Chennai", "state": "Tamil Nadu", "country": "India"},
    {"city": "Coimbatore", "state": "Tamil Nadu", "country": "India"},
    {"city": "Madurai", "state": "Tamil Nadu", "country": "India"},
    {"city": "Tiruchirappalli", "state": "Tamil Nadu", "country": "India"},
    {"city": "Salem", "state": "Tamil Nadu", "country": "India"},
    {"city": "Tirunelveli", "state": "Tamil Nadu", "country": "India"},
    {"city": "Tiruppur", "state": "Tamil Nadu", "country": "India"},
    {"city": "Vellore", "state": "Tamil Nadu", "country": "India"},
    {"city": "Erode", "state": "Tamil Nadu", "country": "India"},
    {"city": "Thoothukudi", "state": "Tamil Nadu", "country": "India"},
    {"city": "Dindigul", "state": "Tamil Nadu", "country": "India"},
    {"city": "Thanjavur", "state": "Tamil Nadu", "country": "India"},
    {"city": "Ranipet", "state": "Tamil Nadu", "country": "India"},
    {"city": "Sivakasi", "state": "Tamil Nadu", "country": "India"},
    {"city": "Karur", "state": "Tamil Nadu", "country": "India"},
    {"city": "Udhagamandalam (Ooty)", "state": "Tamil Nadu", "country": "India"},
    {"city": "Viluppuram", "state": "Tamil Nadu", "country": "India"},
    {"city": "Villupuram Rural", "state": "Tamil Nadu", "country": "India"},
    {"city": "Vilathikulam", "state": "Tamil Nadu", "country": "India"},
    {"city": "Vilavancode", "state": "Tamil Nadu", "country": "India"},

    # Andhra Pradesh
    {"city": "Visakhapatnam", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Vijayawada", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Guntur", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Nellore", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Kurnool", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Kakinada", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Rajahmundry", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Kadapa", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Tirupati", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Anantapur", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Vizianagaram", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Eluru", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Ongole", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Nandyal", "state": "Andhra Pradesh", "country": "India"},
    {"city": "Machilipatnam", "state": "Andhra Pradesh", "country": "India"},

    # Kerala
    {"city": "Thiruvananthapuram", "state": "Kerala", "country": "India"},
    {"city": "Kochi", "state": "Kerala", "country": "India"},
    {"city": "Kozhikode", "state": "Kerala", "country": "India"},
    {"city": "Kollam", "state": "Kerala", "country": "India"},
    {"city": "Thrissur", "state": "Kerala", "country": "India"},
    {"city": "Kannur", "state": "Kerala", "country": "India"},
    {"city": "Alappuzha", "state": "Kerala", "country": "India"},
    {"city": "Kottayam", "state": "Kerala", "country": "India"},
    {"city": "Palakkad", "state": "Kerala", "country": "India"},
    {"city": "Manjeri", "state": "Kerala", "country": "India"},
    {"city": "Thalassery", "state": "Kerala", "country": "India"},
    {"city": "Kasaragod", "state": "Kerala", "country": "India"},

    # Delhi / NCR
    {"city": "Delhi", "state": "Delhi", "country": "India"},
    {"city": "New Delhi", "state": "Delhi", "country": "India"},
    {"city": "Noida", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Greater Noida", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Ghaziabad", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Gurugram", "state": "Haryana", "country": "India"},
    {"city": "Faridabad", "state": "Haryana", "country": "India"},

    # Gujarat
    {"city": "Ahmedabad", "state": "Gujarat", "country": "India"},
    {"city": "Surat", "state": "Gujarat", "country": "India"},
    {"city": "Vadodara", "state": "Gujarat", "country": "India"},
    {"city": "Rajkot", "state": "Gujarat", "country": "India"},
    {"city": "Bhavnagar", "state": "Gujarat", "country": "India"},
    {"city": "Jamnagar", "state": "Gujarat", "country": "India"},
    {"city": "Junagadh", "state": "Gujarat", "country": "India"},
    {"city": "Gandhinagar", "state": "Gujarat", "country": "India"},
    {"city": "Anand", "state": "Gujarat", "country": "India"},
    {"city": "Navsari", "state": "Gujarat", "country": "India"},
    {"city": "Morbi", "state": "Gujarat", "country": "India"},
    {"city": "Vapi", "state": "Gujarat", "country": "India"},

    # Rajasthan
    {"city": "Jaipur", "state": "Rajasthan", "country": "India"},
    {"city": "Jodhpur", "state": "Rajasthan", "country": "India"},
    {"city": "Kota", "state": "Rajasthan", "country": "India"},
    {"city": "Bikaner", "state": "Rajasthan", "country": "India"},
    {"city": "Ajmer", "state": "Rajasthan", "country": "India"},
    {"city": "Udaipur", "state": "Rajasthan", "country": "India"},
    {"city": "Bhilwara", "state": "Rajasthan", "country": "India"},
    {"city": "Alwar", "state": "Rajasthan", "country": "India"},
    {"city": "Bharatpur", "state": "Rajasthan", "country": "India"},
    {"city": "Sikar", "state": "Rajasthan", "country": "India"},
    {"city": "Banswara", "state": "Rajasthan", "country": "India"},

    # Uttar Pradesh
    {"city": "Lucknow", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Kanpur", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Varanasi", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Agra", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Prayagraj", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Meerut", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Bareilly", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Aligarh", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Moradabad", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Saharanpur", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Gorakhpur", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Firozabad", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Jhansi", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Muzaffarnagar", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Mathura", "state": "Uttar Pradesh", "country": "India"},
    {"city": "Banda", "state": "Uttar Pradesh", "country": "India"},

    # West Bengal
    {"city": "Kolkata", "state": "West Bengal", "country": "India"},
    {"city": "Howrah", "state": "West Bengal", "country": "India"},
    {"city": "Durgapur", "state": "West Bengal", "country": "India"},
    {"city": "Asansol", "state": "West Bengal", "country": "India"},
    {"city": "Siliguri", "state": "West Bengal", "country": "India"},
    {"city": "Bardhaman", "state": "West Bengal", "country": "India"},
    {"city": "Malda", "state": "West Bengal", "country": "India"},
    {"city": "Kharagpur", "state": "West Bengal", "country": "India"},
    {"city": "Bankura", "state": "West Bengal", "country": "India"},

    # Madhya Pradesh
    {"city": "Indore", "state": "Madhya Pradesh", "country": "India"},
    {"city": "Bhopal", "state": "Madhya Pradesh", "country": "India"},
    {"city": "Jabalpur", "state": "Madhya Pradesh", "country": "India"},
    {"city": "Gwalior", "state": "Madhya Pradesh", "country": "India"},
    {"city": "Ujjain", "state": "Madhya Pradesh", "country": "India"},
    {"city": "Sagar", "state": "Madhya Pradesh", "country": "India"},
    {"city": "Dewas", "state": "Madhya Pradesh", "country": "India"},
    {"city": "Satna", "state": "Madhya Pradesh", "country": "India"},
    {"city": "Ratlam", "state": "Madhya Pradesh", "country": "India"},
    {"city": "Rewa", "state": "Madhya Pradesh", "country": "India"},

    # Bihar
    {"city": "Patna", "state": "Bihar", "country": "India"},
    {"city": "Gaya", "state": "Bihar", "country": "India"},
    {"city": "Bhagalpur", "state": "Bihar", "country": "India"},
    {"city": "Muzaffarpur", "state": "Bihar", "country": "India"},
    {"city": "Purnia", "state": "Bihar", "country": "India"},
    {"city": "Darbhanga", "state": "Bihar", "country": "India"},
    {"city": "Bihar Sharif", "state": "Bihar", "country": "India"},
    {"city": "Arrah", "state": "Bihar", "country": "India"},
    {"city": "Begusarai", "state": "Bihar", "country": "India"},

    # Punjab / Haryana
    {"city": "Chandigarh", "state": "Chandigarh", "country": "India"},
    {"city": "Ludhiana", "state": "Punjab", "country": "India"},
    {"city": "Amritsar", "state": "Punjab", "country": "India"},
    {"city": "Jalandhar", "state": "Punjab", "country": "India"},
    {"city": "Patiala", "state": "Punjab", "country": "India"},
    {"city": "Bathinda", "state": "Punjab", "country": "India"},
    {"city": "Panipat", "state": "Haryana", "country": "India"},
    {"city": "Ambala", "state": "Haryana", "country": "India"},
    {"city": "Yamunanagar", "state": "Haryana", "country": "India"},
    {"city": "Rohtak", "state": "Haryana", "country": "India"},
    {"city": "Hisar", "state": "Haryana", "country": "India"},
    {"city": "Karnal", "state": "Haryana", "country": "India"},

    # Odisha
    {"city": "Bhubaneswar", "state": "Odisha", "country": "India"},
    {"city": "Cuttack", "state": "Odisha", "country": "India"},
    {"city": "Rourkela", "state": "Odisha", "country": "India"},
    {"city": "Berhampur", "state": "Odisha", "country": "India"},
    {"city": "Sambalpur", "state": "Odisha", "country": "India"},
    {"city": "Puri", "state": "Odisha", "country": "India"},
    {"city": "Balasore", "state": "Odisha", "country": "India"},

    # Jharkhand / Chhattisgarh
    {"city": "Ranchi", "state": "Jharkhand", "country": "India"},
    {"city": "Jamshedpur", "state": "Jharkhand", "country": "India"},
    {"city": "Dhanbad", "state": "Jharkhand", "country": "India"},
    {"city": "Bokaro Steel City", "state": "Jharkhand", "country": "India"},
    {"city": "Deoghar", "state": "Jharkhand", "country": "India"},
    {"city": "Raipur", "state": "Chhattisgarh", "country": "India"},
    {"city": "Bhilai", "state": "Chhattisgarh", "country": "India"},
    {"city": "Bilaspur", "state": "Chhattisgarh", "country": "India"},
    {"city": "Korba", "state": "Chhattisgarh", "country": "India"},

    # Assam & Northeast
    {"city": "Guwahati", "state": "Assam", "country": "India"},
    {"city": "Silchar", "state": "Assam", "country": "India"},
    {"city": "Dibrugarh", "state": "Assam", "country": "India"},
    {"city": "Jorhat", "state": "Assam", "country": "India"},
    {"city": "Nagaon", "state": "Assam", "country": "India"},
    {"city": "Agartala", "state": "Tripura", "country": "India"},
    {"city": "Shillong", "state": "Meghalaya", "country": "India"},
    {"city": "Aizawl", "state": "Mizoram", "country": "India"},
    {"city": "Imphal", "state": "Manipur", "country": "India"},
    {"city": "Kohima", "state": "Nagaland", "country": "India"},
    {"city": "Dimapur", "state": "Nagaland", "country": "India"},
    {"city": "Itanagar", "state": "Arunachal Pradesh", "country": "India"},
    {"city": "Gangtok", "state": "Sikkim", "country": "India"},

    # Jammu & Kashmir / Himachal / Uttarakhand
    {"city": "Srinagar", "state": "Jammu and Kashmir", "country": "India"},
    {"city": "Jammu", "state": "Jammu and Kashmir", "country": "India"},
    {"city": "Anantnag", "state": "Jammu and Kashmir", "country": "India"},
    {"city": "Shimla", "state": "Himachal Pradesh", "country": "India"},
    {"city": "Dharamshala", "state": "Himachal Pradesh", "country": "India"},
    {"city": "Mandi", "state": "Himachal Pradesh", "country": "India"},
    {"city": "Solan", "state": "Himachal Pradesh", "country": "India"},
    {"city": "Dehradun", "state": "Uttarakhand", "country": "India"},
    {"city": "Haridwar", "state": "Uttarakhand", "country": "India"},
    {"city": "Roorkee", "state": "Uttarakhand", "country": "India"},
    {"city": "Haldwani", "state": "Uttarakhand", "country": "India"},
    {"city": "Rishikesh", "state": "Uttarakhand", "country": "India"},
]

@lru_cache(maxsize=256)
def _search_online_nominatim(q: str):
    """
    Online OpenStreetMap Nominatim geocoding for Indian cities and villages.
    Falls back gracefully on timeout, rate-limits, or offline mode.
    """
    try:
        url = (
            "https://nominatim.openstreetmap.org/search?"
            + urllib.parse.urlencode({
                "q": q,
                "countrycodes": "in",
                "format": "json",
                "addressdetails": 1,
                "featuretype": "settlement",
                "limit": 8
            })
        )
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "AnemiaScan-Medical-App/1.0 (healthcare screening tool; contact=support@anemiascan.org)"
            }
        )
        with urllib.request.urlopen(req, timeout=1.2) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = []
            for item in data:
                addr = item.get("address", {})
                city = (
                    addr.get("city")
                    or addr.get("town")
                    or addr.get("village")
                    or addr.get("hamlet")
                    or addr.get("suburb")
                    or addr.get("municipality")
                    or item.get("name")
                )
                state = addr.get("state")
                country = addr.get("country", "India")
                if city and state:
                    results.append({
                        "city": city.strip(),
                        "state": state.strip(),
                        "country": country.strip(),
                        "display": f"{city.strip()}, {state.strip()}, {country.strip()}"
                    })
            return results
    except Exception:
        # Graceful fallback: return empty list on any network error or timeout
        return []

def search_locations(query: str, limit: int = 10) -> list[dict]:
    """
    Smart hybrid search:
    1. Fast prefix/substring match against curated dataset (Dav -> Davangere, Davorlim; Ban -> Bengaluru; Mum -> Mumbai; Hyd -> Hyderabad; Vil -> Viluppuram, etc.)
    2. Online query with Nominatim for remote villages and settlements
    3. Deduplication and formatted display
    """
    q = (query or "").strip().lower()
    if len(q) < 2:
        return []

    matches = []
    seen = set()

    # 1. Local fast search
    # Exact startswith priority
    startswith_matches = []
    contains_matches = []

    for loc in INDIAN_LOCATIONS:
        city_name = loc["city"]
        state_name = loc["state"]
        country_name = loc["country"]
        key = f"{city_name.lower()}|{state_name.lower()}"

        display = f"{city_name}, {state_name}, {country_name}"
        record = {
            "city": city_name,
            "state": state_name,
            "country": country_name,
            "display": display
        }

        # Check if city starts with query or if secondary name starts with query
        city_lower = city_name.lower()
        is_prefix = (
            city_lower.startswith(q) or
            f"({q}" in city_lower or
            f" {q}" in city_lower or
            (q.startswith("ban") and "bengaluru" in city_lower) or
            (q.startswith("ben") and "bangalore" in city_lower)
        )
        if is_prefix:
            if key not in seen:
                seen.add(key)
                startswith_matches.append(record)
        elif q in city_lower or q in state_name.lower():
            if key not in seen:
                seen.add(key)
                contains_matches.append(record)

    matches.extend(startswith_matches)
    matches.extend(contains_matches)

    # 2. If fewer results than limit, query online Nominatim
    if len(matches) < limit:
        online_results = _search_online_nominatim(q)
        for res in online_results:
            key = f"{res['city'].lower()}|{res['state'].lower()}"
            if key not in seen:
                seen.add(key)
                matches.append(res)
            if len(matches) >= limit:
                break

    return matches[:limit]
