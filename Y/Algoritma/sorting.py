# =============================================
# sorting.py - Modul Sorting Hero
# =============================================
# Menyediakan fungsi sorting hero di Barrack
# dengan beberapa algoritma dan kriteria.
# =============================================


def bubble_sort_by_level(heroes: list, ascending: bool = False) -> list:
    """
    Mengurutkan list Hero berdasarkan level
    menggunakan algoritma Bubble Sort.

    Parameter:
        heroes    : list of Hero object
        ascending : True = level terkecil dulu, False = terbesar dulu (default)

    Return:
        list Hero yang sudah terurut (sorted copy)
    """
    hasil = heroes[:]
    n = len(hasil)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            a = hasil[j].level
            b = hasil[j + 1].level

            if ascending:
                kondisi = a > b
            else:
                kondisi = a < b

            if kondisi:
                hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]

    return hasil


def selection_sort_by_star(heroes: list, ascending: bool = False) -> list:
    """
    Mengurutkan list Hero berdasarkan bintang (star_level)
    menggunakan algoritma Selection Sort.

    Parameter:
        heroes    : list of Hero object
        ascending : True = bintang terkecil dulu, False = terbesar dulu (default)

    Return:
        list Hero yang sudah terurut (sorted copy)
    """
    hasil = heroes[:]
    n = len(hasil)

    for i in range(n):
        idx_terpilih = i

        for j in range(i + 1, n):
            a = hasil[j].star_level
            b = hasil[idx_terpilih].star_level

            if ascending:
                kondisi = a < b
            else:
                kondisi = a > b

            if kondisi:
                idx_terpilih = j

        hasil[i], hasil[idx_terpilih] = hasil[idx_terpilih], hasil[i]

    return hasil


def insertion_sort_by_name(heroes: list, ascending: bool = True) -> list:
    """
    Mengurutkan list Hero berdasarkan nama secara alfabetis
    menggunakan algoritma Insertion Sort.

    Parameter:
        heroes    : list of Hero object
        ascending : True = A-Z (default), False = Z-A

    Return:
        list Hero yang sudah terurut (sorted copy)
    """
    hasil = heroes[:]
    n = len(hasil)

    for i in range(1, n):
        kunci = hasil[i]
        j = i - 1

        if ascending:
            while j >= 0 and hasil[j].nama.lower() > kunci.nama.lower():
                hasil[j + 1] = hasil[j]
                j -= 1
        else:
            while j >= 0 and hasil[j].nama.lower() < kunci.nama.lower():
                hasil[j + 1] = hasil[j]
                j -= 1

        hasil[j + 1] = kunci

    return hasil


# =============================================
# Fungsi Tampilan (UI) untuk menu Daftar Hero
# =============================================

def tampilkan_daftar(heroes: list):
    """Menampilkan list hero ke layar."""
    if not heroes:
        print("[Kosong] Tidak ada hero untuk ditampilkan.")
        return

    print(f"\n{'='*45}")
    print(f"  Total: {len(heroes)} Hero")
    print(f"{'='*45}")
    for hero in heroes:
        hero.tampilkan_stats()
        print()


def menu_daftar_hero(barrack_aktif: dict):
    """
    Menampilkan menu daftar hero dengan pilihan sorting.
    Dipanggil dari main.py saat layar_sekarang == "Daftar Hero".

    Parameter:
        barrack_aktif : dict { hero_id: Hero }
    """
    if not barrack_aktif:
        print("[Kosong] Kamu belum punya hero. Gacha dulu sana!")
        input("Tekan Enter untuk kembali...")
        return

    kumpulan_hero = list(barrack_aktif.values())

    while True:
        print("--- DAFTAR HERO (SORTING) ---")
        print("1. Urutkan by Level    (Tertinggi → Terendah) [Bubble Sort]")
        print("2. Urutkan by Level    (Terendah → Tertinggi) [Bubble Sort]")
        print("3. Urutkan by Bintang  (Tertinggi → Terendah) [Selection Sort]")
        print("4. Urutkan by Bintang  (Terendah → Tertinggi) [Selection Sort]")
        print("5. Urutkan by Nama     (A → Z)                [Insertion Sort]")
        print("6. Urutkan by Nama     (Z → A)                [Insertion Sort]")
        print("0. Kembali ke Barrack")

        pilihan = input("> Pilih urutan: ").strip()

        if pilihan == "1":
            hasil = bubble_sort_by_level(kumpulan_hero, ascending=False)
            tampilkan_daftar(hasil)
            input("Tekan Enter untuk lanjut...")

        elif pilihan == "2":
            hasil = bubble_sort_by_level(kumpulan_hero, ascending=True)
            tampilkan_daftar(hasil)
            input("Tekan Enter untuk lanjut...")

        elif pilihan == "3":
            hasil = selection_sort_by_star(kumpulan_hero, ascending=False)
            tampilkan_daftar(hasil)
            input("Tekan Enter untuk lanjut...")

        elif pilihan == "4":
            hasil = selection_sort_by_star(kumpulan_hero, ascending=True)
            tampilkan_daftar(hasil)
            input("Tekan Enter untuk lanjut...")

        elif pilihan == "5":
            hasil = insertion_sort_by_name(kumpulan_hero, ascending=True)
            tampilkan_daftar(hasil)
            input("Tekan Enter untuk lanjut...")

        elif pilihan == "6":
            hasil = insertion_sort_by_name(kumpulan_hero, ascending=False)
            tampilkan_daftar(hasil)
            input("Tekan Enter untuk lanjut...")

        elif pilihan == "0":
            break

        else:
            print("[!] Pilihan tidak valid.")
            input("Tekan Enter untuk lanjut...")
