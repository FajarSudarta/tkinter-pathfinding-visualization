from tkinter import *
from A_Star import a_star
from A_Star_Debug import a_Star_Debug
from Djikstra_Debug import djikstra_Debug
from Djikstra import djikstra_path
from tkinter import messagebox
from tkinter import filedialog
from Share import Share_Func
from Save_And_Load import save_to_csv ,load_from_csv

import time
import os
os.system('cls')


def GenerateCellButton(Mapsize:tuple,width:int,height:int,bg_color:str,font:str):
    """
    Fungsi untuk men-generate node pada layar
    """
    global Grid_Frame
    
   
    Result = [[None for _ in range(MapSize[0])] for _ in range(MapSize[1])]
    for A in range(MapSize[1]):
        for B in range(MapSize[0]):
           Result[A][B] = Button(Grid_Frame,width=width,height=height,font=(font,10),bg=bg_color)
           Result[A][B].grid(row=A,column=B)
           Result[A][B].config(command=lambda Objek = Result[A][B] : Onclick(Object=Objek))
    
    return Result

def Generate_Func():
    """
    Fungsi yang terhubung dengan button generate grid
    """
    global MapSize
    global End
    global Start
    global GridMap
    
    try:
        Panjang,Lebar = int(Input_Panjang.get()),int(Input_Lebar.get())
        if([Panjang,Lebar] == MapSize):
            return
        if(Panjang < 5 or Lebar < 5):
            messagebox.showinfo(title="Kekecilan",message="Grid Kekecilan")
            return
        if(Panjang > 31 or Lebar > 18):
            messagebox.showinfo(title="Kebesaran",message="Grid Kebesaran")
            return
        
    except:
        messagebox.showerror(title="Error",message="Invalid Input")
        return
    Destroy_Button()
    MapSize = [Panjang,Lebar]
    Start = [0,0]
    End = [MapSize[1]-1,MapSize[0]-1]
    GridMap = GenerateCellButton(MapSize,4,2,"White","Arial")
    Set_Early_Node()

def Destroy_Button():
    """
    Fungsi untuk menghancurkan semua tombol sebelum mengenerate ulang.
    """
    global GridMap
    for a in GridMap:
        for b in a:
            b.destroy()

def State_Func():
    """
    Fungsi yang terhubung ke State_Button 
    untuk mengubah input klik mouse antara meletakkan collider atau Start dan End
    """
    global Mode
    if(State_Btn.cget('text') != "Place Collider"):
        Mode = "Place Collider"
        State_Btn.config(text=Mode)
        window.title("Pathfinding: " + Mode)
        return
    if(State_Btn.cget('text') != "Place Start/End"):
        Mode = "Place Start/End"
        State_Btn.config(text=Mode)
        window.title("Pathfinding: " + Mode)
        return

def Onclick(Object:Button):
    """
    Fungsi yang terhubung ke setiap tombol node pada aplikasi.
    
    """
    if(Simulate_Btn.cget('text') == "Stop"):
        return
    global Mode
    global Start_End_State
    row:int = Object.grid_info().get('row')
    column:int = Object.grid_info().get('column')
    match Mode:
        case "Place Collider":
            Set_Open_And_Close_Node(Object,[row,column])
            return
        case "Place Start/End":
            match Start_End_State:
                case "SETSTART":
                    Set_StartEND_Node([row,column],"Start")
                    Start_End_State = "SETEND"
                    return
                case "SETEND":
                    Set_StartEND_Node([row,column],"End")
                    Start_End_State = "SETSTART"
                    return
    
def Set_Open_And_Close_Node(Object:Button,Obj_pos:list[int]):
    """
    Fungsi Untuk mengubah suatu Node jadi jalur terbuka ataupun buntu
    """
    global Start,End
    if(Obj_pos == Start or Obj_pos == End):
        return
    Object_Color = Object.cget("bg")
    if(Object_Color == "White"):
        Object.config(bg="Black",text="")
    elif(Object_Color == "Black"):
         Object.config(bg="White",text="")
    else:
        Object.config(bg="Black",text="")

    
def Set_StartEND_Node(New:list[int],Set:str):
    """
    Fungsi untuk mengubah suatu Node menjadi Start_Node ataupun End_Node
    """
    global Start
    global End
    global GridMap
    cur: Button = GridMap[New[0]][New[1]]
    Start_Btn : Button = GridMap[Start[0]][Start[1]]
    End_Btn : Button = GridMap[End[0]][End[1]]
    

    if(cur.cget("bg")=="Black"):
        return
    if(New == Start or New == End):
        
        if(Set != cur.cget('text')):
            A = Start
            Start = End
            End = A
            Set_Early_Node()
        return
    if(Set == "Start"):
        Start_Btn.config(bg="White",text="")
        Start = New
        cur.config(bg="Orange",text="Start")
    else:
        End_Btn.config(bg="White",text="")
        End = New
        cur.config(bg="Red",text="End")

def Set_Early_Node():
    """
    Berfungsi untuk meng-update posisi Start dan End
    """
    print("test")
    global Start
    global End
    global GridMap
    Start_Btn : Button = GridMap[Start[0]][Start[1]]
    End_Btn : Button = GridMap[End[0]][End[1]]
    Start_Btn.config(bg="Orange",text="Start")
    End_Btn.config(bg="Red",text="End")

def Delete_Collider():
    """
    Berfungsi untuk me-reset semua jalan buntu
    """
    global GridMap
    value = messagebox.askokcancel(title="Apa kamu yakin?",message="Apakah kamu mau melanjutkan?")
    if(value == False):
        return
    for a in GridMap:
        for b in a:
            curr: Button = b
            color = curr.cget('bg')
            if(color == "Orange"):
                continue
            if(color == "Red"):
                continue
            curr.config(bg="White",text="")
            
def Clear_Path():
    """
    Membersihkan bekas hasil dari proses pencarian sebelumnya
    """
    global GridMap               
    for a in GridMap:
        for b in a:
            curr: Button = b
            color = curr.cget('bg')
            if(color == "Orange"):
                continue
            if(color == "Red"):
                continue
            if(color == "Black"):
                continue
            curr.config(bg="White",text="")
def Debug_Func(Object:Button):
    """
    Fungsi yang terhubung ke tombol visualise
    """
    if(Object.cget('text') == "Visualize: False"):
        Object.config(text="Visualize: True")
    else:
        Object.config(text="Visualize: False")

def Gerak_Func():
    """
    Memilih gaya gerakan dari suatu algoritma pathfinding
    """
    global Gerak
    info = Move_Style_Btn.cget("text")
    if(info == "Gerak: TopDown"):
        Gerak = "AllDirection"
        Move_Style_Btn.config(text="Gerak: AllDirection")
    else:
        Gerak = "TopDown"
        Move_Style_Btn.config(text="Gerak: TopDown")

def Algorithm_Func():
    if(Algorithm_Path.cget('text') == "Algorithm: A*"):
        Algorithm_Path.config(text="Algorithm: Djikstra")
    else:
        Algorithm_Path.config(text="Algorithm: A*")
    print("Test")
    return

def Convert_Grid(GridMap):
    global MapSize
    Data_Grid = [[0 for _ in range(MapSize[0])] for _ in range(MapSize[1])]
    
    for row,A in enumerate(GridMap):
       
        for column,B in enumerate(A):
            Cur_Color = B.cget("bg")
            if(Cur_Color == "White"):
                Data_Grid[row][column] = 1
                
            elif(Cur_Color == "Black"):
                Data_Grid[row][column] = 0
                
            else:
                Data_Grid[row][column] = 1
    return Data_Grid

def Configurasi_Debug_Speed():
    global Debugging_Speed
    if(Debug_btn.cget('text') != "Visualize: True"):
        return 
    if(Debug_Speed_Entry.get() != ""):
            try:
                Debugging_Speed = float(Debug_Speed_Entry.get())
                if(Debugging_Speed > 1):
                    messagebox.showwarning(title="Terlalu lama",message="Visualisasi path terlalu lama\nMaksimal 1 detik")
                    return False
            except ValueError as b:
                messagebox.showerror(title="Error",message=f"Invalid Input for Debugging speed\n{b}")
                return False
            return True
            

def Simulate():
    global Start
    global End
    global GridMap
    global Path_Result
    global Running

    Data_Grid = Convert_Grid(GridMap)
    Check = Configurasi_Debug_Speed()
    if(Check == False):
        return
    Time_Label.config(text="Time Elapsed:")
    if(Algorithm_Path.cget('text') == "Algorithm: A*"):
      AStarPath(Data_Grid,Start,End)
    else:
        Djikstra_Path(Data_Grid,Start,End)
    if(Running == False):
            Running = True
            return
    if(Path_Result == None and Running == True):
        messagebox.showerror(title="Error",message="Lokasi tidak ditemukan")
        return
    Path_Result.pop()
    Path_Result.remove(Start)
    for i in Path_Result:
        GridMap[i[0]][i[1]].config(bg = "Green")

def Djikstra_Path(Map,Start,End):
    global GridMap
    global Path_Result
    global Gerak
    global Debugging_Speed
    global Running
    Clear_Path()
    if(Debug_btn.cget('text') == "Visualize: True"):
      
            
      Share_Func(Running)
      Configure_Widget('disabled')
      Start_Time = time.time()
      Path_Result =  djikstra_Debug(Map,Start,End,GridMap,Debugging_Speed,Grid_Frame,Gerak)
      End_Time = time.time()
      elapsed_time = End_Time - Start_Time
      print(f"Pathfinding selesai dalam {elapsed_time :.2f} detik.")
      Time_Label.config(text=f"Time Elapsed:\n{elapsed_time :.2f} detik")
      Configure_Widget('normal')
    else:
       Path_Result = djikstra_path(Map,Start,End,Gerak)
        
def AStarPath(Map,Start,End):
    global GridMap
    global Path_Result
    global Gerak
    global Debugging_Speed
    global Running
    Clear_Path()
    if(Debug_btn.cget('text') == "Visualize: True"):
       
        Share_Func(Running)
        Configure_Widget('disabled')
        Start_Time = time.time()
        Path_Result = a_Star_Debug(Map,Start,End,GridMap,Debugging_Speed,Grid_Frame,Gerak)
        End_Time = time.time()
        elapsed_time = End_Time - Start_Time
        print(f"Pathfinding selesai dalam {elapsed_time :.2f} detik.")
        Time_Label.config(text=f"Time Elapsed:\n{elapsed_time :.2f} detik")
        Configure_Widget('normal')
    else:
        Path_Result = a_star(Map,Start,End,Gerak)
   
def Stop_Func():
    global Running
    Running = False
    Share_Func(Running)
    Configure_Widget('normal')
    

def Configure_Widget(State:str):
    Clear_Path_Btn.config(state=State)
    Delele_Collider_btn.config(state=State)
    Debug_btn.config(state=State)
    Move_Style_Btn.config(state=State)
    Input_Panjang.config(state=State)
    Input_Lebar.config(state=State)
    Generate_Btn.config(state=State)
    State_Btn.config(state=State)
    Debug_Speed_Entry.config(state=State)
    Save_Btn.config(state=State)
    Load_Btn.config(state=State)
    if(State == 'disabled'):
        Simulate_Btn.config(text="Stop",command=Stop_Func)
    else:
        Simulate_Btn.config(text="Simulasikan",command=Simulate)
    return

def Save_Func():
    global Start , End, MapSize,GridMap

    File = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Simpan Map Pathfinding")
    if(File == ""):
        return
    Data = Convert_Grid(GridMap)
    save_to_csv(File,Data,Start,End,MapSize)
    print(f"Data telah tersimpan di:\n{File}")

def Load_Func():
    global Start , End, MapSize,GridMap
    File = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="Buka Map Pathfinding"
    )
    if(File == ""):
        return
    print(File)
    Grids,Start,End,Size =  load_from_csv(File)
    
    Load_Map(Grids,Size,4,2,"Arial")
    

def Load_Map(Data,SizeMap,width,height,font):
    global Grid_Frame
    global GridMap
    global MapSize
    if(SizeMap != MapSize):
        Destroy_Button()
        MapSize = SizeMap
        Result = [[None for _ in range(MapSize[0])] for _ in range(MapSize[1])]
        for A in range(MapSize[1]):
            for B in range(MapSize[0]):
                if(Data[A][B] == 1):
                    Result[A][B] = Button(Grid_Frame,width=width,height=height,font=(font,10),bg="White")
                    Result[A][B].grid(row=A,column=B)
                    Result[A][B].config(command=lambda Objek = Result[A][B] : Onclick(Object=Objek))
                elif(Data[A][B] == 0):
                    Result[A][B] = Button(Grid_Frame,width=width,height=height,font=(font,10),bg="Black")
                    Result[A][B].grid(row=A,column=B)
                    Result[A][B].config(command=lambda Objek = Result[A][B] : Onclick(Object=Objek))
        GridMap = Result
    else:
         for A in range(MapSize[1]):
            for B in range(MapSize[0]):
                if(Data[A][B] == 1):
                   
                    GridMap[A][B].config(bg="White",text="")
                elif(Data[A][B] == 0):
                    GridMap[A][B].config(bg="Black",text="")
         
    Set_Early_Node()

Running = True
Start_End_State = "SETSTART"
MapSize = [31,18]
Start = [0,0]
End = [MapSize[1]-1,MapSize[0]-1]
Mode = "Place Collider"
Gerak = "TopDown"
count = 0
Debugging_Speed = 0.002
Path_Result = []
window = Tk()

window.title("Pathfinding: " + Mode)
Grid_Frame = Frame(window)
Settings_frame = Frame(window)
Simulate_Btn = Button(Settings_frame,text="Simulasikan",font=(15),command=Simulate)
Delele_Collider_btn = Button(Settings_frame,text="Clear Collider",font=(15),command=Delete_Collider)
Debug_btn = Button(Settings_frame,text="Visualize: False",font=(15),command=lambda: Debug_Func(Debug_btn))
Clear_Path_Btn = Button(Settings_frame,text="Bersihkan",font=(15),command=Clear_Path)
Move_Style_Btn = Button(Settings_frame,text="Gerak: TopDown",font=(15),command=Gerak_Func)
Input_Panjang = Entry(Settings_frame,font=(15))
Input_Lebar = Entry(Settings_frame,font=(15))
Generate_Btn = Button(Settings_frame,font=(15),text="Generate Grid",command=Generate_Func)
State_Btn = Button(Settings_frame,font=(15),text="Place Collider",command=State_Func)
Debug_Speed_Entry = Entry(Settings_frame,font=(15))
Stop_Btn = Button(Settings_frame,font=(15),text="Stop Debugging",command=Stop_Func)
Algorithm_Path = Button(Settings_frame,font=(15),text="Algorithm: A*",command=Algorithm_Func)
Time_Label = Label(Settings_frame,font=(15),text="Time Elapsed:")
Save_Btn = Button(Settings_frame,font=(15),text="Save",command=Save_Func)
Load_Btn = Button(Settings_frame,font=(15),text="Load",command=Load_Func)

Algorithm_Path.pack(anchor=N,fill=X)
Simulate_Btn.pack(anchor=N,fill=X)
Clear_Path_Btn.pack(anchor=N,fill=X)
Delele_Collider_btn.pack(anchor=N,fill=X)
Debug_btn.pack(anchor=N,fill=X)
Move_Style_Btn.pack(anchor=N,fill=X)
Label(Settings_frame,text="Panjang Grid",font=(15)).pack(anchor=N,fill=X)
Input_Panjang.pack(anchor=N,fill=X)
Label(Settings_frame,text="Lebar Grid",font=(15)).pack(anchor=N,fill=X)
Input_Lebar.pack(anchor=N,fill=X)
Generate_Btn.pack(anchor=N,fill=X)
Label(Settings_frame,text="State",font=(15)).pack(anchor=N,fill=X)
State_Btn.pack(anchor=N,fill=X)
Label(Settings_frame,text="Visualize Speed(s)",font=(15)).pack(anchor=N,fill=X)
Debug_Speed_Entry.pack(anchor=N,fill=X)
Save_Btn.pack(anchor=N,fill=X)
Load_Btn.pack(anchor=N,fill=X)
Time_Label.pack(anchor=N,fill=X)
#Stop_Btn.pack(anchor=N,fill=X)
Grid_Frame.pack(side=LEFT)
Settings_frame.pack(side=RIGHT,fill=Y)
GridMap = GenerateCellButton(MapSize,4,2,"White","Arial")

Set_Early_Node()
window.mainloop()