class RaidNode:
    def __init__(self, objek_entitas, peran):
        self.entitas = objek_entitas 
        self.peran = peran           # "Master", "Kapten", "Anggota", "Monster"
        self.anak = []      
        
    def tambah_unit(self, node_baru):
        if self.peran == "Kapten" and len(self.anak) >= 4:
            print(f"[!] Gagal: Party Kapten {self.entitas.nama} sudah penuh.")
            return False
        
        self.anak.append(node_baru)
        return True

    def tampilkan_struktur_raid(self, level=0):
        indentasi = "    " * level
        
        print(f"{indentasi} {self.entitas.nama} ({self.peran}) - HP: {self.entitas.hp}")
        
        for unit in self.anak:
            unit.tampilkan_struktur_raid(level + 1)