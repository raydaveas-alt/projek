import json
from pathlib import Path
from StrukturData.Tower.LantaiTower import DoubleLinkedList

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
json_path = ROOT_DIR / "data"

def siapkan_menara():
    menara_game = DoubleLinkedList()
    try:
        with open(json_path / "blueprint_tower.json", "r") as file:
            data_100_lantai = json.load(file)
            
        for data_lantai in data_100_lantai:
            menara_game.BuatLantai(data_lantai)
            
        print("Menara 100 lantai siap dipanjat!")
        return menara_game
        
    except FileNotFoundError:
        print("Error: blueprint_tower.json belum dibuat!")
        return None

# menara_mc = siapkan_menara()

# print(f"Pemain berada di: Lantai {menara_mc.lantai_sekarang.data['no_lantai']} - {menara_mc.lantai_sekarang.data['nama_lokasi']}")
# menara_mc.NaikLantai()
# print(f"Pemain berada di: Lantai {menara_mc.lantai_sekarang.data['no_lantai']} - {menara_mc.lantai_sekarang.data['nama_lokasi']}")
