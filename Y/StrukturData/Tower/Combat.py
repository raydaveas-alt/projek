import StrukturData.Tower.Node as n
import time
import random

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.giliran_sekarang = None
        
    def TambahEntity(self, node_tree):
        giliran_berikutnya = n.Node(node_tree)
        if not self.head:
            self.head = giliran_berikutnya
            self.tail = giliran_berikutnya
            self.head.next = self.head
        else: 
            self.tail.next = giliran_berikutnya
            self.tail = giliran_berikutnya
            self.tail.next = self.head    
        
    def Mulai(self):
        self.giliran_sekarang = self.head
        return self.giliran_sekarang
        
    def NextTurn(self):
        if self.giliran_sekarang:
            self.giliran_sekarang = self.giliran_sekarang.next
            return self.giliran_sekarang
        return None
    
def siapkan_entitas_ke_arena(node_tree, arena_cll, daftar_pasukan, peran_valid):
    if node_tree.peran in peran_valid and node_tree.entitas.is_alive:
        arena_cll.TambahEntity(node_tree)
        daftar_pasukan.append(node_tree) 
    
    for bawahan in node_tree.anak:
        siapkan_entitas_ke_arena(bawahan, arena_cll, daftar_pasukan, peran_valid)
        
        
def jalankan_raid_kombat(master_tree, master_musuh_tree, arena_cll):
    pasukan_hero = []
    pasukan_musuh = []
    
    siapkan_entitas_ke_arena(master_tree, arena_cll, pasukan_hero, ["Kapten", "Anggota"])
    siapkan_entitas_ke_arena(master_musuh_tree, arena_cll, pasukan_musuh, ["Monster"])
    
    print("\n" + "="*45)
    print(f"⚔️ PERTEMPURAN DIMULAI: Menghadapi {len(pasukan_musuh)} Musuh! ")
    print("="*45)
    
    giliran_aktif = arena_cll.Mulai()
    turn = 1
    
    while True:
        hero_hidup = [h for h in pasukan_hero if h.entitas.is_alive]
        musuh_hidup = [m for m in pasukan_musuh if m.entitas.is_alive]
        
        if not hero_hidup:
            print("\n" + "="*45)
            print(" DEFEAT! Seluruh party hancur, Master terpaksa mundur dari pertempuran...")
            return False
            
        if not musuh_hidup:
            print("\n" + "="*45)
            print(" VICTORIOUS! Seluruh musuh telah dihancurkan. Lantai diselesaikan!")
            return True
            
        node_petarung = giliran_aktif.data
        entitas_aktif = node_petarung.entitas
        
        if not entitas_aktif.is_alive:
            giliran_aktif = arena_cll.NextTurn()
            continue
            
        print(f"\n[Turn {turn}]  Giliran: {entitas_aktif.nama} (HP: {entitas_aktif.hp}/{entitas_aktif.hp_max})")
        time.sleep(1) 
        
        if node_petarung.peran == "Monster":
            target_hero = random.choice(hero_hidup)
            entitas_aktif.serang(target_hero.entitas)
        else:
            target_musuh = random.choice(musuh_hidup)
            entitas_aktif.serang(target_musuh.entitas)
            
        turn += 1
        giliran_aktif = arena_cll.NextTurn()