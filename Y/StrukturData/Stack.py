from StrukturData.Tower.Node import Node

class Stack:
    def __init__(self):
        self.top = None
        
    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        
    def pop(self):
        if self.top is None:
            return None
        popped_data = self.top.data
        self.top = self.top.next
        return popped_data
    
    def peek(self):
        if self.top is None:
            return None
        return self.top.data
    
    def is_empty(self):
        return self.top is None
    
    def size(self):
        count = 0
        current = self.top
        while current:
            count += 1
            current = current.next
        return count

class SistemMenu:
    def __init__(self):
        self.riwayat_menu = Stack()
        self.riwayat_menu.push("Lobi Utama")
        
    def masuk_menu(self, nama_menu):
        self.riwayat_menu.push(nama_menu)
        print(f"\n[+] Membuka layar: {nama_menu}")
        
    def kembali(self):
        if self.riwayat_menu.size() > 1:
            menu_sebelumnya = self.riwayat_menu.pop()
            print(f"\n[-] Menutup layar {menu_sebelumnya}...")
            print(f"[*] Kembali ke: {self.riwayat_menu.peek()}")
        else:
            print("\n[!] Kamu sudah berada di Lobi Utama, tidak bisa kembali lagi. Tekan 0git  untuk keluar game.")

    def menu_sekarang(self):
        return self.riwayat_menu.peek()

