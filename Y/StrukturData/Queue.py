import StrukturData.Tower.Node as n

class Queue:
    def __init__(self):
        self.front = None 
        self.rear = None   
        self._size = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, data):
        node_baru = n.Node(data)
        
        if self.rear is None:
            self.front = self.rear = node_baru
            self._size += 1
            return
            
        self.rear.next = node_baru
        self.rear = node_baru
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            return "Antrean kosong!"
            
        pop = self.front.data
        
        self.front = self.front.next
        self._size -= 1
        
        if self.front is None:
            self.rear = None
            
        return pop

    def front_item(self):
        if self.is_empty():
            return "Antrean kosong!"
        return self.front.data

    def size(self):
        return self._size
    
    def display(self):
        if self.is_empty():
            print("Antrean kosong!")
            return
        
        current = self.front
        while current:
            print(current.data)
            current = current.next
    