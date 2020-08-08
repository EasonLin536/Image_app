import sys
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image


class ImageApp():
    def __init__(self, master):
        master.title("Image Tool")
        title_icon = PhotoImage(file="icons/picture.png")
        master.tk.call('wm', 'iconphoto', master._w, title_icon)
        
        # define
        self.window_width = 1000
        self.window_height = 600
        self.toolbar = Frame(master)
        self.ori_img_pil = None
        self.img_pil = None
        self.canvas = Canvas(master, height=self.window_height, width=self.window_width, bg="gray")
        self.canvas_img = None

        # image variables
        self.img_x = 0
        self.img_y = 0
        self.img_w = 0
        self.img_h = 0
        
        # crop
        self.crop = False
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.cur_x = None
        self.cur_y = None

        # mat
        self.mat = False
        self.pick_1 = False # True: picked, False: not picked
        self.pick_2 = False # True: picked, False: not picked
        self.r_1 = self.g_1 = self.b_1 = 0
        self.r_2 = self.g_2 = self.b_2 = 0

        # mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        # button
        self.open_tk  = ImageTk.PhotoImage(Image.open("icons/folder.png").resize((30, 30)))
        self.save_tk  = ImageTk.PhotoImage(Image.open("icons/save.png").resize((30, 30)))
        self.crop_tk  = ImageTk.PhotoImage(Image.open("icons/crop.png").resize((30, 30)))
        self.mat_tk   = ImageTk.PhotoImage(Image.open("icons/mat.png").resize((30, 30)))
        self.reset_tk = ImageTk.PhotoImage(Image.open("icons/reset.png").resize((30, 30)))
        self.button_open  = Button(self.toolbar, text="open",  image=self.open_tk,  command=self.open_image)
        self.button_save  = Button(self.toolbar, text="save",  image=self.save_tk,  command=self.save_image)
        self.button_crop  = Button(self.toolbar, text="crop",  image=self.crop_tk,  command=self.crop_image)
        self.button_mat   = Button(self.toolbar, text="mat",   image=self.mat_tk,   command=self.mat_image)
        self.button_reset = Button(self.toolbar, text="reset", image=self.reset_tk, command=self.reset_image)

        # position
        self.canvas.pack(side=TOP)
        self.button_open.pack(side=LEFT, padx=10, pady=10)
        self.button_save.pack(side=LEFT, padx=10, pady=10)
        self.button_crop.pack(side=LEFT, padx=10, pady=10)
        self.button_mat.pack(side=LEFT, padx=10, pady=10)
        self.button_reset.pack(side=LEFT, padx=10, pady=10)
        self.toolbar.pack(side=TOP)


    """Utils"""    
    # update img variables
    def update_img_var(self):
        w, h = self.img_pil.size
        self.img_x = self.window_width/2 - w/2
        self.img_y = self.window_height/2 - h/2
        self.img_w = w
        self.img_h = h


    # refresh canvas images
    def refresh_image(self):
        self.img_in_tk = ImageTk.PhotoImage(self.img_pil)
        if not self.canvas_img: 
            self.canvas.delete(self.canvas_img)
        self.canvas_img = self.canvas.create_image(self.window_width/2, self.window_height/2, anchor=CENTER, image=self.img_in_tk)


    # make sure only 1 function is currently using
    def reset_flag(self):
        self.crop = False
        self.mat = False
        self.pick_1 = False
        self.pick_2 = False
        self.canvas.config(cursor="")


    """Interface"""
    # method for mouse function
    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x) - self.img_x
        self.start_y = self.canvas.canvasy(event.y) - self.img_y
        if self.start_x < 0: self.start_x = 0
        elif self.start_x > self.img_w: self.start_x = self.img_w
        if self.start_y < 0: self.start_y = 0
        elif self.start_y > self.img_h: self.start_y = self.img_h
        
        if self.crop: 
            # create rectangle if not yet exist
            print(f"Start at ({self.start_x}, {self.start_y})")
            if not self.rect:
                self.rect = self.canvas.create_rectangle(0, 0, 1, 1, width=5, outline='black')
        
        elif self.mat:
            if not self.pick_1:
                self.r_1, self.g_1, self.b_1 = self.pick_color()
                self.pick_1 = True

            elif self.pick_1 and not self.pick_2:
                self.r_2, self.g_2, self.b_2 = self.pick_color()
                self.pick_2 = True

            if self.pick_1 and self.pick_2:
                self.remove_color()


    def on_move_press(self, event):
        self.cur_x = self.canvas.canvasx(event.x) - self.img_x
        self.cur_y = self.canvas.canvasy(event.y) - self.img_y
        if self.cur_x < 0: self.cur_x = 0
        elif self.cur_x > self.img_w: self.cur_x = self.img_w
        if self.cur_y < 0: self.cur_y = 0
        elif self.cur_y > self.img_h: self.cur_y = self.img_h

        if self.crop:
            print(f"End at ({self.cur_x}, {self.cur_y})", end="\t\t\r")
            self.canvas.coords(self.rect, self.start_x + self.img_x, self.start_y + self.img_y,\
                self.cur_x + self.img_x, self.cur_y + self.img_y)


    def on_button_release(self, event):
        if self.crop:
            self.img_pil = self.img_pil.crop((self.start_x, self.start_y, self.cur_x, self.cur_y))
            self.update_img_var()

            self.canvas.delete(self.rect)
            self.rect = None

            self.canvas.config(cursor="")
            self.crop = False

            self.refresh_image()
            print("\n========== Image cropped ==========\n")

        elif self.mat and self.pick_1 and self.pick_2:
            self.mat = False
            print("========== Image matted ==========\n")

    
    """Button Functions"""
    # open and fit the input image to the window
    def open_image(self):
        print("========== Open image ==========")
        in_fname = filedialog.askopenfilename(title="Select image")
        img = Image.open(in_fname)
        w, h = img.size
        
        print(f"Original image size: {w}x{h}")
        
        resize_flag = False

        if w > self.window_width:
            h = int(h * self.window_width / w)
            w = self.window_width
            resize_flag = True

        if h > self.window_height:
            w = int(w * self.window_height / h)
            h = self.window_height
            resize_flag = True

        if resize_flag:
            print(f"Resize image size: {w}x{h}")
            self.ori_img_pil = self.img_pil = img.resize((w,h))
        else:
            self.ori_img_pil = self.img_pil = img

        self.update_img_var()
        self.refresh_image()
        
        print("========== Image opened ==========\n")


    # method for crop
    def crop_image(self):
        self.reset_flag()
        print("========== Crop image ==========")
        print("Drag for desired crop box")
        self.canvas.config(cursor="cross")
        self.crop = True


    # method for save
    def save_image(self):
        self.reset_flag()
        print("========== Save image ==========")
        fname = filedialog.asksaveasfile(mode='w')
        if not fname:
            return
        self.img_pil.save(fname.name)
        print("========== Image saved ==========\n")


    # method for reset
    def reset_image(self):
        self.reset_flag()
        print("========== Reset image ==========")
        self.img_pil = self.ori_img_pil
        self.refresh_image()
        print("========== Image reset ==========\n")


    # method for matting
    def pick_color(self):
        rgb_im = self.ori_img_pil.convert('RGB')
        r, g, b = rgb_im.getpixel((self.start_x, self.start_y))
        print("Picked color :", r, g, b)

        return r, g, b


    def remove_color(self):
        threshold = 5

        print("Remove color in range")
        if self.r_1 > self.r_2: self.r_1, self.r_2 = self.r_2, self.r_1
        if self.g_1 > self.g_2: self.g_1, self.g_2 = self.g_2, self.g_1
        if self.b_1 > self.b_2: self.b_1, self.b_2 = self.b_2, self.b_1

        print(f"range of r: ({self.r_1}, {self.r_2})")
        print(f"range of g: ({self.g_1}, {self.g_2})")
        print(f"range of b: ({self.b_1}, {self.b_2})")

        self.img_pil = self.img_pil.convert("RGBA")
        datas = self.img_pil.getdata()

        newData = []
        for item in datas:
            if item[0] in range(self.r_1 - threshold, self.r_2 + 1 + threshold) and \
                item[1] in range(self.g_1 - threshold, self.g_2 + 1 + threshold) and \
                item[2] in range(self.b_1 - threshold, self.b_2 + 1 + threshold):
                newData.append((item[0], item[1], item[2], 0))
            else:
                newData.append(item)

        self.img_pil.putdata(newData)
        self.refresh_image()


    def mat_image(self):
        self.reset_flag()
        print("Pick 2 colors for color range")
        self.mat = True
        self.pick_1 = False
        self.pick_2 = False
    

if __name__ == "__main__":
    root = Tk()
    app = ImageApp(root)
    root.mainloop()