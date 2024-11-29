import turtle

blue = "#0000ff"
pink = "#ff00ff"
green="#00ff00"

def drawSquare(size, colour):
    turtle.color(colour)
    for i in range(4):
        turtle.forward(size)
        turtle.right(90)

turtle.speed(5)
turtle.setheading(0)
turtle.pendown()
drawSquare(100, blue)
turtle.penup()
turtle.forward(3)
turtle.left(90)
turtle.forward(5)
turtle.pendown()
drawSquare(80, pink)
turtle.penup()
