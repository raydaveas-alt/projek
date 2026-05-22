from .entity import Entity

class Enemy(Entity):
    def __init__(self, nama, hp, atk, lvl = 1, is_boss = False):
        super().__init__(nama, hp, atk, lvl)
        self.is_boss = is_boss
        
    def pesan_kematian(self):
        if self.is_boss:
            print(f"[BOSS KALAH] {self.nama} meraung membelah bumi! 'TIDAK MUNGKIN... BAGAIMANA BISA AKU KALAH?!.....'")
        else:
            print(f"[TERBUNUH] Berhasil mengalahkan {self.nama}")