## fiturlantai dibuat dalam bentuk ldouble linked list agar bisa naik dan juga turun lantai dengan mudah, tanpa harus mengulang dari awal lagi 

import StrukturData.Tower.Node as n

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.lantai_sekarang = None
        
    def BuatLantai(self, data_lantai):
        lantai_baru = n.Node(data_lantai)
        if not self.head:
            self.head = lantai_baru
            self.lantai_sekarang = lantai_baru
            return
            
        current = self.head
        while current.next:
            current = current.next
        
        current.next = lantai_baru
        lantai_baru.prev = current
        
        
    def NaikLantai(self):
        if self.lantai_sekarang and self.lantai_sekarang.next:
            self.lantai_sekarang = self.lantai_sekarang.next
            return True
        return False # bakal ngembaliin false klo dah mentok di puncak tower
    
    def TurunLantai(self):
        if self.lantai_sekarang and self.lantai_sekarang.prev:
            self. lantai_sekarang = self.lantai_sekarang.prev
            return True
        return False
        
    