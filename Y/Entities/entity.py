class Entity:
    def __init__(self, nama, hp, attack, level=1):
        self.nama = nama
        self.hp = hp
        self.hp_max = hp
        self.attack = attack
        self.level = level
        self.is_alive = True
        
    def pesan_kematian(self):
        pass

    def terima_damage(self, damage):
        """Logika universal saat karakter menerima serangan"""
        if not self.is_alive:
            return

        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            self.pesan_kematian()

    def serang(self, target):
        """Logika universal menyerang entitas lain"""
        if self.is_alive and target.is_alive:
            print(f"      {self.nama} memberikan {self.attack} DMG kepada {target.nama}!")
            target.terima_damage(self.attack)