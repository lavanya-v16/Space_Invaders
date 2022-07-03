import turtle as t
import math
import random
import winsound
import pickle
import mysql.connector as n
from tkinter import *
from mysql.connector import Error as e


#setting screen
pic=open("SPACEINVADERSPIC.gif","r")
wn = t.Screen()
wn.title('SPACEINVADERS')
wn.bgcolor("black")
wn.bgpic("SPACEINVADERSPIC.gif")
wn.tracer(1)
pic.close()

# drawing border
mypen=t.Turtle()
mypen.color('white')
mypen.penup()
mypen.hideturtle()
mypen.setposition(-300, -300)
mypen.pendown()
mypen.pensize(3)

# for writing other files
mypen1 = t.Turtle()
mypen1.color('white')
mypen1.penup()
mypen1.setposition(-150, 310)
mypen1.pensize(3)

for side in range(4):
    mypen.forward(600)
    mypen.left(90)
mypen.hideturtle()

# create player
player = t.Turtle()
player.color("yellow")
player.shape("arrow")
player.penup()  # to avoid animation line
player.speed(0)  # animation speed 0 is max
score = 0

# create goals
maxGoals = 6
goals = []

for count in range(maxGoals):
    goals.append(t.Turtle())  # for a total of 6 turtles
    goals[count].color("orange")
    goals[count].shape("turtle")
    goals[count].penup()
    goals[count].speed(0)
    goals[count].setposition(random.randint(-300, 300), random.randint(-300, 300))

# setting speed
speed = 1

# def function for turning
def turnleft():
    player.left(30)

def turnright():
    player.right(30)

def increasespeed():
    global speed
    speed += 1

def isCollision(t1, t2):
    d = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if d < 20:
        return True
    else:
        return False

# set keyboard to movements
t.listen()
t.onkey(turnleft, "Left")
t.onkey(turnright, "Right")
t.onkey(increasespeed, "Up")
chance = 2
while chance > 0:
    player.forward(speed)

    # boundary checking
    if player.xcor() > 300 or player.xcor() < -300:
        player.right(180)
        chance -= 1
        winsound.PlaySound("BREAKING2.mp3", winsound.SND_ASYNC)
        # chance warning
        mypen1.undo()
        mypen1.penup()
        mypen1.hideturtle()
        mypen1.setposition(-150, 310)
        chancestring = 'collisions left:', chance
        mypen1.write(chancestring, False, align='left', font=('Arial', 14, 'normal'))
    if player.ycor() > 300 or player.ycor() < -300:
        player.right(180)
        chance -= 1
        # chance warning
        mypen1.undo()
        mypen1.penup()
        mypen1.hideturtle()
        mypen1.setposition(-150, 310)
        chancestring = 'collisions left:', chance
        mypen1.write(chancestring, False, align='left', font=('Arial', 14, 'normal'))
        winsound.PlaySound("BREAKING2.mp3", winsound.SND_ASYNC)

    # move the goal
    for count in range(maxGoals):
        goals[count].forward(3)

        # boundary checking
        if goals[count].xcor() > 290 or goals[count].xcor() < -290:
            goals[count].right(180)
            winsound.PlaySound("BREAKING2.mp3", winsound.SND_ASYNC)
        if goals[count].ycor() > 290 or goals[count].ycor() < -290:
            goals[count].right(180)
            winsound.PlaySound("BREAKING2.mp3", winsound.SND_ASYNC)

        # collision checking
        if isCollision(player, goals[count]):
            goals[count].setposition(random.randint(-300, 300), random.randint(-300, 300))
            goals[count].right(random.randint(0, 360))
            winsound.PlaySound("COLLISION2.mp3", winsound.SND_ASYNC)
            score += 1
            # draw score
            mypen.undo()  # to undo the previous score n write the next one
            mypen.penup()
            mypen.hideturtle()
            mypen.setposition(-290, 310)
            scorestring = "score:", score
            mypen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))


else:
    #game over
    for a in range(50):
        mypen.setposition(0, 0)
        mypen.write('GAME OVER', False, align='center', font=("Arial", 30, "normal"))
    else:
        wn.clearscreen()
        wn.bgcolor('black')

    #displaying high score
    file2 = open('SCORE', 'ab+')
    pickle.dump( str(score), file2)
    pickle.dump('\n',file2)
    file2.seek(0)
    scorelist = []
    namelist=[]
    try:
        while True:
            k = pickle.load(file2)
            if k.isalpha():
                namelist+=[k]
            elif k.isdigit():
                scorelist += [int(k)]

    except EOFError:
        file2.close()

    highscore = scorelist[0]
    highname=namelist[0]
    for i in range(len(scorelist)):
        if scorelist[i] > highscore:
            highscore = scorelist[i]
            highname=namelist[i]
    NAME=namelist[i]
    if highscore == score:
        mypen.setposition(0, 0)
        mypen.write('YAYY '+NAME+'!!!! \nYOU GOT THE HIGHEST SCORE :'+str(score), False, align='center', font=('Arial', 20, 'normal'))
        t.exitonclick()
    else:
        string = 'YOUR SCORE :\n'+NAME +':'+ str(score) + '\n\n\n' + 'HIGHEST SCORE:\n'+highname +':'+ str(highscore)
        mypen.setposition(0, 0)
        mypen.write(string, False, align='center', font=('Arial', 20, 'normal'))
        t.exitonclick()


connection = n.connect(host='localhost',user='root',
                                         password='mysql20',
                                         database='SPACEINVADERSGAME')



if connection.is_connected():
    cursor = connection.cursor()
    act="insert into PLAYERSCORE values('%s',%s)".format(NAME,score)
    connection.commit()
    cursor.execute(act)
    cursor.execute('select row_number() over (order by SCORE) as S.NO.,NAME,SCORE from PLAYERSCORE;')
    record = cursor.fetchall()
    cursor.close()
    connection.close()

#record=[['Anna',12],['Emma',8],['Lava',11],['Madhu',13],['Zac',9]]
    Scores=''
    for row in record:
        r=''
        r+=str(row[0])
        r+=':'
        r+=str(row[1])

        Scores+=(r+'\n')
    cursor.close()
    connection.close()

en=Tk()
l=Label(en,text=Scores,width=40,height=20,bg='purple',font=('Arial',13))
l.pack()
mainloop()


