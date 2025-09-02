import json

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent = 4)

# User management functions
def create_user(email, password, name, birthday = "", gender = ""):
    users = load_json("data/users.json")
    users.append({
        "id": len(users) + 1,
        "email": email,
        "password": password,
        "name": name,
        "birthday": birthday,
        "gender": gender,
        "avatar": ""
    })
    write_json("data/users.json", users)

def get_user_by_id(id):
    users = load_json("data/users.json")
    for user in users:
        if user["id"] == id:
            return user
    return None

def get_user_by_email(email):
    users = load_json("data/users.json")
    for user in users:
        if user["email"] == email:
            return user
    return None

def get_user_by_email_and_password(email, password):
    users = load_json("data/users.json")
    for user in users:
        if user["email"] == email and user["password"] == password:
            return user
    return None

def update_user(id, name, birthday = "", gender = ""):
    users = load_json("data/users.json")
    for user in users:
        if user["id"] == id:
            user["id"] = id
            user["name"] = name
            user["birthday"] = birthday
            user["gender"] = gender
            break
    write_json("data/users.json", users)

def update_user_avatar(id, avatar):
    users = load_json("data/users.json")
    for user in users:
        if user["id"] == id:
            user["avatar"] = avatar
            break
    write_json("data/users.json", users)

# Football fields data functions - Basic search only
def load_football_fields():
    """Load all football fields from data.json"""
    try:
        return load_json("data/data.json")
    except Exception as e:
        return []

def load_field_types():
    """Load unique field types from football fields data"""
    fields = load_football_fields()
    types = []
    seen = set()
    for field in fields:
        t = field.get("field_type", "").strip()
        if t and t not in seen:
            types.append(t)
            seen.add(t)
    return types

def filter_football_fields(city=None, field_type=None, name=None):
    """Return football fields filtered by city, field_type, and name (AND logic)."""
    fields = load_football_fields()
    results = fields
    
    if city and city != "All Cities":
        c = city.lower().strip()
        results = [f for f in results if c in f.get("city", "").lower()]
    
    if field_type and field_type != "All Types":
        t = field_type.lower().strip()
        results = [f for f in results if t in f.get("field_type", "").lower()]
    
    if name:
        q = name.lower().strip()
        results = [f for f in results if q in f.get("name", "").lower()]
    
    return results

def load_cities():
    """Load unique cities from football fields data"""
    fields = load_football_fields()
    cities = []
    seen_cities = set()
    
    for field in fields:
        city = field.get("city", "")
        if city and city not in seen_cities:
            cities.append({"id": len(cities) + 1, "name": city})
            seen_cities.add(city)
    
    return cities