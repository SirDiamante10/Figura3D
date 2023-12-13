import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, sin

# Variables para el control de la rotación
yaw = 0.0
pitch = 0.0
last_x, last_y = 0.0, 0.0
left_mouse_button_pressed = False

# Posición de la fuente de luz
light_position = (2.0, 2.0, 2.0, 1.0)

def draw_sphere(radius, slices, stacks):
    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def set_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    ambient_light = (0.2, 0.2, 0.2, 1.0)
    diffuse_light = (1.0, 1.0, 1.0, 1.0)  # Aumentar la intensidad de la luz difusa
    specular_light = (1.0, 1.0, 1.0, 1.0)

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)


def set_material(color):
    # Configurar el material del objeto
    ambient_material = (color[0] * 0.3, color[1] * 0.2, color[2] * 0.2, 1.0)
    diffuse_material = (color[0] * 0.9, color[1] * 0.8, color[2] * 0.8, 1.0)
    specular_material = (1.0, 1.0, 1.0, 1.0)

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_material)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_material)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_material)
    glMaterialf(GL_FRONT, GL_SHININESS, 100.0)

def draw_character():
    global yaw, pitch

    glRotatef(yaw, 0.0, 1.0, 0.0)
    glRotatef(pitch, 1.0, 0.0, 0.0)

    set_lighting()  # Configurar iluminación

    # Cuerpo (una esfera rosa)
    glColor3f(1.0, 0.5, 0.5)  # Color rosa
    set_material((1.0, 0.5, 0.5))  # Configurar material
    draw_sphere(0.4, 20, 20)

    # Brazos (dos brazos semi esféricos pegados al cuerpo)
    glColor3f(1.0, 0.5, 0.5)  # Color rosa
    set_material((1.0, 0.5, 0.5))  # Configurar material
    glPushMatrix()
    glTranslatef(0.3, 0.0, 0.0)
    draw_sphere(0.2, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.3, 0.0, 0.0)
    draw_sphere(0.2, 20, 20)
    glPopMatrix()

    # Pies (dos esferas rojas como pies)
    glColor3f(1.0, 0.0, 0.0)  # Color rojo
    set_material((1.0, 0.0, 0.0))  # Configurar material
    glPushMatrix()
    glTranslatef(0.15, -0.4, 0.0)
    draw_sphere(0.2, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.15, -0.4, 0.0)
    draw_sphere(0.2, 20, 20)
    glPopMatrix()

    # Cara (dos ojos negros y una sonrisa)
    glColor3f(0.0, 0.0, 0.0)  # Color negro
    set_material((0.0, 0.0, 0.0))  # Configurar material
    glPushMatrix()
    glTranslatef(0.1, 0.2, 0.25)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.1, 0.2, 0.25)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.25)
    glRotatef(180, 1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLE_STRIP)
    for angle in range(0, 91, 5):
        x = 0.15 * cos(angle)
        y = 0.05 * sin(angle)
        glVertex3f(x, y, 0.0)
    glEnd()
    glPopMatrix()

    # Boca (círculo negro debajo de los ojos)
    glColor3f(0.0, 0.0, 0.0)  # Color negro
    set_material((0.0, 0.0, 0.0))  # Configurar material
    glPushMatrix()
    glTranslatef(0.0, 0.1, 0.25)
    draw_sphere(0.08, 20, 20)
    glPopMatrix()

    # Retinas de los ojos (dos esferas cyan en los ojos)
    glColor3f(0.0, 1.0, 1.0)  # Color cyan
    set_material((0.0, 1.0, 1.0))  # Configurar material
    glPushMatrix()
    glTranslatef(0.1, 0.2, 0.25)
    draw_sphere(0.05, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.1, 0.2, 0.25)
    draw_sphere(0.05, 20, 20)
    glPopMatrix()

    # Desactivar la iluminación después de dibujar
    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)

def draw_shadow():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.0, 0.0, 1.0, 0.5)  # Sombra azul con opacidad
    glPushMatrix()
    glTranslatef(light_position[0], light_position[1], light_position[2])
    glTranslatef(0.0, -0.5, 0.0)  # Ajustar la posición de la sombra
    draw_character()
    glPopMatrix()

    glDisable(GL_BLEND)

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    if button == glfw.MOUSE_BUTTON_LEFT:
        left_mouse_button_pressed = (action == glfw.PRESS)

def cursor_pos_callback(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, left_mouse_button_pressed

    if left_mouse_button_pressed:
        sensitivity = 0.1
        yaw += (xpos - last_x) * sensitivity
        pitch += (ypos - last_y) * sensitivity

    last_x, last_y = xpos, ypos

def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def main():
    global last_x, last_y, left_mouse_button_pressed

    if not glfw.init():
        return

    width, height = 800, 600
    window = glfw.create_window(width, height, "Personaje 3D con Sombra", None, None)
    
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)

    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 50.0)

        glTranslatef(0.0, 0.0, -5)

        # Dibujar sombra antes del personaje
        draw_shadow()

        # Dibujar personaje principal
        draw_character()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

