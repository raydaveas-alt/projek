import json
import random
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
json_path = ROOT_DIR / "data"


tema_musuh = {
    "Hutan Pemula": ["M01", "M02", "M03"],            
    "Gua Lembap": ["M04", "M05", "M06", "M07"],       
    "Padang Rumput Angin": ["M08", "M09", "M10"],     
    "Reruntuhan Kuno": ["M11", "M12", "M13"],         
    "Kastil Terbengkalai": ["M14", "M15", "M16"],     
    "Gurun Pasir Panas": ["M17", "M18", "M19"],       
    "Oasis Tersembunyi": ["M20", "M21"],              
    "Lembah Racun": ["M22", "M23", "M24"],            
    "Hutan Berbisik": ["M25", "M26"],                 
    "Pegunungan Es": ["M27", "M28", "M29"],           
    "Kuil Beku": ["M28", "M29", "M30"],               
    "Danau Kaca": ["M31", "M32"],                     
    "Gunung Berapi": ["M33", "M34", "M35"],           
    "Lautan Lahar": ["M35", "M36", "M37"],            
    "Gua Kristal": ["M38", "M39", "M40"],             
    "Jembatan Langit": ["M41", "M42"],                
    "Pulau Terapung": ["M43", "M44"],                 
    "Dimensi Kesengsaraan": ["M45", "M46", "M47"],    
    "Kuil Bintang": ["M48", "M49"],                   
    "Istana Langit": ["M50", "M51", "M52"]            
}

musuh_default = ["M01", "M02", "M03"] 

def perbarui_menara():
    
    with open(json_path / "blueprint_tower.json", 'r') as file:
        data_tower = json.load(file)
        
    for lantai in data_tower:
        lokasi = lantai["nama_lokasi"]
        is_boss = lantai["is_boss"]
        
        pool_musuh = tema_musuh.get(lokasi, musuh_default)
        
        if not is_boss:
            jumlah_musuh = random.randint(2, 5)
            pasukan = random.choices(pool_musuh, k=jumlah_musuh)
            
            lantai["id_musuh"] = pasukan
            
        else:
            id_boss_lama = lantai["id_musuh"]
            
            if isinstance(id_boss_lama, list):
                id_boss_lama = id_boss_lama[0]
                
            jumlah_minions = random.randint(1, 3)
            minions = random.choices(pool_musuh, k=jumlah_minions)
            
            pasukan = [id_boss_lama] + minions
            
            lantai["id_musuh"] = pasukan

    with open(json_path / "blueprint_tower.json", 'w') as file:
        json.dump(data_tower, file, indent=4)
        
    print("[+] blueprint_tower.json berhasil diperbarui dengan sistem Multi-Enemy!")

if __name__ == "__main__":
    perbarui_menara()
