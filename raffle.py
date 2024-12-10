import random
import tkinter as tk
from tkinter import messagebox


def read_names_from_file():
    names = []
    try:
        with open('class_names.txt', 'r') as file:
            for line in file.readlines():
                names.append(line.strip())
    except FileNotFoundError:
        messagebox.showerror('错误', '未找到包含班级同学名字的文件，请确保class_names.txt存在。')
    return names


def read_winners_file():
    winners = set()
    try:
        with open('winners.txt', 'r') as file:
            for line in file.readlines():
                winners.add(line.strip())
    except FileNotFoundError:
        pass
    return winners


def write_winner_to_file(winner):
    try:
        with open('winners.txt', 'a') as file:
            file.write(winner + '\n')
    except IOError:
        messagebox.showerror('错误', '写入中奖者文件失败，请检查文件系统。')


def lottery(names, winners):
    available_names = [name for name in names if name not in winners]
    if not available_names:
        return '没有可供抽奖的名字，请检查名单文件。'
    index = random.randint(0, len(available_names) - 1)
    winner = available_names[index]
    write_winner_to_file(winner)
    return winner


def start_lottery():
    names = read_names_from_file()
    winners = read_winners_file()
    winner = lottery(names, winners)
    result_label.config(text=f'本次中奖的幸运同学是：{winner}', font=('Arial', int(20 * 2 / 3)))
    if tk.messagebox.askyesno('抽奖', '是否继续抽奖?'):
        start_lottery()
    else:
        root.destroy()


root = tk.Tk()
root.title('班级人名抽奖')

# 设置窗口大小为400x300
root.geometry('500x300')

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口的x和y坐标，使其居中
x = (screen_width - 400) / 2
y = (screen_height - 600) / 2
root.geometry('+%d+%d' % (x, y))

# 创建一个Canvas
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# 假设这里有一张名为background.png的图片，你可以根据实际情况替换
try:
    background_image = tk.PhotoImage(file="background.png")
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
except tk.TclError:
    pass

# 在Canvas上创建按钮
start_button = tk.Button(canvas, text='开始抽奖', command=start_lottery, relief='raised', borderwidth=2, width=10,
                         height=1)
canvas.create_window(200, 100, window=start_button)

# 在Canvas上创建结果显示标签
result_label = tk.Label(canvas, text='')
result_label.config(font=('Arial', int(20 * 2 / 3)))
canvas.create_window(200, 150, window=result_label)

root.mainloop()
