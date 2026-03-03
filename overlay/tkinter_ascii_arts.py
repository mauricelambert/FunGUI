import tkinter as tk

WIDTH = 600
HEIGHT = 600

ascii_art = r"""
   /\_/\
  ( o.o )
   > ^ <
"""

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "white")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0)
canvas.pack()

text = canvas.create_text(
    WIDTH/2, HEIGHT/2,
    text=ascii_art,
    font=("Courier", 20),
    fill="red"
)

size = 20

def animate():
    global size
    size += 1
    canvas.itemconfig(text, font=("Courier", size))

    x1, y1, x2, y2 = canvas.bbox(text)

    if x1 <= 0 or y1 <= 0 or x2 >= WIDTH or y2 >= HEIGHT:
        root.destroy()
        return

    root.after(30, animate)

animate()
root.mainloop()