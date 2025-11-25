"""
Jatin Gandhi., 
Fun way to create non-rectangle GUI window with TKInter
"""
import tkinter as tk



# FILLCOLOR = "skyblue"
# OUTLINECOLOR = "skyblue"

FILLCOLOR = "black"
OUTLINECOLOR = "white"

WIDTH=600
HEIGHT=600
# Create main window
root = tk.Tk()
root.overrideredirect(True)  # Remove window border and title bar
root.geometry(f"{WIDTH}x{HEIGHT}+100+100")  # Set size and position
root.wm_attributes("-topmost", True)  # Keep window on top
root.wm_attributes("-transparentcolor", "pink")  # Make pink transparent (Windows only)


# Set transparent background color
root.config(bg='pink')

# Canvas to draw custom shape
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='pink', highlightthickness=0)
canvas.pack()

# Draw a circular shape
canvas.create_oval(0, 0, WIDTH - 4, HEIGHT - 4, fill=FILLCOLOR, outline=OUTLINECOLOR)

# Window dragging functionality
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

canvas.bind("<ButtonPress-1>", start_move)
canvas.bind("<ButtonRelease-1>", stop_move)
canvas.bind("<B1-Motion>", do_move)

# Close window on Escape key
root.bind("<Escape>", lambda e: root.destroy())
label_ip1 = tk.Label(root, text="Hollow World!",fg="white",bg=FILLCOLOR, font=("Arial", 24,"italic"))
label_ip1.place(x=WIDTH/4 + 40,y=(HEIGHT/2) - 40); # x and y -> tiral-error
root.mainloop()
