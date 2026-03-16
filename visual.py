from pyray import *
init_window(800, 450, "Hello")
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    if is_mouse_button_down(0):
        draw_rectangle(0, 0, 100, 200, BLACK)
    draw_text("Hello world", 190, 200, 20, VIOLET)
    end_drawing()
close_window()