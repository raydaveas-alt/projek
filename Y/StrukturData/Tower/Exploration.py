import Node as n

class SingleLinkedList:
    def __init__(self):
        self.head = None
        self.pos_sekarang = None
        
    def TambahPos(self, pos):
        pos_berikutnya = n.Node(pos)
        if not self.head:
            self.head = pos_berikutnya
            return
        
        current = self.head
        while current.next:
            current = current.next
            
        current.next = pos_berikutnya
        
    def MulaiEkplorasi(self):
        self.pos_sekarang = self.head
        return self.pos_sekarang
    
    def NextPos(self):
        if self.pos_sekarang and self.pos_sekarang.next:
            self.pos_sekarang = self.pos_sekarang.next
            return self.pos_sekarang
        return None
    
# if __name__ == "__main__":
#     jalur_farming = SingleLinkedList()
    
#     jalur_farming.TambahPos({"nama_pos": "Gerbang Hutan", "drop": "Kristal Colorless"})
#     jalur_farming.TambahPos({"nama_pos": "Danau Peri", "drop": "Kristal Merah"})
#     jalur_farming.TambahPos({"nama_pos": "Gua Tambang", "drop": "Kristal Kuning"})
    
#     print("--- EKSPEDISI DIMULAI ---")
#     pos = jalur_farming.MulaiEkplorasi()
#     print(f"Party tiba di: {pos.data['nama_pos']} | Mendapat: {pos.data['drop']}")
    
#     print("\n...Party melanjutkan perjalanan...")
#     pos = jalur_farming.NextPos()
#     print(f"Party tiba di: {pos.data['nama_pos']} | Mendapat: {pos.data['drop']}")
    
#     print("\n...Party melanjutkan perjalanan...")
#     pos = jalur_farming.NextPos()
#     print(f"Party tiba di: {pos.data['nama_pos']} | Mendapat: {pos.data['drop']}")
    
#     print("\n...Party melanjutkan perjalanan...")
#     pos = jalur_farming.NextPos()
#     if pos is None:
#         print("EKSPEDISI SELESAI! Party kembali ke Base Camp.")