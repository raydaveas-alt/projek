# =============================================
# saveload.py - Sistem Save & Load Permainan
# =============================================
# Menyimpan dan memuat state permainan ke/dari
# file JSON di folder saves/.
# =============================================

import json
import os
from datetime import datetime
from pathlib import Path

SAVE_DIR = Path(__file__).resolve().parent.parent / "saves"


def _pastikan_folder_save():
    """Buat folder saves/ jika belum ada."""
    SAVE_DIR.mkdir(exist_ok=True)


def _hero_ke_dict(hero) -> dict:
    """Konversi Hero object → dict untuk disimpan ke JSON."""
    return {
        "id":         hero.id,
        "name":       hero.nama,
        "hp":         hero.hp,
        "hp_max":     hero.hp_max,
        "attack":     hero.attack,
        "level":      hero.level,
        "star_level": hero.star_level,
        "exp":        hero.exp,
        "exp_next":   hero.exp_next,
        "is_alive":   hero.is_alive,
        "equipment":  {"weapon": hero.weapon},
    }


def _dict_ke_hero(data: dict):
    """
    Konversi dict dari JSON → Hero object.
    Mempertahankan state (level, HP, exp, dll) yang sudah ada.
    """
    from Entities.hero import Hero

    hero = Hero(data)

    # Pulihkan state yang tidak di-set oleh __init__
    hero.hp      = data["hp"]
    hero.hp_max  = data["hp_max"]
    hero.attack  = data["attack"]
    hero.level   = data["level"]
    hero.exp     = data["exp"]
    hero.exp_next = data["exp_next"]
    hero.is_alive = data["is_alive"]

    return hero


# =============================================
# FUNGSI UTAMA: SAVE
# =============================================

def simpan_permainan(
    barrack_aktif: dict,
    graveyard: set,
    daftar_party: dict,
    menara_game,
    slot: int = 1
):
    """
    Menyimpan state permainan ke file JSON.

    Parameter:
        barrack_aktif : dict { hero_id: Hero }
        graveyard     : set of hero_id yang sudah gugur
        daftar_party  : dict { nama_party: [hero_id, ...] }
        menara_game   : DoubleLinkedList (menara)
        slot          : nomor slot save (1-3, default 1)

    Return:
        True jika berhasil, False jika gagal
    """
    _pastikan_folder_save()

    try:
        # Ambil no_lantai saat ini dari menara
        no_lantai_sekarang = menara_game.lantai_sekarang.data["no_lantai"]

        data_save = {
            "waktu_simpan":       datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "no_lantai_sekarang": no_lantai_sekarang,
            "graveyard":          list(graveyard),
            "daftar_party":       daftar_party,
            "barrack_aktif":      {
                h_id: _hero_ke_dict(hero_obj)
                for h_id, hero_obj in barrack_aktif.items()
            },
        }

        path_file = SAVE_DIR / f"save_slot{slot}.json"
        with open(path_file, "w") as f:
            json.dump(data_save, f, indent=2)

        print(f"\n[✔] Permainan berhasil disimpan ke Slot {slot}!")
        print(f"    Lantai  : {no_lantai_sekarang}")
        print(f"    Hero    : {len(barrack_aktif)} di Barrack, {len(graveyard)} gugur")
        print(f"    Waktu   : {data_save['waktu_simpan']}")
        return True

    except Exception as e:
        print(f"\n[✘] Gagal menyimpan permainan: {e}")
        return False


# =============================================
# FUNGSI UTAMA: LOAD
# =============================================

def muat_permainan(menara_game, slot: int = 1):
    """
    Memuat state permainan dari file JSON.

    Parameter:
        menara_game : DoubleLinkedList yang sudah di-init (dari siapkan_menara())
        slot        : nomor slot save yang dimuat (1-3)

    Return:
        (barrack_aktif, graveyard, daftar_party) jika berhasil
        None jika gagal / file tidak ditemukan
    """
    path_file = SAVE_DIR / f"save_slot{slot}.json"

    if not path_file.exists():
        print(f"\n[!] Slot {slot} kosong. Belum ada data tersimpan.")
        return None

    try:
        with open(path_file, "r") as f:
            data_save = json.load(f)

        # Pulihkan barrack
        barrack_aktif = {}
        for h_id, hero_data in data_save["barrack_aktif"].items():
            barrack_aktif[h_id] = _dict_ke_hero(hero_data)

        # Pulihkan graveyard
        graveyard = set(data_save["graveyard"])

        # Pulihkan party
        daftar_party = data_save["daftar_party"]

        # Pulihkan posisi menara — maju sampai lantai yang tersimpan
        no_lantai_target = data_save["no_lantai_sekarang"]
        menara_game.lantai_sekarang = menara_game.head  # reset ke awal

        current = menara_game.head
        while current is not None:
            if current.data["no_lantai"] == no_lantai_target:
                menara_game.lantai_sekarang = current
                break
            current = current.next

        print(f"\n[✔] Permainan berhasil dimuat dari Slot {slot}!")
        print(f"    Lantai  : {no_lantai_target}")
        print(f"    Hero    : {len(barrack_aktif)} di Barrack, {len(graveyard)} gugur")
        print(f"    Disimpan: {data_save['waktu_simpan']}")

        return barrack_aktif, graveyard, daftar_party

    except Exception as e:
        print(f"\n[✘] Gagal memuat permainan: {e}")
        return None


# =============================================
# FUNGSI BANTU: INFO SLOT
# =============================================

def info_semua_slot() -> list:
    """
    Membaca info singkat semua slot save yang ada.

    Return:
        list of dict { slot, waktu_simpan, no_lantai, jumlah_hero }
        atau dict { slot, kosong: True } untuk slot yang belum terisi
    """
    _pastikan_folder_save()
    hasil = []

    for slot in range(1, 4):
        path_file = SAVE_DIR / f"save_slot{slot}.json"
        if path_file.exists():
            try:
                with open(path_file, "r") as f:
                    data = json.load(f)
                hasil.append({
                    "slot":         slot,
                    "kosong":       False,
                    "waktu_simpan": data.get("waktu_simpan", "-"),
                    "no_lantai":    data.get("no_lantai_sekarang", "?"),
                    "jumlah_hero":  len(data.get("barrack_aktif", {})),
                })
            except Exception:
                hasil.append({"slot": slot, "kosong": True})
        else:
            hasil.append({"slot": slot, "kosong": True})

    return hasil


# =============================================
# FUNGSI TAMPILAN (UI)
# =============================================

def tampilkan_slot():
    """Menampilkan info semua slot save ke layar."""
    slots = info_semua_slot()
    print(f"\n{'='*45}")
    print("  SLOT SAVE")
    print(f"{'='*45}")
    for s in slots:
        if s["kosong"]:
            print(f"  Slot {s['slot']} : [Kosong]")
        else:
            print(f"  Slot {s['slot']} : Lantai {s['no_lantai']} | "
                  f"{s['jumlah_hero']} Hero | {s['waktu_simpan']}")
    print(f"{'='*45}")


def menu_simpan(barrack_aktif, graveyard, daftar_party, menara_game):
    """Menu Save — dipanggil dari main.py."""
    tampilkan_slot()
    pilihan = input("Simpan ke slot mana? (1/2/3 | 0=Batal): ").strip()

    if pilihan in ("1", "2", "3"):
        simpan_permainan(barrack_aktif, graveyard, daftar_party, menara_game, int(pilihan))
    elif pilihan == "0":
        print("[Batal] Tidak jadi menyimpan.")
    else:
        print("[!] Pilihan tidak valid.")

    input("Tekan Enter untuk lanjut...")


def menu_muat(menara_game):
    """
    Menu Load — dipanggil dari main.py saat di layar utama.

    Return:
        (barrack_aktif, graveyard, daftar_party) jika berhasil dimuat
        None jika batal / gagal
    """
    tampilkan_slot()
    pilihan = input("Muat dari slot mana? (1/2/3 | 0=Batal): ").strip()

    if pilihan in ("1", "2", "3"):
        hasil = muat_permainan(menara_game, int(pilihan))
        input("Tekan Enter untuk lanjut...")
        return hasil
    elif pilihan == "0":
        print("[Batal] Tidak jadi memuat.")
    else:
        print("[!] Pilihan tidak valid.")

    input("Tekan Enter untuk lanjut...")
    return None
