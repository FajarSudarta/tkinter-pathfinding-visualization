
import heapq
from tkinter import Button,Frame
import math
from Share import Read_Value
def heuristic(a, b,gerak:str):
    # Menghitung jarak Manhattan
    if(gerak == "TopDown"):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    elif(gerak == "AllDirection"):
        #return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)



def djikstra_Debug(map_grid, start:list, end:list,Gridmap,delay:float,frame:Frame,gerak:str):
    delay = int(delay * 1000)
    print(delay)
    rows, cols = len(map_grid), len(map_grid[0])
    
    # Fungsi validasi untuk memastikan node ada di dalam grid dan bisa diakses
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and map_grid[x][y] == 1

    # Arah gerakan: atas, bawah, kiri, kanan
    #,(1,1),(1,-1),(-1,1),(-1,-1)
    directions = []
    if(gerak == "TopDown"):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    elif(gerak == "AllDirection"):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),(1,1),(1,-1),(-1,1),(-1,-1)]
    
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    # G-cost (biaya jarak dari start ke node saat ini)
    g_cost = {tuple(start): 0}
    
    # Parent node untuk merekonstruksi jalur
    parent = {tuple(start): None}
    
    while open_list and Read_Value() == True:
        # Ambil node dengan nilai F paling kecil
        _, current = heapq.heappop(open_list)
       
        Node: Button = Gridmap[current[0]][current[1]]
        if(current != start and current != end):
            Node.config(bg="Light Blue")
            frame.update()
            frame.after(delay+5)
        

        # Jika mencapai tujuan, rekonstruksi jalur
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent[tuple(current)]
            return path[::-1]  # Balikkan jalur
        
        # Periksa semua tetangga
        for dx, dy in directions:
            neighbor = [current[0] + dx, current[1] + dy]
            neighbor_tuple = tuple(neighbor)
            
            if is_valid(neighbor[0], neighbor[1]):
                # Hitung G-cost untuk tetangga
                move_cost = math.sqrt(2) if dx != 0 and dy != 0 else 1 
                tentative_g_cost = g_cost[tuple(current)] + move_cost
                
                # Jika tetangga belum dikunjungi atau G-cost lebih kecil
                if neighbor_tuple not in g_cost or tentative_g_cost < g_cost[neighbor_tuple]:
                    g_cost[neighbor_tuple] = tentative_g_cost
                    
                    heapq.heappush(open_list, (tentative_g_cost, neighbor))
                    parent[neighbor_tuple] = current
                    
                    Node = Gridmap[neighbor[0]][neighbor[1]]
                    if(neighbor != end):
                        Node.config(bg="Yellow",text=round(tentative_g_cost,1))
                        frame.update()
                        frame.after(delay)

        if(current != start and current != end):
            Gridmap[current[0]][current[1]].config(bg="Gray")
            frame.update()
            frame.after(delay)           
                    
    
    # Jika tidak ada jalur
    return None