import pyglet
from random import randint
from math import sin, cos, radians, degrees, atan2


cloud_sprites = []
ground_sprites = []
bird_sprites = []
target_x = 10
target_y = 200
corn_x = 10
corn_y = 200
limit = 500
limit_range = 50
init_score = 0
skill_activated = False
second_skill_activated = False
game_stop = True
high_score = 0
skill_cool_down = 500
second_skill_cool_down = 1000
init_game_speed = 10
init_bird_speed = 20
skill_duration = 150
second_skill_duration = 300
cool_down = 0
second_cool_down = 0
max_bird_speed = init_bird_speed
duration = skill_duration
second_duration = second_skill_duration
game_speed = init_game_speed
window = pyglet.window.Window(fullscreen=True)
pyglet.gl.glClearColor(0,128,255,255)
batch = pyglet.graphics.Batch()
batch1 = pyglet.graphics.Batch()
cloud_img = pyglet.image.load('images/cloud1.png')
ground_img = pyglet.image.load('images/ground1.png')
corn_img = pyglet.image.load('images/corn1.png')
scarecrow_img = pyglet.image.load('images/scarecrow.png')
cage_img = pyglet.image.load('images/cage.png')
cloud_img.anchor_x = cloud_img.width
cloud_img.anchor_y = cloud_img.height
ground_img.anchor_x = ground_img.width
ground_img.anchor_y = 0
corn_img.anchor_x = corn_img.width // 2
corn_img.anchor_y = corn_img.height // 2
cage_img.anchor_x = 0
cage_img.anchor_y = cage_img.height
scarecrow_img.anchor_x = scarecrow_img.width // 2
scarecrow_img.anchor_y = scarecrow_img.height // 3 * 2
cage_sprite = pyglet.sprite.Sprite(img=cage_img, x=0, y=window.height, batch=batch)
cage_sprite.scale_x = 1
cage_sprite.scale_y = 2.6
scarecrow_sprite = pyglet.sprite.Sprite(img=scarecrow_img)
scarecrow_sprite.scale = 0.6
scarecrow_sprite.scale_x = -1
score_label = pyglet.text.Label("score: 0", bold=True, font_size=30, x=10, y=window.height - 50, batch=batch)
cool_down_label = pyglet.text.Label("Skill cooldown: " + "I" * (cool_down // 10), font_size=30, x=10, y=window.height - 100, bold=True, batch=batch)
second_cool_down_label = pyglet.text.Label("2nd Skill cooldown: " + "I" * (second_cool_down // 20), font_size=30, x=10, y=window.height - 150, bold=True, batch=batch)
duration_label = pyglet.text.Label("Skill duration: " + str(duration), font_size=30, x=10, y=window.height - 200, bold=True)
second_duration_label = pyglet.text.Label("2nd Skill duration: " + str(second_duration), font_size=30, x=10, y=window.height - 250, bold=True)
score_board = pyglet.text.Label("SCORE: 0", font_size=45, x=window.width // 2, y=window.height // 2 + 35, anchor_x="center", anchor_y="center", batch=batch1)
result_label = pyglet.text.Label("Press [ESC] to quit - Press [ENTER] to play", font_size=20, x=window.width // 2, y=window.height // 2 - 100, anchor_x="center", anchor_y="center", batch=batch1)
high_score_board = pyglet.text.Label("HIGH SCORE: " + str(high_score), font_size=45, x=window.width // 2, y=window.height // 2 - 35, anchor_x="center", anchor_y="center", batch=batch1)
# cursor = pyglet.window.ImageMouseCursor(corn_img, 16, corn_img.height)
# window.set_mouse_cursor(cursor)

#create clouds
def create_cloud(position=1):
    global cloud_sprites
    cloud_x = window.width * position
    cloud_y = window.height - 100
    Up = True
    for index in range(15):
        sprite = pyglet.sprite.Sprite(img=cloud_img, y=cloud_y, x=cloud_x, batch=batch)
        sprite.scale = randint(8, 12) / 100
        if randint(0, 10) > 5:
            cloud_sprites.append(sprite)
        cloud_x -= cloud_img.width * sprite.scale / 2 + randint(10, 50)
        if Up:
            cloud_y -= cloud_img.height * sprite.scale + randint(10, 50)
            Up = False
        else:
            cloud_y += cloud_img.height * sprite.scale + randint(10, 50)
            Up = True


def create_ground(ground_x=window.width, ground_y=0):
    global ground_sprites
    sprite = pyglet.sprite.Sprite(img=ground_img, y=ground_y, x=ground_x, batch=batch)
    sprite.scale = 0.25
    ground_sprites.append(sprite)


def create_bird_motion():
    global raven_list
    raven_list = []
    for i in range(25):
        strg = 'images/raven' + str(i + 1) + '.png'
        raven_list.append(pyglet.image.load(strg))

def create_bird():
    global bird_img
    global crow_wave_sound
    speed = randint(20, max_bird_speed)
    bird_img = pyglet.image.Animation.from_image_sequence(raven_list, (55 - speed) / 200, True)
    bird_x = window.width + bird_img.get_max_width()
    bird_y = randint(200, window.height - 200)
    _bird_img = bird_img.get_transform(True, False, 0)
    sprite = pyglet.sprite.Sprite(img=_bird_img, x=bird_x, y=bird_y, batch=batch)
    rotate = 180 - degrees(atan2(target_y - bird_y, target_x - bird_x))
    sprite.update(rotation=rotate)
    scored_status = False
    x_target = target_x
    y_target = target_y
    bird_sprites.append([sprite, rotate, speed, scored_status, x_target, y_target])



def create_target():
    global corn_sprite
    global target_sprite
    corn_sprite = pyglet.sprite.Sprite(img=corn_img, x=corn_x, y=corn_y, batch=batch)
    target_sprite = pyglet.sprite.Sprite(img=corn_img, x=target_x, y=target_y + corn_img.height // 2)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global skill_activated
    global cool_down
    global target_x
    global target_y
    global second_skill_activated
    global corn_img
    global target_sprite
    if button == pyglet.window.mouse.LEFT and cool_down == 0 and duration > 0:
        skill_activated = True
        # target_x = x
        # target_y = y
        target_sprite.update(x=target_x, y=target_y + corn_img.height * 2 // 3)
    if button == pyglet.window.mouse.RIGHT and second_cool_down == 0 and second_duration > 0:
        second_skill_activated = True

@window.event
def on_mouse_release(x, y, button, modifiers):
    global skill_activated
    global target_y
    global cool_down
    if button == pyglet.window.mouse.LEFT and cool_down == 0:
        skill_activated = False
        target_y = y - corn_img.height // 2
        cool_down = skill_cool_down

@window.event
def on_mouse_motion(x, y, dx, dy):
    global target_x
    global target_y
    global corn_x
    global corn_y
    if not game_stop:
        if x < limit - limit_range:
            target_x = x
            corn_x = x
        if y > ground_sprites[0].height:
            if not skill_activated:
                target_y = y - corn_img.height // 2
            corn_y = y
        corn_sprite.update(x=corn_x, y=corn_y)
        scarecrow_sprite.update(x=corn_x, y=corn_y)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global target_x
    global target_y
    global corn_x
    global corn_y
    if not game_stop:
        if x < limit - limit_range:
            target_x = x
            corn_x = x
        if y > ground_sprites[0].height:
            if skill_activated and cool_down == 0 and duration > 0:
                pass
            else:
                target_y = y - corn_img.height // 2
            corn_y = y
        corn_sprite.update(x=corn_x, y=corn_y)
        scarecrow_sprite.update(x=corn_x, y=corn_y)

@window.event
def on_draw():
    window.clear()
    batch.draw()
    score_label.draw()
    if second_duration > 0 and second_skill_activated:
        scarecrow_sprite.draw()
    if skill_activated:
        duration_label.draw()
        target_sprite.draw()
    if second_skill_activated:
        second_duration_label.draw()
    if game_stop:
        batch1.draw()


@window.event
def on_key_press(s, modifiers):
    global game_stop
    global score
    if (s == pyglet.window.key.ENTER or s == 65421) and game_stop:
        game_stop = False
        score = init_score
        score_label.text = 'score: 0'
        init()

def stop_game():
    global game_speed
    global bird_sprites
    global game_stop
    global high_score
    game_speed = 0
    game_stop = True
    for index in range(len(bird_sprites)):
        bird_sprites[index][2] = 0
    if score > high_score:
        high_score = score
        f = open('data', 'w')
        f.write(str(high_score))
        f.close()
    score_board.text = 'SCORE: ' + str(score)
    high_score_board.text = 'HIGH SCORE: ' + str(high_score)


def load_high_score():
    global high_score
    f = open('data', 'r')
    high_score = int(f.read())
    f.close()


def change_background():
    ran = randint(0, 3)
    if ran == 0:
        pyglet.gl.glClearColor(0,128,255,255)
    elif ran == 1:
        pyglet.gl.glClearColor(255,255,0,255)
    elif ran == 2:
        pyglet.gl.glClearColor(255,0,255,255)
    elif ran == 3:
        pyglet.gl.glClearColor(0,0,0,255)

def init():
    global bird_sprites
    global ground_sprites
    global game_speed
    global max_bird_speed
    global cloud_sprites
    global cool_down
    global second_cool_down
    global duration
    global second_duration
    global skill_activated
    global second_skill_activated
    for sprite in range(len(bird_sprites)):
        bird_sprites[sprite][0].delete()
    for ground in ground_sprites:
        ground.delete()
    for cloud in cloud_sprites:
        cloud.delete()
    bird_sprites = []
    ground_sprites = []
    cloud_sprites = []
    game_speed = init_game_speed
    max_bird_speed = init_bird_speed
    cool_down = 0
    second_cool_down = 0
    duration = skill_duration
    second_duration = second_skill_duration
    second_skill_activated = False
    skill_activated = False
    cool_down_label.text = 'Skill cooldown: '
    cool_down_label.color = (255, 255, 255, 255)
    second_cool_down_label.text = "2n Skill cooldown: "
    second_cool_down_label.color = (255, 255, 255, 255)
    window.clear()
    load_high_score()
    high_score_board.text = "HIGH SCORE: " + str(high_score)
    create_cloud()
    create_ground()
    create_bird_motion()
    create_bird()
    create_target()

def game_loop(_):
    if not game_stop:
        global score
        global game_speed
        global bird_speed
        global max_bird_speed
        global cool_down
        global second_cool_down
        global duration
        global second_duration
        global skill_activated
        global second_skill_activated
        global target_x
        global target_y
        global corn_img
        remove_list = []
        if cool_down > 0:
            cool_down -= 1
            if cool_down > skill_cool_down // 2:
                cool_down_label.color = (255, 0, 0, 255)
            elif skill_cool_down // 5 <= cool_down <= skill_cool_down // 2:
                cool_down_label.color = (255, 255, 0, 255)
            else:
                cool_down_label.color = (0, 255, 0, 255)
            cool_down_label.text = "Skill cooldown: " + "I" * (cool_down // 10)
        if second_cool_down > 0:
            second_cool_down -= 1
            if second_cool_down > second_skill_cool_down // 2:
                second_cool_down_label.color = (255, 0, 0, 255)
            elif second_skill_cool_down // 5 <= second_cool_down <= second_skill_cool_down // 2:
                second_cool_down_label.color = (255, 255, 0, 255)
            else:
                second_cool_down_label.color = (0, 255, 0, 255)
            second_cool_down_label.text = "2nd Skill cooldown: " + "I" * (second_cool_down // 20)
        if skill_activated and duration > 0:
            duration -= 1
            duration_display = ""
            for i in range(duration // 10):
                duration_display += "I"
            if duration > skill_duration // 2:
                duration_label.color = (0, 255, 0, 255)
            elif skill_duration // 5 <= duration <= skill_duration // 2:
                duration_label.color = (255, 255, 0, 255)
            else:
                duration_label.color = (255, 0, 0, 255)
            duration_label.text = "Skill duration: " + duration_display
        if second_skill_activated and second_skill_duration > 0:
            second_duration -= 1
            second_duration_display = ""
            for i in range(second_duration // 10):
                second_duration_display += "I"
            if second_duration > second_skill_duration // 2:
                second_duration_label.color = (0, 255, 0, 255)
            elif second_skill_duration // 5 <= second_duration <= second_skill_duration // 2:
                second_duration_label.color = (255, 255, 0, 255)
            else:
                second_duration_label.color = (255, 0, 0, 255)
            second_duration_label.text = "Skill duration: " + second_duration_display
        if duration == 0:
            skill_activated = False
            target_x = corn_x
            target_y = corn_y - corn_img.height // 2
            cool_down = skill_cool_down
            duration = skill_duration
            target_y = target_y - corn_img.height // 2
        if second_duration == 0:
            second_skill_activated = False
            #target_sprite.update(img=corn_img)
            # corn_img = pyglet.image.load('images/corn1.png')
            second_cool_down = second_skill_cool_down
            second_duration = second_skill_duration
        for sprite in cloud_sprites:
            sprite.x -= game_speed
            if sprite.x < 0:
                remove_list.append(sprite)
        for remove in remove_list:
            remove.delete()
            cloud_sprites.remove(remove)
        if sprite.x < window.width:
            create_cloud(2)

        ground_remove_list = []
        for ground in ground_sprites:
            if ground.x <= window.width and len(ground_sprites) < 2:
                create_ground(window.width + ground.width - 1)
            if ground.x <= 0:
                ground_remove_list.append(ground)
            ground.x -= game_speed
        for rmv in ground_remove_list:
            ground_sprites.remove(rmv)
            rmv.delete()
        if randint(0, 1000) > 990 - score:
            create_bird()
        bird_remove_list = []
        for bird, rotate, speed, scored_status, bird_target_x, bird_target_y in bird_sprites:
            bird.x -= cos(radians(rotate)) * speed
            if bird.x > bird_target_x:
                if rotate < 0:
                    bird.y -= sin(radians(rotate)) * speed
                elif rotate > 0:
                    bird.y += sin(radians(rotate)) * speed
            if bird.x < 0 - bird_img.get_max_width():
                score += 1
                if score % 10 == 0:
                    change_background()
                if max_bird_speed < 50:
                    max_bird_speed += 1
                score_label.text = 'score: ' + str(score)
                bird_remove_list.append([bird, rotate, speed, scored_status, bird_target_x, bird_target_y])
        for rmv in bird_remove_list:
            rmv[0].delete()
            bird_sprites.remove(rmv)
        for index in range(len(bird_sprites)):
            if second_skill_activated:
                bird_sprites[index][4] = target_x
                if index % 2 == 0:
                    bird_sprites[index][5] = target_y + 200
                else:
                    bird_sprites[index][5] = target_y - 350
            else:
                bird_sprites[index][4] = target_x
                bird_sprites[index][5] = target_y
            if bird_sprites[index][0].x > limit + limit_range:
                rt = degrees(atan2(bird_sprites[index][5] - bird_sprites[index][0].y, bird_sprites[index][4] - bird_sprites[index][0].x))
                # print(rt)
                # if rt < 170 and rt > 0:
                #     rt = 170
                # elif rt > -170 and rt < 0:
                #     rt = -170
                bird_sprites[index][1] = 180 - rt
                bird_sprites[index][0].update(rotation=bird_sprites[index][1])
            if bird_sprites[index][0].x < corn_x < bird_sprites[index][0].x + bird_img.get_max_width() // 5 and \
                    bird_sprites[index][0].y + 20 < corn_y < bird_sprites[index][0].y + bird_img.get_max_height() and \
                    bird_sprites[index][3] is False:
                bird_sprites[index][3] = True
                stop_game()

init()
pyglet.clock.schedule(game_loop)
pyglet.app.run()
