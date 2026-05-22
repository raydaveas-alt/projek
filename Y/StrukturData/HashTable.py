class HashTable():
    def __init__(self, ukuran):
        self.ukuran = ukuran
        self.table = [None] * ukuran

    def _fungsiHash(self, key):
        total = 0

        for huruf in key:
            total += ord(huruf)

        return total % self.ukuran
    
    def tambah(self, key, value):
        indeks = self._fungsiHash(key)

        if self.table[indeks] is None:
            self.table[indeks] = []

        self.table[indeks].append((key, value))

    def cari(self, key):
        indeks = self._fungsiHash(key)

        if self.table[indeks] is not None:
            for pasangan in self.table[indeks]:
                if pasangan[0] == key:
                    return pasangan[1]

        return None
    
    def cari_nama(self, nama_target):
        nama_target = nama_target.lower()
        
        for slot in self.table:
            if slot is not None:
                for pasangan in slot:
                    nama_hero = pasangan[1]['name'].lower()
                    
                    if nama_target in nama_hero:
                        return pasangan[0], pasangan[1] 
                        
        return None, None 
    
    def ambilsemua(self):
        hasil = []
        for slot in self.table:
            if slot is not None:
                for pasangan in slot:
                    hasil.append((pasangan[0], pasangan[1]))
        return hasil


# import json
# from pathlib import Path

# ROOT_DIR = Path(__file__).resolve().parent.parent
# json_path = ROOT_DIR / 'data' / 'heroBlueprints.json'

# with open(json_path, 'r') as f:
#     hero_data = json.load(f)

# database_katalog = HashTable(100)

# for hero_id, hero_info in hero_data.items():
#     database_katalog.tambah(hero_id, hero_info)

# hasil_pencarian = database_katalog.cari("H004")

# print(f"Data ditemukan: {hasil_pencarian['name']} (Bintang {hasil_pencarian['star_level']})")

