import turtle
import level
ms = turtle.Screen()
ms.setup(950, 650, 200, 0)#设置窗口大小和在屏幕上的坐标 
ms.register_shape('bc1.gif')#注册图形
ms.bgpic('bc1.gif')#设置背景图片，只支持gif格式 
ms.title('py-game')
ms.register_shape('wall.gif')
ms.register_shape('o.gif')
ms.register_shape('p.gif')
ms.register_shape('box.gif')
ms.register_shape('boxc.gif')
ms.tracer(0)#自动屏幕更新关闭

levels = level.level_list()


class Pen(turtle.Turtle):
    def __init__(self, pic):
        super().__init__()
        self.shape(pic)
        self.penup()

    def move(self, x, y, px, py):
        gox, goy = x+px, y+py
        if (gox, goy) in go_space:
            self.goto(gox, goy)
        if (gox+px, goy+py) in go_space and (gox, goy) in box_space:
            for i in box_list:
                if i.pos() == (gox, goy):
                    go_space.append(i.pos())
                    box_space.remove(i.pos())
                    i.goto(gox+px, goy+py)
                    self.goto(gox, goy)
                    go_space.remove(i.pos())
                    box_space.append(i.pos())
                    if i.pos() in correct_box_space:
                        i.shape('boxc.gif')
                    else:
                        i.shape('box.gif')
                    if set(box_space) == set(correct_box_space):
                        text.show_win()

                    

    def go_up(self):
        self.move(self.xcor(), self.ycor(), 0, 50)

    def go_down(self):
        self.move(self.xcor(), self.ycor(), 0, -50)

    def go_left(self):
        self.move(self.xcor(), self.ycor(), -50, 0)

    def go_right(self):
        self.move(self.xcor(), self.ycor(), 50, 0)


class Game():
    def paint(self):
        i_date = len(levels[num-1])
        j_date = len(levels[num-1][0])
        for i in range(i_date):
            for j in range(j_date):
                x = -j_date*25+25+j*50 + sister_x
                y = i_date*25-25-i*50
                if levels[num-1][i][j] == ' ':
                    go_space.append((x, y))
                if levels[num-1][i][j] == 'X':
                    wall.goto(x, y)
                    wall.stamp()
                if levels[num-1][i][j] == 'O':
                    correct_box.goto(x, y)
                    correct_box.stamp()
                    go_space.append((x, y))
                    correct_box_space.append((x, y))
                if levels[num-1][i][j] == 'P':
                    player.goto(x, y)
                    go_space.append((x, y))
                if levels[num-1][i][j] == 'B':
                    box = Pen('box.gif')
                    box.goto(x, y)
                    box_list.append(box)
                    box_space.append((x, y))


class ShowMessage(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.pencolor('blue')
        self.ht()

    def message(self):
        self.goto(0+sister_x, 290)
        self.write(f'第{num}关', align='center', font=('仿宋', 20, 'bold'))
        self.goto(0+sister_x, 270)
        self.write('重新开始本关请按回车键', align='center', font=('仿宋', 15, 'bold'))
        self.goto(0+sister_x, 250)
        self.write('选择关卡请按Q', align='center', font=('仿宋', 15, 'bold'))

    def show_win(self):
        global num
        if num == len(levels):
            num = 1
            self.goto(0, 0)
            self.write('你已全部过关', align='center', font=('黑体', 30, 'bold'))
            self.goto(0, -50)
            self.write('返回第一关轻按空格键', align='center', font=('黑体', 30, 'bold'))
        else:
            num = num+1
            self.goto(0, 0)
            self.write('恭喜过关', align='center', font=('黑体', 30, 'bold'))
            self.goto(0, -50)
            self.write('进入下一关请按空格键', align='center', font=('黑体', 30, 'bold'))


def init():
    text.clear()
    wall.clear()
    correct_box.clear()
    for i in box_list:
        i.ht()
        del(i)
    box_list.clear()
    box_space.clear()
    go_space.clear()
    correct_box_space.clear()
    game.paint()
    text.message()
    ms.bgpic(f'bc1.gif')


def choose():
    global num
    a = ms.numinput('选择关卡', '你的选择（请输入1-5）', 1)
    if a is None:
        a = num
    num = int(a)
    init()
    ms.listen()


sister_x = 225
num = 1
correct_box_space = []
box_list = []
box_space = []
go_space = []
wall = Pen('wall.gif')
correct_box = Pen('o.gif')
player = Pen('p.gif')
game = Game()
game.paint()
text = ShowMessage()
text.message()

ms.listen()
ms.onkey(player.go_up, 'Up')
ms.onkey(player.go_down, 'Down')
ms.onkey(player.go_left, 'Left')
ms.onkey(player.go_right, 'Right')
ms.onkey(init, 'Return')
ms.onkey(init, 'space')
ms.onkey(choose, 'q')

while True:
    ms.update()

ms.mainloop()
