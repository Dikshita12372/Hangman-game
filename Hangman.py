import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random


word_lists = {
    "Easy": 
    {
        "map":"Guide",
        "milk":"drink",
        "dog":"animal",
        "train":"vehicle",
        "apple":"fruit",
        "cake":"dessert",
        "desk":"household item",
        "phone":"device"
    },
    "Medium": 
    {
        "teacher":"profession",
        "notebook":"stationery",
        "football":"sport",
        "yogurt":"dairy product",
        "library":"books",
        "cabinet":"house"
    },
    "Hard": 
    {
        "elephant":"animal",
        "earthquake":"disaster",
        "hippopotamus":"animal",
        "constitution":"document",
        "database":"storage"
    }
}

max_lives = {"Easy": 7, "Medium": 7, "Hard": 7}

guessed = []
mistakes = 0
word = ""
hint = ""
difficulty = "Easy"
game_over = False
#drawing--

def draw_human():
    global mistakes

    if mistakes == 1:  # line
        C.create_line(320, 50, 320, 90, width=4, capstyle="round", tags="human")

    elif mistakes == 2:  # Head
        C.create_oval(285, 90, 355, 150, fill="black", outline="black", tags="human")

    elif mistakes == 3:  # Body
        C.create_line(320, 150, 320, 230, width=4, capstyle="round", tags="human")

    elif mistakes == 4:  # right Arm
        C.create_line(320, 148, 358, 180, width=4, capstyle="round", tags="human")     #right

    elif mistakes == 5:  # left Arm
        C.create_line(320, 148, 282, 180, width=4, capstyle="round", tags="human")        #left

    elif mistakes == 6:  # right Leg
        C.create_line(320, 230, 358, 285, width=4, capstyle="round", tags="human")         #right

    elif mistakes == 7:  # left Leg
        C.create_line(320, 230, 282, 285, width=4, capstyle="round", tags="human")          #left
        result_label.config(text="💀 Game Over!", fg="#d32f2f",font=("Times New Roman",20))
        
        global game_over
        game_over = True
        entry.config(state="disabled")
        guess_button.config(state="disabled")
        
        shake_human()

        messagebox.showinfo("You Lost 😢",f"Game Over!\n\nThe correct word was:\n\n👉 {word.upper()}")

#logic--

def guess_letter(letter):
    global mistakes

    if mistakes >= max_lives[difficulty]:
        return
    if letter in guessed:
        result_label.config(text="⚠️ Letter already guessed!", fg="orange",font=("Times New Roman",20))
        return
    
    guessed.append(letter)

    if letter not in word:
        mistakes += 1
        draw_human()

    update_word()

def update_word():
    display = " ".join([c if c in guessed else "_" for c in word])
    word_label.config(text=display)

    if "_" not in display:
        result_label.config(text="🎉 You Win!", fg="#6f4e37",font=("Times New Roman",20))
        global game_over
        game_over = True
        entry.config(state="disabled")
        guess_button.config(state="disabled")

        celebrate()



#reset--

def reset_game():
    global word, guessed, mistakes, hint, game_over

    guessed = []
    mistakes = 0
    game_over = False

    entry.config(state="normal")
    guess_button.config(state="normal")
    entry.focus_set()
    
    result_label.config(text="")

    C.delete("all")
    
    draw_pole()

    word, hint = random.choice(list(word_lists[difficulty].items()))
    hint_label.config(text=f"💡: {hint}")
    update_word()

#difficulty level--

def set_difficulty(value):
    global difficulty
    difficulty = value
    reset_game()


#huamn latkane wala pole--

def draw_pole():
    C.create_line(95, 350, 420, 350, width=6, capstyle="round")      # ground
    C.create_line(150, 350, 150, 38, width=6, capstyle="round")      # vertical pole  
    C.create_line(138, 50, 332, 50, width=6, capstyle="round")       # top 

    C.create_line(200, 50, 150, 100, width=6, capstyle="round")       # top diagonal

    C.create_line(150, 290, 110, 350, width=6, capstyle="round")      # left leg 
    C.create_line(150, 290, 190, 350, width=6, capstyle="round")     # right leg 

#animation

def celebrate(count=0):   #win ka animation
    if count >= 12:
        return

#checks if pura human exist karta hai
    items = C.find_withtag("human")
    if not items:
# nothing exists draw full human body
        C.create_line(320, 50, 320, 90, width=4, capstyle="round", tags="human")       # rope
        C.create_oval(285, 90, 355, 150, fill="black", outline="black", tags="human")  # head
        C.create_line(320, 150, 320, 230, width=4, capstyle="round", tags="human")      # body
        C.create_line(320, 230, 282, 285, width=4, capstyle="round", tags="human")      # left leg
        C.create_line(320, 230, 358, 285, width=4, capstyle="round", tags="human")      # right leg
        #win arms
        C.create_line(320, 148, 282, 180, width=4, tags=("human","arms"))               # left
        C.create_line(320, 148, 358, 180, width=4, tags=("human","arms"))               # right
    else:
# some human parts exist add missing body part
        heads = [i for i in items if C.type(i) == "oval"]   # check head
        if not heads:
            C.create_oval(285, 90, 355, 150, fill="black", outline="black", tags="human")
        
        bodies = [i for i in items if C.type(i) == "line" and C.coords(i) == [320, 150, 320, 230]]# check body
        if not bodies:
            C.create_line(320, 150, 320, 230, width=4, capstyle="round", tags="human")
        
        legs = [i for i in items if "legs" in C.gettags(i)]   # check legs
        if not legs:
            C.create_line(320, 230, 282, 285, width=4, capstyle="round", tags=("human","legs"))
            C.create_line(320, 230, 358, 285, width=4, capstyle="round", tags=("human","legs"))
        
        arms = [i for i in items if "arms" in C.gettags(i)]  # check arms
        if not arms:
            C.create_line(320, 148, 282, 180, width=4, tags=("human","arms"))
            C.create_line(320, 148, 358, 180, width=4, tags=("human","arms"))

#animated arms
    C.delete("arms")
    if count % 2 == 0:
        # arms UP
        C.create_line(320, 150, 280, 120, width=4, tags=("human","arms"))
        C.create_line(320, 150, 360, 120, width=4, tags=("human","arms"))
    else:
        # arms DOWN
        C.create_line(320, 150, 282, 180, width=4, tags=("human","arms"))
        C.create_line(320, 150, 358, 180, width=4, tags=("human","arms"))

    root.after(250, lambda: celebrate(count + 1))   #repeat hoga tabtak jatak count>=12 na ho

def shake_human(count=0):   #lose ka animation
    if count >= 20:
        return

    # move whole drawing left & right
    dx = -5 if count % 2 == 0 else 5
    C.move("human", dx, 0)

    root.after(120, lambda: shake_human(count + 1))

#GUI--

root=Tk()
root.title("Hangman")
C=Canvas(root,height=350,width=550,bg="#aedcda")
C.pack()
draw_pole()

word_label = tk.Label(root, font=("Arial", 18))
word_label.pack(pady=20)

#hint--

hint_label = tk.Label(root,text="",font=("Times New Roman", 18, "bold"),width=20,height=2,wraplength=350,justify="center",
                      anchor="center",bd=2,relief="solid",padx=10,pady=5)

hint_label.pack(pady=8)

result_label = tk.Label(root, font=("Arial", 14),fg="#f44336")
result_label.pack()

# Difficulty selector--

diff_var = tk.StringVar(value="Easy")
difficulty_menu=tk.OptionMenu(root, diff_var, "Easy", "Medium", "Hard", command=set_difficulty)
difficulty_menu.config(font=("Times New Roman",15),bg="#ffc107",fg="black",activebackground="#ff00c8",width=14)
difficulty_menu.pack(pady=6)

# Restart button--

tk.Button(root, text="🔁 Restart", command=reset_game,width=14,bg="blue",fg="white",activebackground="#6BA9E8",
          activeforeground="white",font=("Times New Roman",15)).pack(pady=6)

entry = tk.Entry(root, font=("Arial", 14), width=15, justify="center")
entry.pack(pady=5)

def submit_guess():
    if game_over:
        result_label.config(text=" Game Over! Restart to play again",font=("Times New Roman",20))
        return
    
    letter = entry.get().lower()
    entry.delete(0, tk.END)

    result_label.config(text="")

    if not letter.isalpha() or len(letter) != 1:
        result_label.config(text="⚠ Enter ONE letter", fg="red",font=("Times New Roman",20))
        return
    if letter in guessed:
        result_label.config(text=f"😑 {letter} already guessed!😑", fg="black",font=("Times New Roman",20))
        return

    guess_letter(letter)

guess_button = tk.Button(root, text="Guess", command=submit_guess,width=14,bg="black",fg="white",activebackground="#45a049",activeforeground="white",font=("Times New Roman",15))
guess_button.pack(pady=6)

root.bind("<Return>", lambda event: submit_guess())

reset_game()
root.mainloop()


