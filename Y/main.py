# ██████╗ ██╗ ██████╗██╗  ██╗    ███╗   ███╗███████╗    ██╗   ██╗██████╗ 
# ██╔══██╗██║██╔════╝██║ ██╔╝    ████╗ ████║██╔════╝    ██║   ██║██╔══██╗
# ██████╔╝██║██║     █████╔╝     ██╔████╔██║█████╗      ██║   ██║██████╔╝
# ██╔═══╝ ██║██║     ██╔═██╗     ██║╚██╔╝██║██╔══╝      ██║   ██║██╔═══╝ 
# ██║     ██║╚██████╗██║  ██╗    ██║ ╚═╝ ██║███████╗    ╚██████╔╝██║     
# ╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝
import json
import random
import sys
import os
from pathlib import Path

from Entities.hero import Hero
from Entities.enemy import Enemy 
from Entities.entity import Entity
from StrukturData.Tree import RaidNode
from StrukturData.HashTable import HashTable
from StrukturData.Tower.Combat import CircularLinkedList, jalankan_raid_kombat
from StrukturData.Tower.MainTower import siapkan_menara

ROOT_DIR = Path(__file__).resolve().parent
json_path = ROOT_DIR / "data"

ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))


from StrukturData.Stack import Stack
from StrukturData.Queue import Queue 
import random

barrack_aktif = {} 
graveyard = set()
Daftar_Hero = HashTable(400)
n = 1

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def muat_hero():
    with open(json_path / "heroBlueprints.json", "r") as file:
        hero_data = json.load(file)
        
    for hero_id, hero_info in hero_data.items():
        Daftar_Hero.tambah(hero_id, hero_info)
        
    print(f"[Info] {len(hero_data)} Hero berhasil dimuat ke dalam Hash Table!")
        
    
def proses_gacha(id_antrian):
    
    pool_bintang = {1: [], 2: [], 3: [], 4: [], 5: []}
    
    for hero_id, hero_data in Daftar_Hero.ambilsemua():
        if hero_id not in barrack_aktif and hero_id not in graveyard and hero_id not in id_antrian:
            bintang = hero_data['star_level']
            pool_bintang[bintang].append(hero_id)
            
    if all(len(pool) == 0 for pool in pool_bintang.values()):
        print("\nGACHA GAGAL: Semua pahlawan di dunia ini sudah terpanggil atau telah gugur.")
        return None

    bobot_dasar = {
        5: 0.5,   # Bintang 5: 0.5%
        4: 1.5,   # Bintang 4: 1.5%
        3: 5.0,   # Bintang 3: 5.0%
        2: 20.0,  # Bintang 2: 20.0%
        1: 73.0   # Bintang 1: 73.0% 
    }
    
    bintang_tersedia = []
    bobot_tersedia = []
    
    for bintang in range(1, 6):
        if len(pool_bintang[bintang]) > 0:
            bintang_tersedia.append(bintang)
            bobot_tersedia.append(bobot_dasar[bintang])
            
    bintang_terpilih = random.choices(bintang_tersedia, weights=bobot_tersedia, k=1)[0]
    
    id_terpilih = random.choice(pool_bintang[bintang_terpilih])
    data_mentah = Daftar_Hero.cari(id_terpilih)
    
    hero_baru = Hero(data_mentah)
    return hero_baru

def cek_kematian(daftar_party):
    id_yang_mati = []
    
    for hero_id, hero_obj in barrack_aktif.items():
        if not hero_obj.is_alive:
            id_yang_mati.append(hero_id)
            
    for hero_id in id_yang_mati:
        nama = barrack_aktif[hero_id].nama
        print(f"MEMORIAL: {nama} telah dipindahkan ke Memory Hall. Kematiannya tak akan dilupakan ")
        graveyard.add(hero_id)
        del barrack_aktif[hero_id]
        
        for anggota in daftar_party.values():
            if hero_id in anggota:
                anggota.remove(hero_id)
                
# def cek_status(node_party):
#     for anggota in node_party.anak:
#         if anggota.entitas.is_alive and anggota.entitas.hp <= 0.2 * anggota.entitas.hp_max:
#             print(anggota.entitas.nama, "sekarat")
#         if anggota.peran in ["Master", "Kapten", "Anggota"]:
#             cek_status(node_party)
    

def main():
    antrean_gacha = Queue()
    navigasi = Stack()
    muat_hero()
    menara_game = siapkan_menara()
    daftar_party = {"Party 1": []}
    id_dalam_antrean = set()
    
    navigasi.push("Lobi Utama")
    
    while True:
        bersihkan_layar()
        
        layar_sekarang = navigasi.peek()
        
        print("="*45)
        print(f"POSISI SEKARANG: {layar_sekarang.upper()}")
        print("="*45)
        
        # ==========================================
        # LOGIKA MENU: LOBI UTAMA
        # ==========================================
        if layar_sekarang == "Lobi Utama":
            print("1. Pergi ke Summon Hall (Gacha)")
            print("2. Pergi ke Barrack (Atur Party)")
            print("3. Pergi ke Tower Gate ")
            print("0. Keluar dari Game")
            
            pilihan = input("> Pilih aksi (0-3): ")
            
            if pilihan == "1":
                navigasi.push("Summon Hall")  
            elif pilihan == "2":
                navigasi.push("Barrack")
            elif pilihan == "3":
                navigasi.push("Tower Gate")
            elif pilihan == "0":
                print("Menyimpan progres... Sampai jumpa, Master!")
                break 
            else:
                input("Pilihan tidak valid! (Tekan Enter untuk lanjut)")

        # ==========================================
        # LOGIKA MENU: BARRACK
        # ==========================================
        elif layar_sekarang == "Barrack":
            print("1. Lihat Daftar Hero (Sorting)")
            print("2. Cari Hero Spesifik (Searching)")
            print("3. Atur Party")
            print("0. KEMBALI ke Lobi Utama")
            
            pilihan = input("> Pilih aksi (0-3): ")
            
            if pilihan == "1":
                navigasi.push("Daftar Hero") 
            elif pilihan == "2":
                navigasi.push("Cari Hero")
            elif pilihan == "3":
                navigasi.push("Party")
            elif pilihan == "0":
                navigasi.pop() 

        # ==========================================
        # LOGIKA MENU: DAFTAR HERO (Sub-menu Barrack)
        # ==========================================
        elif layar_sekarang == "Daftar Hero":
            kumpulan_hero = list(barrack_aktif.values()) 
            for hero in kumpulan_hero:
                hero.tampilkan_stats()
            print("\n0. KEMBALI ke Barrack")
            
            pilihan = input("> Pilih aksi: ")
            
                
            if pilihan == "0":
                navigasi.pop()
                

        # ==========================================
        # LOGIKA MENU: ATUR PARTY
        # ==========================================
        elif layar_sekarang == "Party":
            
            hero_terpakai = set()
            for anggota in daftar_party.values():
                for h_id in anggota:
                    hero_terpakai.add(h_id)

            print("--- DAFTAR HERO TERSEDIA ---")
            if not barrack_aktif:
                print("[Kosong] Kamu belum punya hero. Gacha dulu sana!")
            else:
                ada_hero_nganggur = False
                for h_id, hero in barrack_aktif.items():
                    if h_id not in hero_terpakai:
                        print(f"ID: {h_id} | {hero.nama} ({hero.star_level}⭐): Lv.{hero.level}")
                        ada_hero_nganggur = True
                
                if not ada_hero_nganggur:
                    print("- Semua heromu sudah ditugaskan ke medan tempur! -")
            
            print("\n--- SLOT PARTY ---")
            for nama_party, anggota in daftar_party.items():
                status = f"{len(anggota)}/5 Hero" if anggota else "KOSONG"
                print(f"- {nama_party} : [{status}]")
                
            print("\n1. Edit Party") 
            print("9. Tambah Slot Party Baru") 
            print("0. KEMBALI ke Barrack")
            
            pilihan = input("> Pilih aksi: ")
            
            if pilihan == "1":
                target_party = input("\nMasukkan nama party yang ingin diedit (Cth: Party 1): ")
                lst_nama = []
                
                if target_party not in daftar_party:
                    print(f"[!] Gagal: {target_party} tidak ditemukan!")
                    input("Tekan Enter untuk kembali...")
                else:
                    print(f"\n[MENGEDIT {target_party.upper()}]")                    
                    print("(Hero yang sedang dipakai di party ini bisa dimasukkan kembali)")
                    
                    for i in range(1, 6):
                        if i == 1:
                            lst_nama.append(input("Masukkan NAMA KAPTEN (Kosongkan jika tidak ada): ").strip())
                        else:
                            lst_nama.append(input(f"Masukkan NAMA ANGGOTA {i-1} (Kosongkan jika tidak ada): ").strip())
                    
                    nama_dimasukkan = [nama for nama in lst_nama if nama != ""]
                    
                    id_dimasukkan = []
                    valid = True
                    
                    for nama_target in nama_dimasukkan:
                        id_ditemukan = None
                        
                        for h_id, hero_obj in barrack_aktif.items():
                            if hero_obj.nama.lower() == nama_target.lower():
                                id_ditemukan = h_id
                                break
                        
                        if id_ditemukan is None:
                            print(f"[!] Gagal: Hero dengan nama '{nama_target}' tidak ada di Barrack!")
                            valid = False
                            break
                            
                        for nama_p, anggota_p in daftar_party.items():
                            if nama_p != target_party and id_ditemukan in anggota_p:
                                print(f"[!] Gagal: {barrack_aktif[id_ditemukan].nama} sedang bertugas di {nama_p}!")
                                valid = False
                                break
                                
                        if not valid:
                            break
                            
                        id_dimasukkan.append(id_ditemukan)
                    
                    if not valid:
                        input("Tekan Enter untuk lanjut...")
                        
                    if valid:
                        daftar_party[target_party] = id_dimasukkan
                        print(f"[+] {target_party} berhasil disimpan dengan {len(id_dimasukkan)} Hero!")
                        input("Tekan Enter untuk lanjut...")

            elif pilihan == "9":
                nomor_baru = len(daftar_party) + 1
                nama_baru = f"Party {nomor_baru}"
                
                daftar_party[nama_baru] = []
                print(f"\n[+] {nama_baru} berhasil dibuat! Gunakan menu Edit untuk mengisi hero.")
                input("Tekan Enter untuk lanjut...")
                    
            elif pilihan == "0":
                navigasi.pop()

        # ==========================================
        # LOGIKA MENU: SUMMON HALL
        # ==========================================
        elif layar_sekarang == "Summon Hall":
            print(f"--- ANTREAN KLAIM: {antrean_gacha.size()} Hero Menunggu ---")
            print("-" * 45)
            
            print("1. Tarik 10x Hero Baru (Gacha)")
            print("2. Klaim 1 Hero dari Antrean")
            print("0. KEMBALI ke Lobi Utama")
            
            pilihan = input("> Pilih aksi: ")
            
            if pilihan == "1":
                print("\n[+] Menarik 10 Hero ke dalam antrean...")
                for i in range(10):
                    hero_gacha = proses_gacha(id_dalam_antrean)
                    
                    if hero_gacha:
                        antrean_gacha.enqueue(hero_gacha)
                        id_dalam_antrean.add(hero_gacha.id) 
                
                input("Gacha selesai! 10 Hero telah masuk antrean. (Tekan Enter)")
                
            elif pilihan == "2":
                if antrean_gacha.is_empty():
                    input("\n[!] Antrean kosong! Kamu harus Gacha dulu. (Tekan Enter)")
                else:
                    hero_diklaim = antrean_gacha.dequeue()
                    id_dalam_antrean.remove(hero_diklaim.id)
                    barrack_aktif[hero_diklaim.id] = hero_diklaim 
                    
                    print(f"[+] Berhasil memanggil: {hero_diklaim.nama} ({hero_diklaim.star_level}⭐)")
                    input("Hero telah dimasukkan ke Inventory. (Tekan Enter)")
                    
            elif pilihan == "0":
                navigasi.pop()
                
                
        # ==========================================
        # LOGIKA MENU: TOWER GATE
        # ==========================================
        elif layar_sekarang == "Tower Gate":
            print("1. Panjat Tower")
            print("2. Eksplorasi")
            print("0. KEMBALI ke Lobi Utama")
            
            pilihan = input("> Pilih aksi (0-3): ")
            
            if pilihan == "1":
                navigasi.push("Tower")  # Pindah menu = Push
            elif pilihan == "2":
                navigasi.push("Eksplorasi")
            elif pilihan == "0":
                navigasi.pop()
            else:
                input("Pilihan tidak valid! (Tekan Enter untuk lanjut)")
                
                
        # ==========================================
        # LOGIKA MENU: TOWER (PILIH LANTAI)
        # ==========================================
        elif layar_sekarang == "Tower":
            print("--- MENU PANJAT TOWER ---")
            
            lantai_tersedia = []
            current_node = menara_game.head
            
            while current_node is not None:
                data_l = current_node.data
                
                is_puncak = (current_node == menara_game.lantai_sekarang)
                if is_puncak or not data_l['is_boss']:
                    lantai_tersedia.append(current_node)
                
                if is_puncak:
                    break
                    
                current_node = current_node.next
                
            print("Pilih lantai untuk pertempuran:")
            for idx, node_lantai in enumerate(lantai_tersedia):
                data = node_lantai.data
                status = "[PUNCAK SAAT INI]" if node_lantai == menara_game.lantai_sekarang else "[FARMING]"
                print(f"{idx + 1}. Lantai {data['no_lantai']} - {data['nama_lokasi']} {status}")
                
            print("0. KEMBALI ke Tower Gate")
            
            pilihan = input(f"> Pilih lantai (0 - {len(lantai_tersedia)}): ")
            
            if pilihan == "0":
                navigasi.pop()
                
            elif pilihan.isdigit() and 1 <= int(pilihan) <= len(lantai_tersedia):
                lantai_pilihan = lantai_tersedia[int(pilihan) - 1]
                data_pilihan = lantai_pilihan.data
                
                print(f"\n[+] Memasuki Lantai {data_pilihan['no_lantai']} ({data_pilihan['nama_lokasi']})...")
                
                party_aktif = {k: v for k, v in daftar_party.items() if len(v) > 0}
                
                if not party_aktif:
                    print("[!] Kamu belum memiliki Party yang terisi! Atur formasi di menu Barrack terlebih dahulu.")
                    input("Tekan Enter untuk kembali...")
                    continue 
                
                list_nama_party = list(party_aktif.keys())
                
                print("\n--- DAFTAR PARTY SIAP TEMPUR ---")
                for i, nama_p in enumerate(list_nama_party, 1):
                    nama_hero = [barrack_aktif[h_id].nama for h_id in party_aktif[nama_p]]
                    print(f"{i}. {nama_p} -> [{', '.join(nama_hero)}]")
                
                master_entity = Entity("Master Whatevr", hp=999, attack=999, level=999)
                master_node = RaidNode(master_entity, "Master")
                
                party_terpilih = []
                
                is_boss = data_pilihan['is_boss']
                
                if not is_boss:
                    print("\n[Lantai Biasa] Kamu hanya diizinkan membawa 1 Party.")
                    pilih_idx = input(f"> Pilih Party (1-{len(list_nama_party)}): ")
                    
                    if pilih_idx.isdigit() and 1 <= int(pilih_idx) <= len(list_nama_party):
                        party_terpilih.append(list_nama_party[int(pilih_idx) - 1])
                    else:
                        print("[!] Pilihan tidak valid.")
                        input("Tekan Enter untuk membatalkan...")
                        continue
                else:
                    print("\n[LANTAI BOSS] Kamu bisa membawa hingga 2 Party!")
                    pilih_1 = input(f"> Pilih Party PERTAMA (1-{len(list_nama_party)}): ")
                    
                    if pilih_1.isdigit() and 1 <= int(pilih_1) <= len(list_nama_party):
                        party_terpilih.append(list_nama_party[int(pilih_1) - 1])
                    else:
                        print("[!] Pilihan tidak valid.")
                        input("Tekan Enter untuk membatalkan...")
                        continue
                        
                    if len(list_nama_party) > 1:
                        pilih_2 = input(f"> Pilih Party KEDUA (Ketik 0 jika hanya ingin bawa 1 party): ")
                        if pilih_2.isdigit() and 1 <= int(pilih_2) <= len(list_nama_party) and pilih_2 != "0":
                            if pilih_2 == pilih_1:
                                print("[!] Party tidak boleh sama! Membawa 1 party saja.")
                            else:
                                party_terpilih.append(list_nama_party[int(pilih_2) - 1])

                for nama_p in party_terpilih:
                    id_anggota = party_aktif[nama_p]
                    
                    kapten_obj = barrack_aktif[id_anggota[0]]
                    kapten_node = RaidNode(kapten_obj, "Kapten")
                    
                    for h_id in id_anggota[1:]:
                        anggota_obj = barrack_aktif[h_id]
                        anggota_node = RaidNode(anggota_obj, "Anggota")
                        kapten_node.tambah_unit(anggota_node) 
                        
                    master_node.tambah_unit(kapten_node)

                print("\n[Formasi Terbentuk]")
                master_node.tampilkan_struktur_raid()
                
                master_musuh_entity = Entity("Pasukan Musuh", hp=999, attack=999)
                master_musuh_node = RaidNode(master_musuh_entity, "Master Musuh")
                
                for m_id in data_pilihan['id_musuh']:
                    cek_boss = "BOSS" in m_id 
                    
                    m_hp = 1000 if cek_boss else random.randint(105, 150)
                    m_atk = 150 if cek_boss else random.randint(15, 30)
                    
                    m_entity = Enemy(nama=m_id, hp=m_hp, atk=m_atk, is_boss=cek_boss)
                    m_node = RaidNode(m_entity, "Monster")
                    
                    master_musuh_node.tambah_unit(m_node)
                
                arena_cll = CircularLinkedList()
                
                menang = jalankan_raid_kombat(master_node, master_musuh_node, arena_cll)
                
                print("\n--- MENGEVALUASI KONDISI PASUKAN ---")
                cek_kematian(daftar_party)
                # cek_status(master_node)
                
                if menang:
                    data_pilihan['is_cleared'] = True
                    
                    print("\nLANTAI SELESAI! Memberikan Reward & Pemulihan...")
                    
                    hadiah_xp = data_pilihan['no_lantai'] * 15
                    if is_boss: hadiah_xp *= 10
                    print("Semua hero mendapatkan", hadiah_xp, "EXP")
                    
                    for nama_p in party_terpilih:
                        for h_id in daftar_party[nama_p]:
                            hero_obj = barrack_aktif[h_id]
                            
                            hero_obj.tambah_xp(hadiah_xp)
                            hero_obj.pulihkan_kondisi()
                    
                    print("═"*45 + "\n")
                    if lantai_pilihan == menara_game.lantai_sekarang:
                        if menara_game.NaikLantai():
                            print(f"\n[+] PROGRESS: Bergerak maju ke Lantai {menara_game.lantai_sekarang.data['no_lantai']}")
                        else:
                            print(f"\n[+] TOWER CLEARED! Kamu sudah mencapai puncak menara!")
                    else:
                        print(f"\n[+] berhasil menyelesaikan lantai {data_pilihan["no_lantai"]}")
                        
                            
                input("\nTekan Enter untuk kembali ke menu Tower...")
                
            else:
                input("\n[!] Pilihan tidak valid! (Tekan Enter)")



if __name__ == "__main__":
    main()