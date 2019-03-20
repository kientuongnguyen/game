import pyglet


pyglet.gl.glClearColor(0,128,255,255)
window = pyglet.window.Window(fullscreen=True)
batch = pyglet.graphics.Batch()
block_size = window.width // 16
n = [2, 4, 5, 3, 7777, 15, 291]
label_list = []
index_list = []
arrow_list = []
rarrow_list = []
larrow_list = []
count = 0
onSwap = False
onInsert = False
swapState = "Pick"
insertState = "Pick"
Speed = 5
step = 0
DELAY = 20 - Speed
Delay = DELAY
RED_COLOR = (255, 0, 0, 255)
GREEN_COLOR = (0, 255, 0, 255)
BLUE_COLOR = (0, 0, 255, 255)
y_label = window.height // 2
y_arrow = y_label - 2 * block_size
y_lrarrow = y_label + 2 * block_size
arrow_img = pyglet.image.load("images/arrow.png")
larrow_img = pyglet.image.load("images/arrow_L.png")
rarrow_img = pyglet.image.load("images/arrow_R.png")
arrow_img.anchor_x = arrow_img.width // 2
larrow_img.anchor_x = larrow_img.width // 2
rarrow_img.anchor_x = rarrow_img.width // 2
arrow_img.anchor_y = arrow_img.height // 2
larrow_img.anchor_y = larrow_img.height // 2
rarrow_img.anchor_y = rarrow_img.height // 2
@window.event
def on_draw():
    window.clear()
    batch.draw()


def create_num_list(n):
    global label_list
    t = 0
    if len(n) % 2 == 0:
        t = block_size // 2
    for i in range(len(n)):
        x_position = (window.width // 2 - (len(n) // 2 * block_size) + t) + i * block_size
        index_list.append(pyglet.text.Label(str(i),  bold=True, font_size=20,
                          x=x_position,
                          y=window.height // 2 - 3 * block_size, anchor_x = "center",
                          anchor_y = "center", batch=batch))
        label_list.append(pyglet.text.Label(str(n[i]),  bold=True, font_size=30,
                          x=x_position,
                          y=y_label, anchor_x = "center",
                          anchor_y = "center", batch=batch))
        arrow_list.append(pyglet.sprite.Sprite(img=arrow_img, x=x_position,
                          y=y_arrow, batch=batch))
        larrow_list.append(pyglet.sprite.Sprite(img=larrow_img, x=x_position - 5,
                          y=y_lrarrow, batch=batch))
        rarrow_list.append(pyglet.sprite.Sprite(img=rarrow_img, x=x_position + 5,
                          y=y_lrarrow, batch=batch))
        arrow_list[i].scale = 0.1
        arrow_list[i].scale_y = -1
        arrow_list[i].visible = False
        larrow_list[i].scale = 0.1
        larrow_list[i].visible = False
        rarrow_list[i].scale = 0.1
        rarrow_list[i].visible = False
        label_list[i].width = block_size
        while label_list[i].content_width > label_list[i].width:
            label_list[i].font_size -= 1


def swap(label_list, a, b):
    if a > b:
        a, b = b, a
    global swapState
    global onSwap
    if swapState == "Pick":
        label_list[a].y += Speed
        label_list[b].y -= Speed
        if label_list[a].y - y_label >= block_size:
            swapState = "Move"
    elif swapState == "Move":
        label_list[a].x += Speed
        label_list[b].x -= Speed
        if label_list[a].x >= index_list[b].x:
            swapState = "Drop"
    elif swapState == "Drop":
        label_list[a].y -= Speed
        label_list[b].y += Speed
        if label_list[a].y == y_label:
            swapState = "Pick"
            onSwap = False
            label_list[a], label_list[b] = label_list[b], label_list[a]

def insert(label_list, a, b):
    global insertState
    global onInsert
    if a < b:
        if insertState == "Pick":
            if label_list[a].y + Speed > y_label + block_size:
                label_list[a].y = y_label + block_size
            else:
                label_list[a].y += Speed
            if label_list[a].y - y_label == block_size:
                insertState = "Push"
        elif insertState == "Push":
            speed = Speed
            if label_list[a + 1].x - Speed < label_list[a].x:
                speed = label_list[a].x - label_list[a + 1].x
            for i in range(len(label_list)):
                if i > a and i <= b:
                    label_list[i].x -= speed
            if label_list[a + 1].x == label_list[a].x:
                insertState = "Move"
        elif insertState == "Move":
            if label_list[a].x + Speed > index_list[b].x:
                label_list[a].x = index_list[b].x
            else:
                label_list[a].x += Speed
            if label_list[a].x == index_list[b].x:
                insertState = "Drop"
        elif insertState == "Drop":
            if label_list[a].y - Speed < y_label:
                label_list[a].y = y_label
            else:
                label_list[a].y -= Speed
            if label_list[a].y == y_label:
                onInsert = False
                insertState = "Pick"
                temp = label_list[a]
                for lb in range(a, b):
                    label_list[lb] = label_list[lb + 1]
                label_list[b] = temp
    elif a > b:
        if insertState == "Pick":
            if label_list[a].y + Speed > y_label + block_size:
                label_list[a].y = y_label + block_size
            else:
                label_list[a].y += Speed
            if label_list[a].y - y_label == block_size:
                insertState = "Push"
        elif insertState == "Push":
            speed = Speed
            if label_list[a - 1].x + Speed > label_list[a].x:
                speed = label_list[a].x - label_list[a - 1].x
            for i in range(len(label_list)):
                if i >= b and i < a:
                    label_list[i].x += speed
            if label_list[a - 1].x == label_list[a].x:
                insertState = "Move"
        elif insertState == "Move":
            if label_list[a].x - Speed < index_list[b].x:
                label_list[a].x = index_list[b].x
            else:
                label_list[a].x -= Speed
            if label_list[a].x == index_list[b].x:
                insertState = "Drop"
        elif insertState == "Drop":
            if label_list[a].y - Speed < y_label:
                label_list[a].y = y_label
            else:
                label_list[a].y -= Speed
            if label_list[a].y == y_label:
                onInsert = False
                insertState = "Pick"
                temp = label_list[a]
                for lb in range(a, b):
                    label_list[lb] = label_list[lb + 1]
                label_list[b] = temp

def Done(label_list, idx, color):
    label_list[idx].color = color

def End(label_list, color):
    for lb in label_list:
        lb.color = color

def Point(*idx):
    for i in range(len(arrow_list)):
        if i not in idx:
            arrow_list[i].visible = False
        else:
            arrow_list[i].visible = True

def Lp(idx):
    for i in range(len(larrow_list)):
        if i == idx:
            if larrow_list[i].visible == False:
                larrow_list[i].visible = True
        else:
            larrow_list[i].visible = False

def Rp(idx):
    for i in range(len(rarrow_list)):
        if i == idx:
            if rarrow_list[i].visible == False:
                rarrow_list[i].visible = True
        else:
            rarrow_list[i].visible = False


x = 0
y = 0

def game_loop(_):
    global count
    global label_list
    global onSwap, onInsert
    global x, y
    global step, Delay
    global command_list
    Delay -= 1
    if Delay <= 0:
        if not onSwap and not onInsert:
            if len(command_list) > 0:
                s = command_list.pop(0)
                if s[0] == "Point":
                    Point(s[1], s[2])
                    Delay = DELAY
                if s[0] == "Swap":
                    onSwap = True
                    x = s[1]
                    y = s[2]
                    swap(label_list, x, y)
                if s[0]== "Done":
                    Done(label_list, s[1], GREEN_COLOR)
                    Delay = DELAY


    if onSwap:
        swap(label_list, x, y)


    if onInsert:
        insert(label_list, x, y)
        if not onInsert:
            step += 1

create_num_list(n)
command_list = []
for i in range(len(n) - 1):
    for j in range(i, len(n)):
        command_list.append(["Point", i, j])
        if n[i] > n[j]:
            print(n)
            print(n[i], n[j])
            n[i], n[j] = n[j], n[i]
            command_list.append(["Swap", i, j])
    command_list.append(["Done", i])
command_list.append(["Done", i + 1])
print(command_list)
pyglet.clock.schedule(game_loop)

pyglet.app.run()
