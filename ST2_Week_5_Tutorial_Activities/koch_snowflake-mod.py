#Now, you will modify the sierpinski_triangle.py program to display snowflake fractal, another fractal named after Koch a Swedish mathematician. fractal, called the Koch snowflake,

from tkinter import *
import math

class KochSnowflake:
    def __init__(self):
        window = Tk()
        window.title("Koch Snowflake")

        self.width = 400
        self.height = 400

        self.canvas = Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()

        frame = Frame(window)
        frame.pack()

        Label(frame, text="Order: ").pack(side=LEFT)
        self.order = StringVar()
        Entry(frame, textvariable=self.order).pack(side=LEFT)

        Button(frame, text="Draw", command=self.draw).pack(side=LEFT)

        window.mainloop()

    def draw(self):
        self.canvas.delete("line")

        p1 = (100, 300)
        p2 = (300, 300)
        p3 = (200, 100)

        order = int(self.order.get())

        self.koch(p1, p2, order)
        self.koch(p2, p3, order)
        self.koch(p3, p1, order)

    def koch(self, p1, p2, order):
        if order == 0:
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], tags="line")
        else:
            x1, y1 = p1
            x2, y2 = p2

            dx = (x2 - x1) / 3
            dy = (y2 - y1) / 3

            pA = (x1 + dx, y1 + dy)
            pB = (x1 + 2*dx, y1 + 2*dy)

            # Peak of triangle
            angle = math.radians(60)
            px = pA[0] + (dx * math.cos(angle) - dy * math.sin(angle))
            py = pA[1] + (dx * math.sin(angle) + dy * math.cos(angle))
            pC = (px, py)

            self.koch(p1, pA, order-1)
            self.koch(pA, pC, order-1)
            self.koch(pC, pB, order-1)
            self.koch(pB, p2, order-1)


KochSnowflake()