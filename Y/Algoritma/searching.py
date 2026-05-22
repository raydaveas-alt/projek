# =============================================
# search.py - Modul Pencarian Hero
# =============================================
# Menyediakan fungsi pencarian hero di Barrack
# maupun di katalog semua hero (HashTable).
# =============================================


def linear_search_barrack(barrack_aktif: dict, keyword: str) -> list:
    """
    Mencari hero di barrack (hero yang sudah dimiliki) 
    berdasarkan nama menggunakan Linear Search.
    
    Parameter:
        barrack_aktif : dict { hero_id: Hero }
        keyword       : string nama yang dicari (tidak case-sensitive)
    
    Return:
        list of Hero yang cocok
    """
    keyword = keyword.lower().strip()
    hasil = []

    for hero_obj in barrack_aktif.values():
        if keyword in hero_obj.nama.lower():
            hasil.append(hero_obj)

    return hasil


def linear_search_katalog(daftar_hero, keyword: str) -> list:
    """
    Mencari hero di katalog semua hero (HashTable)
    berdasarkan nama menggunakan Linear Search.

    Parameter:
        daftar_hero : HashTable berisi semua blueprint hero
        keyword     : string nama yang dicari (tidak case-sensitive)

    Return:
        list of tuple (hero_id, hero_data_dict) yang cocok
    """
    keyword = keyword.lower().strip()
    hasil = []

    for hero_id, hero_data in daftar_hero.ambilsemua():
        if keyword in hero_data['name'].lower():
            hasil.append((hero_id, hero_data))

    return hasil


def binary_search_by_id(barrack_aktif: dict, target_id: str):
    """
    Mencari hero di barrack berdasarkan ID tepat 
    menggunakan Binary Search (list diurutkan dulu berdasarkan ID).

    Parameter:
        barrack_aktif : dict { hero_id: Hero }
        target_id     : string ID hero (misal: "H001")

    Return:
        Hero object jika ditemukan, None jika tidak
    """
    # Urutkan list ID secara alfabetis
    daftar_id = sorted(barrack_aktif.keys())

    kiri = 0
    kanan = len(daftar_id) - 1

    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        id_tengah = daftar_id[tengah]

        if id_tengah == target_id:
            return barrack_aktif[id_tengah]
        elif id_tengah < target_id:
            kiri = tengah + 1
        else:
            kanan = tengah - 1

    return None


# =============================================
# Fungsi Tampilan (UI) untuk menu Cari Hero
# =============================================

def tampilkan_hasil(hasil: list, mode: str = "barrack"):
    """
    Menampilkan hasil pencarian ke layar.

    Parameter:
        hasil : list of Hero (mode barrack) atau list of tuple (mode katalog)
        mode  : "barrack" atau "katalog"
    """
    if not hasil:
        print("[!] Tidak ada hero yang ditemukan.")
        return

    print(f"\n{'='*45}")
    print(f"  Ditemukan {len(hasil)} hero:")
    print(f"{'='*45}")

    if mode == "barrack":
        for hero_obj in hasil:
            hero_obj.tampilkan_stats()
            print()
    elif mode == "katalog":
        for hero_id, data in hasil:
            status_barrack = ""
            print(f"[{data['star_level']}⭐] {data['name']} (ID: {hero_id})")
            print(f"    HP: {data['hp']} | ATK: {data['attack']} | Senjata: {data['equipment']['weapon']}")
            print()


def menu_cari_hero(barrack_aktif: dict, daftar_hero):
    """
    Menampilkan menu pencarian lengkap.
    Dipanggil dari main.py saat layar_sekarang == "Cari Hero".

    Parameter:
        barrack_aktif : dict hero yang dimiliki player
        daftar_hero   : HashTable semua blueprint hero
    """
    while True:
        print("--- CARI HERO ---")
        print("1. Cari di Barrack (hero yang kamu punya) - by Nama")
        print("2. Cari di Barrack (hero yang kamu punya) - by ID")
        print("3. Cari di Katalog (semua hero) - by Nama")
        print("0. Kembali")

        pilihan = input("> Pilih mode pencarian: ").strip()

        if pilihan == "1":
            if not barrack_aktif:
                print("\n[Kosong] Kamu belum punya hero di Barrack.")
                input("Tekan Enter untuk lanjut...")
                continue

            keyword = input("Masukkan nama hero: ").strip()
            if not keyword:
                print("[!] Keyword tidak boleh kosong.")
                input("Tekan Enter untuk lanjut...")
                continue

            hasil = linear_search_barrack(barrack_aktif, keyword)
            tampilkan_hasil(hasil, mode="barrack")
            input("Tekan Enter untuk lanjut...")

        elif pilihan == "2":
            if not barrack_aktif:
                print("\n[Kosong] Kamu belum punya hero di Barrack.")
                input("Tekan Enter untuk lanjut...")
                continue

            target_id = input("Masukkan ID hero (contoh: H001): ").strip().upper()
            if not target_id:
                print("[!] ID tidak boleh kosong.")
                input("Tekan Enter untuk lanjut...")
                continue

            hero = binary_search_by_id(barrack_aktif, target_id)

            print(f"\n{'='*45}")
            if hero:
                print(f"  Hero ditemukan:")
                print(f"{'='*45}")
                hero.tampilkan_stats()
            else:
                print(f"[!] Hero dengan ID '{target_id}' tidak ditemukan di Barrack.")
            print()
            input("Tekan Enter untuk lanjut...")

        elif pilihan == "3":
            keyword = input("Masukkan nama hero: ").strip()
            if not keyword:
                print("[!] Keyword tidak boleh kosong.")
                input("Tekan Enter untuk lanjut...")
                continue

            hasil = linear_search_katalog(daftar_hero, keyword)
            tampilkan_hasil(hasil, mode="katalog")
            input("Tekan Enter untuk lanjut...")

        elif pilihan == "0":
            break

        else:
            print("[!] Pilihan tidak valid.")
            input("Tekan Enter untuk lanjut...")
