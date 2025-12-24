import tkinter as tk
from tkinter import messagebox
import time
import threading
from collections import deque

# =======================
# CONFIG
# =======================
TOTAL_MEMORY = 1024
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

MEMORY_BAR_WIDTH = 420
MEMORY_BAR_HEIGHT = 480

FREE_COLOR = "#BBDEFB"
OCCUPIED_COLOR = "#C8E6C9"
FRAG_COLOR = "#FFCDD2"
FAILED_COLOR = "#E0E0E0"

FREE_COLOR = "#BBDEFB"
USED_COLOR = "#C8E6C9"
FRAG_COLOR = "#FFCDD2"
BUDDY_COLOR = "#D1C4E9"
# =======================
# MAIN CLASS
# =======================
class OS_Simulator:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Memory & Page Replacement Simulator")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg="white")

        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.clear()
        self.show_intro()

    # -----------------------
    # CLEAR
    # -----------------------
    def clear(self):
        for w in self.root.winfo_children():
            if w != self.canvas:
                w.destroy()
        self.canvas.delete("all")

    # -----------------------
    # INTRO
    # -----------------------
    def show_intro(self):
        self.clear()
        text_item = self.canvas.create_text(
            WINDOW_WIDTH//2, WINDOW_HEIGHT//2-60,
            text="", font=("Helvetica", 26, "bold"),
            justify="center"
        )

        msg = (
            "Hello dear teacher,\n\n"
            "Welcome to Operating System\n"
            "Memory & Page Replacement Simulator"
        )

        def animate():
            s = ""
            for c in msg:
                s += c
                self.canvas.itemconfig(text_item, text=s)
                time.sleep(0.04)
            time.sleep(1)
            self.root.after(0, self.main_menu)

        threading.Thread(target=animate).start()

    # -----------------------
    # MAIN MENU
    # -----------------------
    def main_menu(self):
        self.clear()
        self.canvas.create_text(
            WINDOW_WIDTH//2, 100,
            text="Choose Topic",
            font=("Helvetica", 22, "bold")
        )

        tk.Button(
            self.root, text="Fixed Size Partition",
            font=("Helvetica", 14),
            width=30,
            command=self.partition_type
        ).place(x=WINDOW_WIDTH//2 - 170, y=200)

        tk.Button(
            self.root, text="Page Replacement Algorithm",
            font=("Helvetica", 14, "bold"),
            width=30,
            bg="red", fg="white",
            command=self.page_replacement_menu
        ).place(x=WINDOW_WIDTH//2 - 170, y=270)

        tk.Button(self.root, text="Buddy System",
                  width=35, font=("Helvetica", 14),
                  command=self.buddy_menu).place(x=WINDOW_WIDTH//2-200, y=340)

    # ========================
    # -----------------------
    # MEMORY PARTITION MODULE
    # -----------------------
    # -----------------------
    def partition_type(self):
        self.clear()
        self.canvas.create_text(
            WINDOW_WIDTH//2, 80,
            text="Total Main Memory = 1 GB (1024 MB)",
            font=("Helvetica", 22, "bold")
        )

        self.canvas.create_text(
            WINDOW_WIDTH//2, 140,
            text="Choose Partition Type",
            font=("Helvetica", 16)
        )

        tk.Button(
            self.root, text="Fixed Size Partition",
            font=("Helvetica", 14),
            width=25, command=self.ask_partition_count
        ).place(x=WINDOW_WIDTH//2 - 150, y=220)

        tk.Button(
            self.root, text="Back",
            command=self.main_menu
        ).place(x=20, y=20)

    # -----------------------
    # ASK PARTITION COUNT
    # -----------------------
    def ask_partition_count(self):
        self.clear()
        self.canvas.create_text(
            WINDOW_WIDTH//2, 160,
            text="How many partitions do you want?",
            font=("Helvetica", 18)
        )

        self.part_count_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.part_count_entry.place(x=WINDOW_WIDTH//2 - 60, y=210)

        tk.Button(
            self.root, text="Submit",
            font=("Helvetica", 12),
            command=self.partition_count_submit
        ).place(x=WINDOW_WIDTH//2 - 30, y=250)

    # -----------------------
    # PARTITION COUNT SUBMIT
    # -----------------------
    def partition_count_submit(self):
        try:
            self.partition_count = int(self.part_count_entry.get())
            if self.partition_count < 1:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid partition count")
            return

        self.partitions = []
        self.used_memory = 0
        self.current_partition = 1
        self.ask_partition_size()

    # -----------------------
    # ASK PARTITION SIZE
    # -----------------------
    def ask_partition_size(self):
        self.clear()
        if self.current_partition < self.partition_count:
            self.canvas.create_text(
                WINDOW_WIDTH//2, 150,
                text=f"Enter size of Partition {self.current_partition} (MB)",
                font=("Helvetica", 18)
            )
            self.part_size_entry = tk.Entry(self.root, font=("Helvetica", 14))
            self.part_size_entry.place(x=WINDOW_WIDTH//2 - 60, y=200)
            tk.Button(
                self.root, text="Submit",
                command=self.save_partition_size
            ).place(x=WINDOW_WIDTH//2 - 30, y=240)
        else:
            self.partitions.append(TOTAL_MEMORY - self.used_memory)
            self.animate_partitions()

    def save_partition_size(self):
        try:
            size = int(self.part_size_entry.get())
            if size <= 0 or self.used_memory + size >= TOTAL_MEMORY:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid partition size")
            return

        self.partitions.append(size)
        self.used_memory += size
        self.current_partition += 1
        self.ask_partition_size()

    # -----------------------
    # ANIMATE PARTITIONS
    # -----------------------
    def animate_partitions(self):
        self.clear()
        self.draw_memory(self.partitions, None)
        self.canvas.create_text(
            WINDOW_WIDTH//2, 620,
            text="Partitioning Completed",
            font=("Helvetica", 18, "bold"),
            fill="green"
        )

        tk.Button(
            self.root, text="Add Processes",
            font=("Helvetica", 14),
            command=self.ask_process_count
        ).place(x=WINDOW_WIDTH//2 - 90, y=650-40)

        tk.Button(
            self.root, text="Back to Main Menu",
            font=("Helvetica", 12),
            command=self.main_menu
        ).place(x=20, y=20)

    # -----------------------
    # PROCESS INPUT
    # -----------------------
    def ask_process_count(self):
        self.clear()
        self.canvas.create_text(
            WINDOW_WIDTH//2, 150,
            text=f"How many processes? (Max {len(self.partitions)})",
            font=("Helvetica", 18)
        )
        self.proc_count_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.proc_count_entry.place(x=WINDOW_WIDTH//2 - 60, y=200)
        tk.Button(
            self.root, text="Submit",
            command=self.process_count_submit
        ).place(x=WINDOW_WIDTH//2 - 30, y=240)

    def process_count_submit(self):
        try:
            self.proc_count = int(self.proc_count_entry.get())
            if self.proc_count < 1 or self.proc_count > len(self.partitions):
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid process count")
            return

        self.processes = []
        self.proc_index = 1
        self.ask_process_size()

    def ask_process_size(self):
        self.clear()
        if self.proc_index <= self.proc_count:
            self.canvas.create_text(
                WINDOW_WIDTH//2, 150,
                text=f"Enter size of Process P{self.proc_index} (MB)",
                font=("Helvetica", 18)
            )
            self.proc_size_entry = tk.Entry(self.root, font=("Helvetica", 14))
            self.proc_size_entry.place(x=WINDOW_WIDTH//2 - 60, y=200)
            tk.Button(
                self.root, text="Submit",
                command=self.save_process_size
            ).place(x=WINDOW_WIDTH//2 - 30, y=240)
        else:
            self.algorithm_menu()

    def save_process_size(self):
        try:
            size = int(self.proc_size_entry.get())
            if size <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid size")
            return
        self.processes.append(size)
        self.proc_index += 1
        self.ask_process_size()

    # -----------------------
    # ALGORITHM MENU
    # -----------------------
    def algorithm_menu(self):
        self.clear()
        self.canvas.create_text(
            WINDOW_WIDTH//2, 100,
            text="Choose Allocation Algorithm",
            font=("Helvetica", 22, "bold")
        )
        y = 180
        for name in ["First Fit", "Next Fit", "Best Fit", "Worst Fit"]:
            tk.Button(
                self.root, text=name,
                font=("Helvetica", 14),
                width=20,
                command=lambda n=name: self.run_algorithm(n)
            ).place(x=WINDOW_WIDTH//2 - 120, y=y)
            y += 60

        tk.Button(
            self.root, text="Back",
            command=self.animate_partitions
        ).place(x=20, y=20)

    # -----------------------
    # RUN ALGORITHM
    # -----------------------
    def run_algorithm(self, algo):
        self.clear()
        definitions = {
            "First Fit": "Each process is placed in the first free block large enough.",
            "Next Fit": "Like First Fit, but starts searching from last allocated block.",
            "Best Fit": "Each process goes to the smallest block that fits it.",
            "Worst Fit": "Each process goes to the largest available block."
        }

        text = self.canvas.create_text(
            WINDOW_WIDTH//2, 100,
            text="", font=("Helvetica", 18),
            justify="center"
        )

        def animate_def():
            s = ""
            for c in definitions[algo]:
                s += c
                self.canvas.itemconfig(text, text=s)
                time.sleep(0.04)
            time.sleep(1)
            self.root.after(0, lambda: self.animate_allocation(algo))

        threading.Thread(target=animate_def).start()

    # -----------------------
    # ANIMATE ALLOCATION
    # -----------------------
    def animate_allocation(self, algo):
        self.clear()
        blocks = self.partitions[:]
        used = [False]*len(blocks)
        last = 0
        self.allocations = []

        for i, p in enumerate(self.processes):
            idx = None
            if algo == "First Fit":
                for j in range(len(blocks)):
                    if not used[j] and blocks[j] >= p:
                        idx = j; break
            elif algo == "Next Fit":
                for k in range(len(blocks)):
                    j = (last + k) % len(blocks)
                    if not used[j] and blocks[j] >= p:
                        idx = j; last = j+1; break
            elif algo == "Best Fit":
                fits = [(blocks[j], j) for j in range(len(blocks)) if not used[j] and blocks[j] >= p]
                if fits: idx = min(fits)[1]
            elif algo == "Worst Fit":
                fits = [(blocks[j], j) for j in range(len(blocks)) if not used[j] and blocks[j] >= p]
                if fits: idx = max(fits)[1]

            if idx is not None:
                used[idx] = True
                self.allocations.append((i, idx, blocks[idx]-p))
            else:
                self.allocations.append((i, None, None))

            self.draw_memory(blocks, self.allocations)
            time.sleep(1)

        tk.Button(
            self.root, text="Previous Menu",
            font=("Helvetica", 12),
            command=self.algorithm_menu
        ).place(x=WINDOW_WIDTH-160, y=20)

    # -----------------------
    # DRAW MEMORY
    # -----------------------
    def draw_memory(self, blocks, allocs):
        self.canvas.delete("all")
        x1 = 80
        y1 = 120
        x2 = x1 + MEMORY_BAR_WIDTH

        current_y = y1
        for i, size in enumerate(blocks):
            h = (size/TOTAL_MEMORY)*MEMORY_BAR_HEIGHT
            y2 = current_y + h

            self.canvas.create_rectangle(x1, current_y, x2, y2, fill=FREE_COLOR, outline="black")

            if allocs:
                for a in allocs:
                    if a[1] == i:
                        psize = self.processes[a[0]]
                        ph = (psize/TOTAL_MEMORY)*MEMORY_BAR_HEIGHT
                        self.canvas.create_rectangle(x1, current_y, x2, current_y+ph, fill=OCCUPIED_COLOR)
                        self.canvas.create_rectangle(x1, current_y+ph, x2, y2, fill=FRAG_COLOR)
                        self.canvas.create_text(
                            x2+140, (current_y+y2)//2,
                            text=f"P{a[0]+1} → Fragment {a[2]} MB",
                            font=("Helvetica", 12)
                        )

            self.canvas.create_text(
                (x1+x2)//2, (current_y+y2)//2,
                text=f"{size} MB",
                font=("Helvetica", 12, "bold")
            )
            current_y = y2

    # -----------------------
    # -----------------------
    # PAGE REPLACEMENT MODULE
    # -----------------------
    # -----------------------
    def page_replacement_menu(self):
        self.clear()
        self.canvas.create_text(
            WINDOW_WIDTH//2, 100,
            text="Page Replacement Algorithms",
            font=("Helvetica", 22, "bold")
        )

        tk.Button(
            self.root, text="FIFO Page Replacement",
            font=("Helvetica", 14),
            width=30,
            command=lambda: self.page_input("FIFO")
        ).place(x=WINDOW_WIDTH//2 - 170, y=200)

        tk.Button(
            self.root, text="Optimal Page Replacement",
            font=("Helvetica", 14),
            width=30,
            command=lambda: self.page_input("OPT")
        ).place(x=WINDOW_WIDTH//2 - 170, y=260)

        tk.Button(
            self.root, text="Back",
            command=self.main_menu
        ).place(x=20, y=20)

    def page_input(self, algo):
        self.clear()
        self.page_algo = algo
        self.canvas.create_text(
            WINDOW_WIDTH//2, 120,
            text="Enter Reference String (e.g. 123412512345)",
            font=("Helvetica", 16)
        )
        self.ref_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.ref_entry.place(x=WINDOW_WIDTH//2 - 120, y=160)
        self.canvas.create_text(
            WINDOW_WIDTH//2, 210,
            text="Enter Number of Frames",
            font=("Helvetica", 16)
        )
        self.frame_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.frame_entry.place(x=WINDOW_WIDTH//2 - 120, y=250)
        tk.Button(
            self.root, text="Start Simulation",
            command=self.page_definition
        ).place(x=WINDOW_WIDTH//2 - 80, y=300)

    def page_definition(self):
        try:
            self.ref_string = [int(x) for x in self.ref_entry.get()]
            self.frames = int(self.frame_entry.get())
        except:
            messagebox.showerror("Error", "Invalid input")
            return

        self.clear()
        definitions = {
            "FIFO": "FIFO (First In First Out):\nThe oldest page is replaced first.",
            "OPT": "Optimal: Replaces page used farthest in future."
        }

        text = self.canvas.create_text(
            WINDOW_WIDTH//2, 200,
            text="", font=("Helvetica", 18),
            justify="center"
        )

        def animate():
            s = ""
            for c in definitions[self.page_algo]:
                s += c
                self.canvas.itemconfig(text, text=s)
                time.sleep(0.04)
            time.sleep(1)
            self.root.after(0, self.animate_page_algo)

        threading.Thread(target=animate).start()

    def animate_page_algo(self):
        self.clear()
        frames = []
        queue = deque()
        faults = 0
        start_y = 100

        for i, page in enumerate(self.ref_string):
            hit = page in frames
            if not hit:
                faults += 1
                if len(frames) < self.frames:
                    frames.append(page)
                    queue.append(page)
                else:
                    if self.page_algo == "FIFO":
                        old = queue.popleft()
                        idx = frames.index(old)
                        frames[idx] = page
                        queue.append(page)
                    else:  # OPT
                        future = self.ref_string[i+1:]
                        distances = []
                        for f in frames:
                            if f in future:
                                distances.append(future.index(f))
                            else:
                                distances.append(float('inf'))
                        idx = distances.index(max(distances))
                        frames[idx] = page

            # Draw Step
            self.canvas.create_text(80, start_y + i*35, text=f"{i+1}", font=("Helvetica", 12))
            self.canvas.create_text(120, start_y + i*35, text=f"{page}", font=("Helvetica", 12))
            for j in range(self.frames):
                x = 200 + j*60
                val = frames[j] if j < len(frames) else "-"
                self.canvas.create_rectangle(x, start_y+i*35-15, x+40, start_y+i*35+15)
                self.canvas.create_text(x+20, start_y+i*35, text=val)
            self.canvas.create_text(
                200 + self.frames*60 + 40,
                start_y + i*35,
                text="FAULT" if not hit else "HIT",
                fill="red" if not hit else "green",
                                font=("Helvetica", 12, "bold")
            )
            self.root.update()
            time.sleep(0.7)

        # Total page faults
        self.canvas.create_text(
            WINDOW_WIDTH//2, start_y + len(self.ref_string)*35 + 40,
            text=f"Total Page Faults = {faults}",
            font=("Helvetica", 20, "bold"),
            fill="red"
        )

        tk.Button(
            self.root, text="Back to Main Menu",
            font=("Helvetica", 12),
            command=self.main_menu
        ).place(x=20, y=20)
 # =====================================================
    # BUDDY SYSTEM
    # =====================================================
    def buddy_menu(self):
        self.clear()
        self.canvas.create_text(WINDOW_WIDTH//2, 80,
                                text="Buddy System",
                                font=("Helvetica", 22, "bold"))

        for i, s in enumerate([512, 256, 128, 64]):
            tk.Button(self.root, text=f"Apply Buddy System on {s} MB",
                      width=30, font=("Helvetica", 14),
                      command=lambda x=s: self.animate_buddy(x)
                      ).place(x=WINDOW_WIDTH//2-180, y=160+i*60)

        tk.Button(self.root, text="Back",
                  command=self.main_menu).place(x=20, y=20)

    def animate_buddy(self, size):
        self.clear()
        self.canvas.create_text(WINDOW_WIDTH//2, 40,
                                text=f"Buddy System on {size} MB",
                                font=("Helvetica", 22, "bold"))

        blocks = [(400, 120, 400, 50, size, "A")]

        while blocks:
            x, y, w, h, s, label = blocks.pop(0)
            self.canvas.create_rectangle(x, y, x+w, y+h,
                                         fill=BUDDY_COLOR, outline="black")
            self.canvas.create_text(x+w/2, y+h/2,
                                    text=f"{s} MB ({label})")
            self.root.update()
            time.sleep(1)

            if s <= 32:
                continue

            half = s // 2
            blocks.append((x, y+80, w//2, h, half, label+"L"))
            blocks.append((x+w//2, y+80, w//2, h, half, label+"R"))

        tk.Button(self.root, text="Back",
                  command=self.buddy_menu).place(x=20, y=20)
# =======================
# RUN THE PROGRAM
# =======================
if __name__ == "__main__":
    root = tk.Tk()
    app = OS_Simulator(root)
    root.mainloop()
