import tkinter as tk

WIDTH = 600
HEIGHT = 600

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "white")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0)
canvas.pack()

face = canvas.create_oval(200, 200, 400, 400, fill="yellow", outline="")
eye1 = canvas.create_oval(250, 260, 290, 300, fill="black")
eye2 = canvas.create_oval(310, 260, 350, 300, fill="black")
mouth = canvas.create_arc(260, 300, 340, 360, start=180, extent=180, style="chord")

items = [face, eye1, eye2, mouth]

def animate():
    for item in items:
        canvas.scale(item, WIDTH/2, HEIGHT/2, 1.03, 1.03)

    x1, y1, x2, y2 = canvas.bbox(face)

    if x1 <= 0 or y1 <= 0 or x2 >= WIDTH or y2 >= HEIGHT:
        root.destroy()
        return

    root.after(16, animate)

animate()
root.mainloop()