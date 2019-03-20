import pyglet

# Global variables
window = pyglet.window.Window(800, 600)
pyglet.gl.glClearColor(0,128,255,255)
label = pyglet.text.Label("0", font_size=36, y=300, x=400)
raven_list = []
for i in range(25):
    strg = 'images/raven' + str(i + 1) + '.png'
    raven_list.append(pyglet.image.load(strg))
# animation = pyglet.image.from_image_sequence(raven_list, 0.2, True)
image = pyglet.image.Animation.from_image_sequence(raven_list, 0.1, True)
batch = pyglet.graphics.Batch()
sprite = pyglet.sprite.Sprite(img=image, batch=batch)
sprite.scale = 0.5
# Event callbacks
@window.event
def on_draw():
    window.clear()
    label.draw()
    batch.draw()

# Game loop (loop? Why loop?)
def game_loop(_):
    label.text = str(int(label.text) + 1)

pyglet.clock.schedule(game_loop)
pyglet.app.run()
