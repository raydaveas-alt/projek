import json

MAX_STAR_LEVEL = 7


# Load data hero dari file
def load_heroes(filename):
    with open(filename, "r") as f:
        return json.load(f)


# Simpan kembali ke file
def save_heroes(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# syarat evolusi
def can_evolve(hero):
    # Contoh aturan:
    # - Level minimal 10
    # - Star belum maksimal
    if hero["star_level"] >= MAX_STAR_LEVEL:
        return False

    if hero["level"] < 10:
        return False

    return True


# Fungsi evolusi
def evolve_hero(hero):
    if can_evolve(hero):
        hero["star_level"] += 1

        # Upgrade stat
        hero["hp"] += 20
        hero["attack"] += 5

        return True

    return False


# Evolusi berdasarkan ID
def evolve_by_id(data, hero_id):
    if hero_id in data:
        hero = data[hero_id]

        if evolve_hero(hero):
            print(f"{hero['name']} naik ke ⭐{hero['star_level']}")
        else:
            print(f"{hero['name']} tidak bisa evolusi")

    return data



heroes = load_heroes("heroBlueprints.json")
heroes = evolve_by_id(heroes, "H001") # Ini nanti dalam menu utama ato game misal mau si player 2 yg evolusi atau semacam itu
save_heroes("heroBlueprints.json", heroes)