import tkinter as tk

def question_ai_red():
    """
    Window to ask what type of player Red should be.
    Returns: The selected type ("ai", "random", or "human").
    """
    window2 = tk.Tk()
    window2.geometry('500x500')
    window2.title("Question IA")

    canvas2 = tk.Canvas(window2, width=500, height=500, bg="white")
    canvas2.pack(fill="both", expand=True)

    canvas2.create_text(200, 200, text="What do you want the player Red to be?", 
                        font=("Arial", 16), fill="black", anchor="center")

    player1_type = tk.StringVar()

    def store_answer(response):
        player1_type.set(response)
        window2.destroy()

    ai_button = tk.Button(window2, text="Ai", command=lambda: store_answer("ai"))
    canvas2.create_window(100, 250, window=ai_button, width=100, height=30)

    random_button = tk.Button(window2, text="Random", command=lambda: store_answer("random"))
    canvas2.create_window(200, 250, window=random_button, width=100, height=30)

    human_button = tk.Button(window2, text="Human", command=lambda: store_answer("human"))
    canvas2.create_window(300, 250, window=human_button, width=100, height=30)

    window2.wait_variable(player1_type)  
    return player1_type.get()


def question_ai_black():
    """
    Window to ask what type of player Black should be.
    Returns: The selected type ("ai", "random", or "human").
    """
    window2 = tk.Tk()
    window2.geometry('500x500')
    window2.title("Question IA")

    canvas2 = tk.Canvas(window2, width=500, height=500, bg="white")
    canvas2.pack(fill="both", expand=True)

    canvas2.create_text(200, 200, text="What do you want the player Black to be?", 
                        font=("Arial", 16), fill="black", anchor="center")

    player2_type = tk.StringVar()

    def store_answer(response):
        player2_type.set(response)
        window2.destroy()

    ai_button = tk.Button(window2, text="Ai", command=lambda: store_answer("ai"))
    canvas2.create_window(100, 250, window=ai_button, width=100, height=30)

    random_button = tk.Button(window2, text="Random", command=lambda: store_answer("random"))
    canvas2.create_window(200, 250, window=random_button, width=100, height=30)

    human_button = tk.Button(window2, text="Human", command=lambda: store_answer("human"))
    canvas2.create_window(300, 250, window=human_button, width=100, height=30)

    window2.wait_variable(player2_type)  
    return player2_type.get()
