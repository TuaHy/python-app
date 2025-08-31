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

def search_football_fields(query, search_type="name"):
    """Search football fields by different criteria"""
    fields = load_football_fields()
    results = []
    
    query = query.lower().strip()
    
    for field in fields:
        if search_type == "name":
            if query in field.get("name", "").lower():
                results.append(field)
        elif search_type == "district":
            if query in field.get("district", "").lower():
                results.append(field)
        elif search_type == "city":
            if query in field.get("city", "").lower():
                results.append(field)
    
    return results

def get_football_fields_by_district(district):
    """Get all football fields in a specific district"""
    return search_football_fields(district, "district")

def get_football_fields_by_city(city):
    """Get all football fields in a specific city"""
    return search_football_fields(city, "city")