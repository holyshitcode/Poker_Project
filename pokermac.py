from tkinter import *
import random
from tkinter import messagebox
import sys
from PIL import Image, ImageTk
import pygame
import datetime
import redis
import main
class card:
    def __init__(self):
        self.mark = ['Spade', 'Club', 'Diamond', 'Heart']
        self.cardnum = ['2', '3', '4', '5', '6', '7', '8',
                                '9', '10', '11', '12', '13', '14']
        self.deck = []
        self.makedeck()
        self.shuffle()


    def makedeck(self):
        for i in self.mark:
            for j in self.cardnum:
                self.deck.append([i, j])

    def shuffle(self):
        random.shuffle(self.deck)

    def restarts(self):
        self.hand.clear()



class user():
    def __init__(self,name,deck):
        self.hand = []
        self.deck = deck
        self.name=name
        self.dealing()
        self.showcard()

    def restart(self):
        self.hand.clear()

    def showcard(self):
        print(f"{self.name}의 카드는{self.hand}")
    def dealing(self):
        for i in range(4):
            self.hand.append(self.deck.pop())

count=0
user1_wincount=0
user2_wincount=0
date_origin=datetime.datetime.now()
date_string = date_origin.strftime(("%Y-%m-%d%H:%M:%S"))
rank_file_path=r"./uploads/rank.txt"

def cardmake():
    global deck#2번째실행
    deck=card()
    print("카드덱 생성완료!")
def gstart(): #1번째실행
    global user1_wincount
    global user2_wincount
    start.withdraw()
    started.deiconify()
    cardmake()
    canvas.delete("win_count")
    user1_wincount = 0
    user2_wincount = 0
def usermake(): #3번째실행
    global user1
    global count
    global user1_wincount
    global user2_wincount
    name="유저(1)"
    user1=user(name,deck.deck)
    shoot()
    count+=1
    if count > 8:
        startre()
        if user1_wincount>user2_wincount:
            messagebox.showinfo("Poker Game", f"유저(1):{user1_wincount}회로 승리")
            with open(rank_file_path, 'a') as file:
                file.write(f"\n{date_string}:/유저(1)/{user1_wincount}회로 승리.")
        elif user1_wincount==user2_wincount:
            messagebox.showinfo("Poker Game", f"무승부")
            with open(rank_file_path, 'a') as file:
                file.write(f"\n{date_string}/:/무승부/.")
        else:
            messagebox.showinfo("Poker Game", f"유저(2):{user2_wincount}회로 승리")
            with open(rank_file_path, 'a') as file:
                file.write(f"\n{date_string}:/유저(2)/{user2_wincount}회로 승리.")
        count=0
        user1_wincount=0; user2_wincount=0
    audio(cardsound)
    toggle_image()
def usermake2():
    global user2
    global count
    global user1_wincount
    global user2_wincount
    name = "유저(2)"
    user2 = user(name,deck.deck)
    shoot1()
    count+=1
    if count > 8:
        startre()
        if user1_wincount > user2_wincount:
            messagebox.showinfo("Poker Game", f"유저(1):{user1_wincount}회로 승리")
            with open(rank_file_path, 'a') as file:
                file.write(f"\n{date_string}:/유저(1)/{user1_wincount}회로 승리.")
        elif user1_wincount == user2_wincount:
            messagebox.showinfo("Poker Game", f"무승부")
            with open(rank_file_path, 'a') as file:
                file.write(f"\n{date_string}/:/무승부.")
        else:
            messagebox.showinfo("Poker Game", f"유저(2):{user2_wincount}회로 승리")
            with open(rank_file_path, 'a') as file:
                file.write(f"\n{date_string}:/유저(2)/{user2_wincount}회로 승리.")
        count = 0
        user1_wincount = 0;
        user2_wincount = 0
    audio(cardsound)
    toggle_image1()

def endshow():
    print(f"1번 유저의패:{determine(user1.hand)}")
    print(f"2번 유저의패:{determine(user2.hand)}")

def straight(hand):
    hande = []
    for i in range(0, 4):
        number = hand[i][1]
        hande.append(int(number))
    hande.sort()
    if hande[0] + 1 == hande[1] and hande[1] + 1 == hande[2] and hande[2] + 1 == hande[3] and len(set(hande)) == 4:
        return True
    else:
        return False
def compare(number):
    combi = {'four of a kind': 1, 'full house': 2, 'flush': 3, 'straight': 4,
             'three of a kind': 5, 'two pair': 6, 'one pair': 7, 'high card': 8}
    return combi[number]

def determine(user):
    combi={'four of a kind':1,'straight flush':2,'flush':3,'straight':4,
                 'three of a kind':5,'two pair':6,'one pair':7,'high card':8}

    counting={}

    for item in user:
        key = item[0]
        value = item[1]
        if key in counting:
            counting[key].append(value)
        else:
            counting[key] = [value]

    for _, num in user:
        if num in counting:
            counting[num] += 1
        else:
            counting[num] = 1

    if user[0][1]==user[1][1]== user[2][1] ==user[3][1]:
        return 'four of a kind'
    elif user[0][0] == user[1][0] == user[2][0] ==user[3][0] and straight(user):
        return 'straight flush'
    elif user[0][0] == user[1][0] == user[2][0] ==user[3][0]:
        return 'flush'
    elif straight(user):
        return 'straight'
    elif 3 in counting.values():
        return 'three of a kind'
    elif list(counting.values()).count(2) == 2:
        return "two pair"
    elif 2 in counting.values():
        return "one pair"
    else:
        return "high card"

def final():
    global user1_wincount
    global user2_wincount
    if compare(determine(user1.hand))==compare(determine(user2.hand)):
        total1=0; total2=0
        for suit, value in user1.hand:
            if value.isdigit():
                total1 += int(value)
        for suit, value in user2.hand:
            if value.isdigit():
                total2 += int(value)
        if total1>total2:
            print("1번유저의 승리")
            canvas.create_image(150, 50, anchor=NW, image=win, tags="winner")
            user1_wincount+=1
            win_rate(user1_wincount)
            messagebox.showinfo("Poker Game", f"유저(1)의 승리횟수:{user1_wincount}")
        else:
            print("2번유저의 승리")
            canvas.create_image(150, 250, anchor=NW, image=win, tags="winner")
            user2_wincount += 1
            win_rate2(user2_wincount)
            messagebox.showinfo("Poker Game", f"유저(2)의 승리횟수:{user2_wincount}")
    elif compare(determine(user1.hand))< compare(determine(user2.hand)):
        print("1번유저의 승리")
        canvas.create_image(150, 50, anchor=NW, image=win, tags="winner")
        user1_wincount += 1
        win_rate(user1_wincount)
        messagebox.showinfo("Poker Game", f"유저(1)의 승리횟수:{user1_wincount}")
    else:
        print("2번유저의 승리")
        canvas.create_image(150, 250, anchor=NW, image=win, tags="winner")
        user2_wincount += 1
        win_rate2(user2_wincount)
        messagebox.showinfo("Poker Game", f"유저(2)의 승리횟수:{user2_wincount}")
def win_rate(count1):
    if count1==1:
        canvas.create_image(500, 350, anchor=NW, image=win_image, tags="win_count")
    elif count1==2:
        canvas.create_image(550, 350, anchor=NW, image=win_image2, tags="win_count")
    elif count1==3:
        canvas.create_image(600, 350, anchor=NW, image=win_image3, tags="win_count")
    elif count1==4:
        canvas.create_image(650, 350, anchor=NW, image=win_image4, tags="win_count")

def win_rate2(count2):
    if count2==1:
        canvas.create_image(500, 450, anchor=NW, image=win1_image, tags="win_count")
    elif count2==2:
        canvas.create_image(550, 450, anchor=NW, image=win1_image2, tags="win_count")
    elif count2==3:
        canvas.create_image(600, 450, anchor=NW, image=win1_image3, tags="win_count")
    elif count2==4:
        canvas.create_image(650, 450, anchor=NW, image=win1_image4, tags="win_count")

def finalshow():
    final()
    endshow()
def print_text(texter):
    class printer:
        def __init__(self, text):
            self.text= text
        def write(self, str):
            self.text.insert(END,str)
        def flush(self):
            pass
    sys.stdout= printer(texter)



def endgame():
    started.destroy()
    start.destroy()
def startre():

    clear_text()
    started.withdraw()
    start.deiconify()


def clear_text():
    user_text.delete('1.0',END)
    user1.restart()
    user2.restart()
    canvas.delete("winner")
    canvas.delete("cards")

def register_text():
    global register_id, register_pd , register_name
    register_id = register_id_entry.get()
    register_pd = register_pd_entry.get()
    register_name = register_name_entry.get()

    register_excess(register_id,register_pd,register_name)
def register_excess(a,b,c):
    global r
    r.rpush(c,a)
    r.rpush(c,b)
    #r.set(a,a)
    #r.set(b,b)
    messagebox.showinfo("Poker Game","회원가입 완료!")
    register.withdraw()
    login.deiconify()

def login_text():
    global id,passwd,name
    id = login_entry.get()
    passwd = passwd_entry.get()
    name = name_entry.get()
    login_excess(id,passwd,name)

def login_excess(a,b,c):
    values = r.lrange(c,0,1)
    string_values = [value.decode('utf-8') for value in values]
    print(string_values[0])
    print(string_values[1])
    if string_values[0]==a and string_values[1]==b:
        start.deiconify()
        login.withdraw()
    else:
        messagebox.showinfo("Login Denied", f"로그인실패! 이름, 아이디, 비밀번호 확인!")

def mute():
    global volume, origin_volume
    if volume > 0:
        origin_volume = volume
        volume = 0
        pygame.mixer.music.set_volume(0)
        cardsound.set_volume(0)

    else:
        volume = origin_volume
        pygame.mixer.music.set_volume(volume)
        cardsound.set_volume(volume)

#기록저장 파일
def rankshow():
    with open('rank.txt', 'r') as file:
        rank_open=file.read()
        print(rank_open)
        print_text(rank_text)


def ranking_go():
    started.withdraw()
    ranking.deiconify()

def ranking_back():
    print_text(user_text)
    ranking.withdraw()
    started.deiconify()

def ranking_delete():
    rank_text.delete('1.0', END)

def register_show():
    login.withdraw()
    register.deiconify()

r = redis.Redis("localhost")

start=Tk()
start.geometry("1024x760")
start.title("Poker Game")
start.option_add("*Font","맑은고딕 17")

start_canvas=Canvas(start, width=1400,height=760)
start_canvas.pack()
back_image = PhotoImage(file=r"./포커카드/redblack.png")
start_canvas.create_image(0,0, anchor=NW, image=back_image)
start.withdraw()


started=Toplevel()
started.geometry("1024x560")
started.title("Poker Game")
started.option_add("*Font","맑은고딕 17")

started.withdraw()

canvas=Canvas(started, width=1500,height=1000)
canvas.pack()
image = Image.open(r"./포커카드/redblack.png")

login=Toplevel()
login.geometry("300x300")
login.title("Poker Game Login")
login_image= PhotoImage(file=r"./포커카드/redblack.png")
login_canvas=Canvas(login, width=300,height=300)
login_canvas.pack()
login_canvas.create_image(0,0, anchor=NW, image=login_image)
login_canvas.create_text(65, 85, text="ID", fill="white", font=("Helvetica", 24))
login_canvas.create_text(105, 155, text="Password", fill="white", font=("Helvetica", 24))
login_canvas.create_text(80, 25, text="Name", fill="white", font=("Helvetica", 24))
#login.withdraw()

name_entry = Entry(login)
name_entry.place(x=50,y=40)

login_entry = Entry(login)
login_entry.place(x=50,y=100)

passwd_entry = Entry(login)
passwd_entry.place(x=50,y=170)

register=Toplevel()
register.geometry("400x400")
register.title("Register")
register_canvas=Canvas(register, width=400,height=400)
register_canvas.pack()
register_canvas.create_image(0,0, anchor=NW, image=login_image)
register.withdraw()

registerGO_btn=Button(login)
registerGO_btn.config(width=5,height=1,text="회원가입")
registerGO_btn.config(command=register_show)
registerGO_btn.config(bd=3,bg="white",font=("Helvetica",12,"bold"))
registerGO_btn.pack()
button_register_go=login_canvas.create_window(150,220,anchor=NW,window=registerGO_btn)


register_id_entry = Entry(register)
register_id_entry.place(x=50,y=100)

register_pd_entry = Entry(register)
register_pd_entry.place(x=50,y=170)

register_name_entry = Entry(register)
register_name_entry.config(width=10)
register_name_entry.place(x=50,y=30)

register_canvas.create_text(65, 85, text="ID", fill="white", font=("Helvetica", 24))
register_canvas.create_text(105, 155, text="Password", fill="white", font=("Helvetica", 24))
register_canvas.create_text(81, 18, text="Name", fill="white", font=("Helvetica", 24))

register_button=Button(register)
register_button.config(width=5,height=1)
register_button.config(text="회원가입")
register_button.config(command=register_text)
register_button.config(bd=3)
register_button.config(bg="white")
register_button.config(font=("Helvetica", 12, "bold"))
register_button.pack()
button_register=register_canvas.create_window(220,220,anchor=NW, window=register_button)
#랭킹창
ranking=Toplevel()
ranking.geometry("1024x670")
ranking.title("RANKING")
ranking.withdraw()


login_button=Button(login)
login_button.config(width=5,height=1)
login_button.config(text="로그인")
login_button.config(command=login_text)
login_button.config(bd=3)
login_button.config(bg="white")
login_button.config(font=("Helvetica", 12, "bold"))
login_button.pack()
button_login=login_canvas.create_window(220,220,anchor=NW, window=login_button)
"""
registerGO_btn=Button(login)
registerGO_btn.config(width=5,height=1,text="회원가입")
registerGO_btn.config(command=register_show())
registerGO_btn.config(bd=3,bg="white",font=("Helvetica",12,"bold"))
#registerGO_btn.pack()
button_register_go=login_canvas.create_window(160,220,anchor=NW,window=registerGO_btn)
"""

play_image = ImageTk.PhotoImage(image)
canvas.create_image(0,0,anchor=NW, image=play_image,tags="background")
canvas.create_text(370, 27, text="Player_1", fill="white", font=("Helvetica", 24))
canvas.create_text(370, 227, text="Player_2", fill="white", font=("Helvetica", 24))
canvas.create_text(110, 420, text="Card Draw(Press for Two)", fill="white", font=("Helvetica", 24))
canvas.create_text(550, 330, text="Player(1)", fill="white", font=("Helvetica", 20))
canvas.create_text(550, 430, text="Player(2)", fill="white", font=("Helvetica", 20))
win_image=PhotoImage(file=r"./포커카드/medal.png")
win_image2=PhotoImage(file=r"./포커카드/medal.png")
win_image3=PhotoImage(file=r"./포커카드/medal.png")
win_image4=PhotoImage(file=r"./포커카드/medal.png")
win1_image=PhotoImage(file=r"./포커카드/medal.png")
win1_image2=PhotoImage(file=r"./포커카드/medal.png")
win1_image3=PhotoImage(file=r"./포커카드/medal.png")
win1_image4=PhotoImage(file=r"./포커카드/medal.png")

#카드 이미지로드
#클로버
c2=PhotoImage(file=r"./포커카드/c2.gif")
c3=PhotoImage(file=r"./포커카드/c3.gif")
c4=PhotoImage(file=r"./포커카드/c4.gif")
c5=PhotoImage(file=r"./포커카드/c5.gif")
c6=PhotoImage(file=r"./포커카드/c6.gif")
c7=PhotoImage(file=r"./포커카드/c7.gif")
c8=PhotoImage(file=r"./포커카드/c8.gif")
c9=PhotoImage(file=r"./포커카드/c9.gif")
c10=PhotoImage(file=r"./포커카드/c10.gif")
c11=PhotoImage(file=r"./포커카드/c11.gif")
c12=PhotoImage(file=r"./포커카드/c12.gif")
c13=PhotoImage(file=r"./포커카드/c13.gif")
c14=PhotoImage(file=r"./포커카드/c14.gif")
#스페이드
s2=PhotoImage(file=r"./포커카드/s2.gif")
s3=PhotoImage(file=r"./포커카드/s3.gif")
s4=PhotoImage(file=r"./포커카드/s4.gif")
s5=PhotoImage(file=r"./포커카드/s5.gif")
s6=PhotoImage(file=r"./포커카드/s6.gif")
s7=PhotoImage(file=r"./포커카드/s7.gif")
s8=PhotoImage(file=r"./포커카드/s8.gif")
s9=PhotoImage(file=r"./포커카드/s9.gif")
s10=PhotoImage(file=r"./포커카드/s10.gif")
s11=PhotoImage(file=r"./포커카드/s11.gif")
s12=PhotoImage(file=r"./포커카드/s12.gif")
s13=PhotoImage(file=r"./포커카드/s13.gif")
s14=PhotoImage(file=r"./포커카드/s14.gif")
#하트
h2=PhotoImage(file=r"./포커카드/h2.gif")
h3=PhotoImage(file=r"./포커카드/h3.gif")
h4=PhotoImage(file=r"./포커카드/h4.gif")
h5=PhotoImage(file=r"./포커카드/h5.gif")
h6=PhotoImage(file=r"./포커카드/h6.gif")
h7=PhotoImage(file=r"./포커카드/h7.gif")
h8=PhotoImage(file=r"./포커카드/h8.gif")
h9=PhotoImage(file=r"./포커카드/h9.gif")
h10=PhotoImage(file=r"./포커카드/h10.gif")
h11=PhotoImage(file=r"./포커카드/h11.gif")
h12=PhotoImage(file=r"./포커카드/h12.gif")
h13=PhotoImage(file=r"./포커카드/h13.gif")
h14=PhotoImage(file=r"./포커카드/h14.gif")
#다이아몬드
d2=PhotoImage(file=r"./포커카드/d2.gif")
d3=PhotoImage(file=r"./포커카드/d3.gif")
d4=PhotoImage(file=r"./포커카드/d4.gif")
d5=PhotoImage(file=r"./포커카드/d5.gif")
d6=PhotoImage(file=r"./포커카드/d6.gif")
d7=PhotoImage(file=r"./포커카드/d7.gif")
d8=PhotoImage(file=r"./포커카드/d8.gif")
d9=PhotoImage(file=r"./포커카드/d9.gif")
d10=PhotoImage(file=r"./포커카드/d10.gif")
d11=PhotoImage(file=r"./포커카드/d11.gif")
d12=PhotoImage(file=r"./포커카드/d12.gif")
d13=PhotoImage(file=r"./포커카드/d13.gif")
d14=PhotoImage(file=r"./포커카드/d14.gif")
###################
win=PhotoImage(file=r"./포커카드/win.gif")
def winning():
    pass
btn_image=PhotoImage(file=r"./포커카드/startbutton.png")
btn=Button(start,image=btn_image)
btn.config(width=1024,height=760)
btn.config(text="게임시작")
btn.config(command=gstart)
btn.config(bd=3)
btn.config(bg="white")
btn.config(font=("Helvetica", 20, "bold"))
#btn.grid(row=1,column=0,padx=430,pady=300)
btn.pack()
button_window=start_canvas.create_window(0,0,anchor=NW, window=btn)
"""
cbtn=Button(started)
cbtn.config(width=15,height=1)
cbtn.config(text="카드만들기")
cbtn.config(command=cardmake)
cbtn.pack()
"""
"""
entry=Entry(started)

entry.pack()
"""
ubtn_image=PhotoImage(file=r"./포커카드/cardss.png")
ubtn=Button(started,image=ubtn_image)
ubtn.config(width=100,height=105)
ubtn.config(text="유저(1) 카드뽑기")
ubtn.config(font=("Helvetica", 14, "bold"))
ubtn.config(bg="brown")
ubtn.config(bd=3)
ubtn.config(command=usermake)
ubtn.pack()
ubtn_window=canvas.create_window(10,445,anchor=NW, window=ubtn)

ubtn2_image=PhotoImage(file=r"./포커카드/cardss.png")
ubtn2=Button(started,image=ubtn2_image)
ubtn2.config(width=100,height=105)
ubtn2.config(text="유저(2) 카드뽑기")
ubtn2.config(font=("Helvetica", 14, "bold"))
ubtn2.config(bg="brown")
ubtn2.config(bd=3)
ubtn2.config(command=usermake2)
ubtn2.pack()
ubtn2_window=canvas.create_window(190,445,anchor=NW, window=ubtn2)

fight=Button(started)
fight.config(width=15,height=1)
fight.config(text="승패 보기")
fight.config(font=("Helvetica", 14, "bold"))
fight.config(bg="silver")
fight.config(bd=3)
fight.config(command=finalshow)
fight.pack()
fight_window=canvas.create_window(745,420,anchor=NW, window=fight)


shutdown=PhotoImage(file=r"./포커카드/shutdown.png")
tryagain=Button(started, image=shutdown)
tryagain.config(width=30,height=30)
tryagain.config(text="게임종료")
tryagain.config(font=("Helvetica", 14, "bold"))
tryagain.config(bg="red")
tryagain.config(bd=3)
tryagain.config(command=endgame)
tryagain.pack()
tryagain_window=canvas.create_window(980,5,anchor=NW, window=tryagain)


restart_button=Button(started)
restart_button.config(width=15,height=1)
restart_button.config(text="Deck Shuffle")
restart_button.config(font=("Helvetica", 14, "bold"))
restart_button.config(bg="silver")
restart_button.config(bd=3)
restart_button.config(command=clear_text)
restart_button.pack()
restart_window=canvas.create_window(745,320,anchor=NW, window=restart_button)

restart1_image=PhotoImage(file=r"./포커카드/restart.png")
restart1_button=Button(started,image=restart1_image)
restart1_button.config(width=30,height=30)
restart1_button.config(text="재시작")
restart1_button.config(font=("Helvetica", 14, "bold"))
restart1_button.config(bg="yellow")
restart1_button.config(bd=3)
restart1_button.config(command=startre)
restart1_button.pack()
restart1_window=canvas.create_window(938,5,anchor=NW, window=restart1_button)

user_text=Text(started,width=35, height=10)
user_text.pack()
user_text_window=canvas.create_window(580,50,anchor=NW, window=user_text)

print_text(user_text)

rank_text=Text(ranking,width=35, height=20)
rank_text.pack()

rank_go=Button(started,text="rank",command=ranking_go,width=5,height=1)
rank_go.place(x=800,y=5)

rank_back=Button(ranking,text="back",command=ranking_back,width=5,height=1)
rank_back.pack()

ranking_show=Button(ranking,text="show",command=rankshow,width=5,height=1)
ranking_show.pack()

ranking_del=Button(ranking,text="delete",command=ranking_delete,width=5,height=1)
ranking_del.pack()
"""
result=Button(started)
result.config(width=10,height=1)
result.config(text="족보 보기")
result.config(command=endshow)
result.pack()
"""

card_images ={
    'Spade' : {
        '2': s2,
        '3': s3,
        '4': s4,
        '5': s5,
        '6': s6,
        '7': s7,
        '8': s8,
        '9': s9,
        '10': s10,
        '11': s11,
        '12': s12,
        '13': s13,
        '14': s14
    },
    'Club' : {
        '2': c2,
        '3': c3,
        '4': c4,
        '5': c5,
        '6': c6,
        '7': c7,
        '8': c8,
        '9': c9,
        '10': c10,
        '11': c11,
        '12': c12,
        '13': c13,
        '14': c14
    },
    'Heart' : {
        '2': s2,
        '3': s3,
        '4': s4,
        '5': s5,
        '6': s6,
        '7': s7,
        '8': s8,
        '9': s9,
        '10': s10,
        '11': s11,
        '12': s12,
        '13': s13,
        '14': s14
    },
    'Diamond' : {
        '2': s2,
        '3': s3,
        '4': s4,
        '5': s5,
        '6': s6,
        '7': s7,
        '8': s8,
        '9': s9,
        '10': s10,
        '11': s11,
        '12': s12,
        '13': s13,
        '14': s14

    }
}
def toggle_image():
    current_state = canvas.itemcget(cardh_button_window, "state")
    current_state1 = canvas.itemcget(cardh1_button_window, "state")
    current_state2 = canvas.itemcget(cardh2_button_window, "state")
    current_state3 = canvas.itemcget(cardh3_button_window, "state")
    statelist=[current_state,current_state1,current_state2,current_state3]
    for i in statelist:
        if i == "hidden" :
            canvas.itemconfig(cardh_button_window, state="normal")
            canvas.itemconfig(cardh1_button_window, state="normal")
            canvas.itemconfig(cardh2_button_window, state="normal")
            canvas.itemconfig(cardh3_button_window, state="normal")
        else:
            canvas.itemconfig(cardh_button_window, state="hidden")
            canvas.itemconfig(cardh1_button_window, state="hidden")
            canvas.itemconfig(cardh2_button_window, state="hidden")
            canvas.itemconfig(cardh3_button_window, state="hidden")
def toggle_image1():
    current_state4 = canvas.itemcget(cardh4_button_window, "state")
    current_state5 = canvas.itemcget(cardh5_button_window, "state")
    current_state6 = canvas.itemcget(cardh6_button_window, "state")
    current_state7 = canvas.itemcget(cardh7_button_window, "state")
    statelist=[current_state4,current_state5,current_state6,current_state7]
    for i in statelist:
        if i == "hidden" :
            canvas.itemconfig(cardh4_button_window, state="normal")
            canvas.itemconfig(cardh5_button_window, state="normal")
            canvas.itemconfig(cardh6_button_window, state="normal")
            canvas.itemconfig(cardh7_button_window, state="normal")
        else:
            canvas.itemconfig(cardh4_button_window, state="hidden")
            canvas.itemconfig(cardh5_button_window, state="hidden")
            canvas.itemconfig(cardh6_button_window, state="hidden")
            canvas.itemconfig(cardh7_button_window, state="hidden")
def audio(file_path):
    pygame.mixer.init()
    cardsound.play()
#카드가리개
cardh_image=PhotoImage(file=r"./포커카드/cardhide.gif")
cardh_button=Button(started)
cardh_button.config(image=cardh_image)
cardh_button.config(width=80,height=120)
#cardh_button.config(command=toggle_image)
cardh_button_window=canvas.create_window(55,40,anchor=NW, window=cardh_button)

cardh1_image=PhotoImage(file=r"./포커카드/cardhide.gif")
cardh1_button=Button(started)
cardh1_button.config(image=cardh_image)
cardh1_button.config(width=80,height=120)
#cardh1_button.config(command=toggle_image)
cardh1_button_window=canvas.create_window(155,40,anchor=NW, window=cardh1_button)

cardh2_image=PhotoImage(file=r"./포커카드/cardhide.gif")
cardh2_button=Button(started)
cardh2_button.config(image=cardh_image)
cardh2_button.config(width=80,height=120)
#cardh2_button.config(command=toggle_image)
cardh2_button_window=canvas.create_window(255,40,anchor=NW, window=cardh2_button)

cardh3_image=PhotoImage(file=r"./포커카드/cardhide.gif")
cardh3_button=Button(started)
cardh3_button.config(image=cardh_image)
cardh3_button.config(width=80,height=120)
#cardh3_button.config(command=toggle_image)
cardh3_button_window=canvas.create_window(355,40,anchor=NW, window=cardh3_button)

#아래쪽 카드가리개
#cardh_image=PhotoImage(file=r".\포커카드\cardhide.gif")
cardh4_button=Button(started)
cardh4_button.config(image=cardh_image)
cardh4_button.config(width=80,height=120)
#cardh_button.config(command=toggle_image)
cardh4_button_window=canvas.create_window(55,240,anchor=NW, window=cardh4_button)

#cardh1_image=PhotoImage(file=r".\포커카드\cardhide.gif")
cardh5_button=Button(started)
cardh5_button.config(image=cardh_image)
cardh5_button.config(width=80,height=120)
#cardh1_button.config(command=toggle_image)
cardh5_button_window=canvas.create_window(155,240,anchor=NW, window=cardh5_button)

#cardh6_image=PhotoImage(file=r".\포커카드\cardhide.gif")
cardh6_button=Button(started)
cardh6_button.config(image=cardh_image)
cardh6_button.config(width=80,height=120)
#cardh2_button.config(command=toggle_image)
cardh6_button_window=canvas.create_window(255,240,anchor=NW, window=cardh6_button)

#cardh7_image=PhotoImage(file=r".\포커카드\cardhide.gif")
cardh7_button=Button(started)
cardh7_button.config(image=cardh_image)
cardh7_button.config(width=80,height=120)
#cardh3_button.config(command=toggle_image)
cardh7_button_window=canvas.create_window(355,240,anchor=NW, window=cardh7_button)
#카드가리개 오픈
open_image=PhotoImage(file=r"./포커카드/opene.gif")
open_button=Button(started)
open_button.config(image=open_image)
open_button.config(command=toggle_image)
open_button.config(width=45,height=20)
open_button_window=canvas.create_window(431,13,anchor=NW, window=open_button)

open_image1=PhotoImage(file=r"./포커카드/opene.gif")
open_button1=Button(started)
open_button1.config(image=open_image1)
open_button1.config(command=toggle_image1)
open_button1.config(width=45,height=20)
open_button1_window=canvas.create_window(435,213,anchor=NW, window=open_button1)

mute_image=PhotoImage(file=r"./포커카드/mute.gif")
mute_button=Button(started,width=45,height=35,text="mute",command=mute)
mute_button.config(image=mute_image)
mute_button_window=canvas.create_window(885,4,anchor=NW, window=mute_button)

origin_volume=0
pygame.mixer.init()
volume=0.4
cardsound = pygame.mixer.Sound(r"./포커카드/cardsound.mp3")
bgm=r"./포커카드/bgm.mp3"
pygame.mixer.music.load(bgm)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume)
def shoot():
    global card_images
    global user1

    for i, card_info in enumerate(user1.hand):
        suit, number = card_info
        x = 100 + i * 100
        y = 100
        image_path = "./포커카드/{}{}.gif".format(suit[0].lower(), number)
        image = Image.open(image_path)
        card_image = ImageTk.PhotoImage(image)
        card_images[(suit, number)] = card_image
        image_item = canvas.create_image(x, y, anchor="center", image=card_image,tags="cards")
        canvas.tag_raise(image_item)
def shoot1():
    global card_images
    global user2

    for i, card_info in enumerate(user2.hand):
        suit, number = card_info
        x = 100 + i * 100
        y = 300
        image_path = "./포커카드/{}{}.gif".format(suit[0].lower(), number)
        image = Image.open(image_path)
        card_image = ImageTk.PhotoImage(image)
        card_images[(suit, number)] = card_image
        image_item = canvas.create_image(x, y, anchor="center", image=card_image, tags="cards")
        canvas.tag_raise(image_item)




"""
res_button=Button(started)
res_button.config(width=15,height=1)
res_button.config(text="테스트")
res_button.config(command=shoot)
res_button.pack()
res_window=canvas.create_window(200,480,anchor=NW, window=res_button)
"""

started.mainloop()
start.mainloop()
