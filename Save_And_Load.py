import csv

def save_to_csv(filename, grid, start, end, size):
    if(filename == ""):
        return
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Baris pertama: Start, End, dan Ukuran Grid
        writer.writerow(start + end + size)
        # Baris berikutnya: Isi grid
        writer.writerows(grid)

def load_from_csv(filename):
    if(filename == ""):
        return
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
        
        # Baris pertama: Start, End, dan Ukuran Grid
        start = list(map(int, data[0][:2]))
        end = list(map(int, data[0][2:4]))
        size = list(map(int, data[0][4:]))
        
        # Baris berikutnya: Isi grid
        grid = [list(map(int, row)) for row in data[1:]]
        
        return grid, start, end, size
# Contoh data
grid = [
    [1, 1, 0, 0],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [0, 1, 0, 1],
]
start = [1, 0]
end = [3, 3]
size = [4, 4]

# Simpan ke file CSV
save_to_csv('map_data.csv', grid, start, end, size)