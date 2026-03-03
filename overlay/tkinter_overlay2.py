import tkinter as tk

WIDTH = 600
HEIGHT = 600

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "white")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0)
canvas.pack()

star = canvas.create_polygon(
    300,150,
    340,250,
    450,250,
    360,320,
    400,430,
    300,360,
    200,430,
    240,320,
    150,250,
    260,250,
    fill="red"
)

def animate():
    canvas.scale(star, WIDTH/2, HEIGHT/2, 1.04, 1.04)

    x1, y1, x2, y2 = canvas.bbox(star)

    if x1 <= 0 or y1 <= 0 or x2 >= WIDTH or y2 >= HEIGHT:
        root.destroy()
        return

    root.after(16, animate)

animate()
root.mainloop()