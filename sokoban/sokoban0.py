from tkinter import *

def level1():
    laud = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 4, 1, 1, 1, 1, 1],
        [1, 1, 1, 4, 3, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 3, 2, 1, 1],
        [1, 1, 4, 0, 3, 3, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 4, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    return laud

def level2():
    laud = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 4, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 3, 0, 3, 2, 1, 1],
        [1, 1, 4, 0, 3, 3, 0, 1, 1, 1],
        [1, 1, 1, 0, 4, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 2, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    return laud

   

def restart_game():
    global lv1, kasutaja, obstacles, finish_points, black_tiles
    lv1 = level1()
    t.delete('all')
    draw_grid()
    kast(lv1)

raam = Tk()
raam.title("Kastimäng Sokoban")
t = Canvas(raam, width=1000, height=1000)
pxl = 100
rida = []
for horisontaal in range(0, 1001, pxl):
    element = []
    for vertikaal in range(0, 1001, pxl):
        pela = t.create_rectangle(horisontaal, vertikaal,
                                  horisontaal + pxl,
                                  vertikaal + pxl, outline="black")
        element.append(pela)
    rida.append(element)

def draw_grid():
    for y in range(10):
        for x in range(10):
            t.create_rectangle(x * pxl, y * pxl, (x + 1) * pxl, (y + 1) * pxl, outline="black")

def kast(laud):
    global kasutaja, lv1x1, lv1x2, lv1y1, lv1y2, obstacles, finish_points, black_tiles
    obstacles = []
    finish_points = []
    seinad = []
    for y in range(len(laud)):
        for x in range(len(laud[y])):
            if laud[y][x] == 1:
                sein = t.create_rectangle(x * pxl, y * pxl, x * pxl + pxl, y * pxl + pxl, fill="black")
                seinad.append((sein, x, y))
            else:
                t.itemconfig(rida[y][x], fill="white")
            if laud[y][x] == 2:
                lv1x1 = x * pxl
                lv1y1 = y * pxl
                lv1x2 = lv1x1 + pxl
                lv1y2 = lv1y1 + pxl
                kasutaja = t.create_oval(lv1x1, lv1y1, lv1x2, lv1y2, fill="orange")
            if laud[y][x] == 3:
                obstacle = t.create_rectangle(x * pxl, y * pxl, x * pxl + pxl, y * pxl + pxl, fill="red")
                obstacles.append((obstacle, x, y))
            if laud[y][x] == 4:
                finish = t.create_rectangle(x * pxl, y * pxl, x * pxl + pxl, y * pxl + pxl, fill="blue")
                finish_points.append((finish, x, y))

def liikumine(event):
    global lv1x1, lv1y1, lv1x2, lv1y2
    rx, ry = 0, 0
    if event.keysym == "Up":
        ry = -pxl
    elif event.keysym == "Down":
        ry = pxl
    elif event.keysym == "Left":
        rx = -pxl
    elif event.keysym == "Right":
        rx = pxl
    nx_lv1x1 = lv1x1 + rx
    nx_lv1y1 = lv1y1 + ry
    nx_lv1x2 = lv1x2 + rx
    nx_lv1y2 = lv1y2 + ry
    next_cell = lv1[nx_lv1y1 // pxl][nx_lv1x1 // pxl]

    if next_cell == 1:  # black cell
        return
    elif next_cell in [0, 2, 4]:  # white cell, user or finish point
        t.move(kasutaja, rx, ry)
        lv1x1 += rx
        lv1x2 += rx
        lv1y1 += ry
        lv1y2 += ry
    elif next_cell == 3:  # movable box
        box_x = nx_lv1x1 // pxl
        box_y = nx_lv1y1 // pxl
        beyond_box_x = box_x + (rx // pxl)
        beyond_box_y = box_y + (ry // pxl)
        if lv1[beyond_box_y][beyond_box_x] in [0, 2, 4]:
            lv1[box_y][box_x] = 0
            lv1[beyond_box_y][beyond_box_x] = 3
            for i, (obs, ox, oy) in enumerate(obstacles):
                if ox == box_x and oy == box_y:
                    t.move(obs, rx, ry)
                    obstacles[i] = (obs, beyond_box_x, beyond_box_y)
                    break
            for finish, fx, fy in finish_points:
                if (beyond_box_x, beyond_box_y) == (fx, fy):
                    t.itemconfig(obs, fill="purple")
            for finish, fx, fy in finish_points:
                if (beyond_box_x, beyond_box_y) == (fx, fy):
                    lv1[beyond_box_y][beyond_box_x] = 5
                    t.itemconfig(finish, fill="purple")
            t.move(kasutaja, rx, ry)
            lv1x1 += rx
            lv1x2 += rx
            lv1y1 += ry
            lv1y2 += ry

raam.bind("<Up>", liikumine)
raam.bind("<Down>", liikumine)
raam.bind("<Left>", liikumine)
raam.bind("<Right>", liikumine)
raam.bind("r", lambda event: restart_game())  # binding R key for restart

lv1 = level1()
draw_grid()
kast(lv1)
t.pack()
raam.mainloop()
