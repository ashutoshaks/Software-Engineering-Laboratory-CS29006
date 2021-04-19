from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image

# Dummy lists to store pictures
in_imgs = list()
post_imgs = list()

# User class for representing each user of the social network
class User:
    def __init__(self, id, contact_list):
        self.id = id # Id of the user as a string
        self.contacts = contact_list # List to store all contacts of a user
        self.groups = list() # List to store all the group ids of which the user is a part
        self.in_posts = list() # List to store all the incoming posts for a user

    # Helper function to custom sort the contact and group lists
    def sortItems(self):
        self.contacts.sort(key = lambda item: (len(item), item))
        self.groups.sort(key = lambda item: (len(item), item))

    # Function for printing various updates to the terminal
    def console_user(self):
        print("Current user selected : " + self.id)
        print("Contacts : " + str(self.contacts))
        print("Groups : " + str(self.groups) + "\n")


# Group class to represent each group in the social network
class Group:
    def __init__(self, id, member_list):
        self.id = id # Id of the group as a string
        self.members = member_list # List to store all the members of a group
        self.in_posts = list() # List to store all the messages posted in the group


# Post class to represent each message / post
class Post:
    def __init__(self, sId, type, rId, text, img_path):
        self.sender_id = sId
        self.type = type
        self.receiver_id = rId
        self.text = text
        self.img_path = img_path

    # Function for printing various updates to the terminal
    def console_message(self):
        print("Message sent from " + self.sender_id)
        print("To " + self.type + " " + self.receiver_id + "\n")


# A social network class to encapsulate all operations
class SocialNetwork:
    def __init__(self):
        self.user_list = dict() # A dictionary which maps each user id to its user object
        self.group_list = dict() # A dictionary which maps each group id to its group object

    # Function to extract contact and group information from social_network.txt
    def parse_user_group_list(self):
        file = open("social_network.txt", "r")
        is_user = True
        for line in file:
            if(line[0 : -1] == "#users"):
                continue
            if(line[0 : -1] == "#groups"):
                is_user = False
                continue
            line = line[1 : -2]
            ind = line.find(':')
            id = line[0:ind]
            line = line[ind + 2 : ]
            if(is_user):
                contact_list = line.split(", ")
                self.user_list[id] = User(id, contact_list)
            else:
                member_list = line.split(", ")
                self.group_list[id] = Group(id, member_list)
                for member in member_list:
                    self.user_list[member].groups.append(id)
        file.close()
        for user in obj.user_list.values():
            user.sortItems()

    # Function to read all previous posts
    def parse_messages(self):
        file = open("messages.txt", "r")
        for line in file:
            line = line.strip("\n")
            if(len(line) == 0):
                continue
            sId, type, rId, text, img_path = line.split('$') # split each line using '$' to get the individual fields
            curr_post = Post(sId, type, rId, text, img_path)
            if(type == "U"):
                self.user_list[rId].in_posts.append(curr_post)
            else:
                grp = self.group_list[rId]
                grp.in_posts.append(curr_post)
                for member_id in grp.members:
                    self.user_list[member_id].in_posts.append(curr_post)
        file.close()


# Class for the left frame of the tkinter window
class LeftFrame(Frame):
    def __init__(self, master, rframe):
        global obj
        Frame.__init__(self, master, bg = "cyan")
        self.master = master
        self.rframe = rframe
        self.grid(row = 0, column = 0, sticky = NSEW)
        master.rowconfigure(0, weight = 1)
        master.columnconfigure(0, weight = 1)

        self.lab = Label(self, text = "Please select a user", font = ("Calibri", 13, "bold"), bg = "cyan")
        self.lab.grid(row = 0, column = 0, columnspan = 2, sticky = NSEW)

        # Dropdown menu for selecting the current user
        option_list = ["User #" + val_id for val_id in obj.user_list]
        self.var = StringVar(self)
        self.var.set(option_list[0])
        self.var.trace("w", self.callback)
        self.opt = OptionMenu(self, self.var, *option_list)
        self.opt.config(width = 20, font = ("Calibri", 13, "bold"), bg = "cyan")
        self.opt.grid(row = 1, column = 0, columnspan = 2, sticky = NSEW)

        self.lab_contact = Label(self, text = "Contacts", font = ("Calibri", 13, "bold"), bg = "cyan")
        self.lab_contact.grid(row = 2, column = 0, sticky = NSEW)

        self.lab_group = Label(self, text = "Groups", font = ("Calibri", 13, "bold"), bg = "cyan")
        self.lab_group.grid(row = 2, column = 1, sticky = NSEW)

        # Textbox to display all contacts of the selected user
        self.contact_text = Text(self, width = 30, height = 30)
        self.contact_text.configure(font = ("Calibri", 12))
        self.contact_text.grid(row = 3, column = 0, sticky = NSEW)

        # Textbox to display all groups of which the selected user is a part
        self.group_text = Text(self, width = 30, height = 30)
        self.group_text.configure(font = ("Calibri", 12))
        self.group_text.grid(row = 3, column = 1, sticky = NSEW)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.callback()

    # Function to update the contact and group textboxes each time a new user is selected
    def callback(self, *args):
        global obj
        curr_user = self.var.get()
        ind = curr_user.find('#')
        user_id = curr_user[ind + 1 : ]

        self.contact_text.configure(state = NORMAL)
        self.group_text.configure(state = NORMAL)

        self.contact_text.delete(1.0, END)
        self.group_text.delete(1.0, END)
        
        obj.user_list[user_id].console_user()
        # show contacts
        for contact_id in obj.user_list[user_id].contacts:
            self.contact_text.insert(END, "User #" + contact_id + "\n")
        # show groups
        for group_id in obj.user_list[user_id].groups:
            self.group_text.insert(END, "Group #" + group_id + "\n")

        # Disable the text boxes so that they cannot be altered during execution
        self.contact_text.configure(state = DISABLED)
        self.group_text.configure(state = DISABLED)
        
        self.rframe.create_post_menu(user_id)
        self.rframe.display_in_messages(user_id)


# Class for the right frame of the tkinter window
class RightFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg = "cyan")
        self.master = master
        self.curr_user = ""
        self.curr_text = "" # stores the text for the current message posted
        self.curr_img_path = "" # stores the image path for the current image posted
        self.grid(row = 0, column = 1, sticky = NSEW)

        master.rowconfigure(0, weight = 1)
        master.columnconfigure(1, weight = 1)

        self.l1 = Label(self, text = "", bg = "cyan")
        self.l1.grid(row = 0, column = 0, sticky = NSEW)

        self.l2 = Label(self, text = "", bg = "cyan")
        self.l2.grid(row = 0, column = 1, sticky = NSEW)

        self.lab_in = Label(self, text = "Incoming Messages", font = ("Calibri", 13, "bold"), bg = "cyan")
        self.lab_in.grid(row = 2, column = 0, sticky = NSEW)

        self.lab_post = Label(self, text = "Post Message", font = ("Calibri", 13, "bold"), bg = "cyan")
        self.lab_post.grid(row = 1, column = 1, columnspan = 2)
        
        # Textbox to display all incoming messages for the selected user
        self.in_messages = Text(self, width = 40, height = 28)
        self.in_messages.configure(font = ("Calibri", 12))
        self.in_messages.grid(row = 3, column = 0, sticky = NSEW)

        # Textbox for the selected user to post a new message and/or image
        self.post_messages = Text(self, width = 40, height = 28)
        self.post_messages.configure(font = ("Calibri", 12))
        self.post_messages.grid(row = 3, column = 1, columnspan = 2, sticky = NSEW)

        self.image_button = Button(self, text = "Select Image", font = ("Calibri", 13, "bold"), bg = "cyan", command = self.upload_image)
        self.image_button.grid(row = 4, column = 1, sticky = NSEW)

        self.post_button = Button(self, text = "Post", font = ("Calibri", 13, "bold"), bg = "cyan", command = self.upload_message)
        self.post_button.grid(row = 4, column = 2, sticky = NSEW)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)

    # Function to display an appropriate dropdown menu containing all contacts and groups for the selected user
    # Used for selecting to whom the message has to be sent
    def create_post_menu(self, user_id):
        global obj
        self.curr_user = user_id
        opt_list_contacts = ["User #" + val_id for val_id in obj.user_list[user_id].contacts]
        opt_list_groups = ["Group #" + val_id for val_id in obj.user_list[user_id].groups]
        option_list = opt_list_contacts + opt_list_groups

        self.var = StringVar(self)
        self.var.set(option_list[0])
        self.opt = OptionMenu(self, self.var, *option_list)
        self.opt.config(width = 20, font = ("Calibri", 13, "bold"), bg = "cyan")
        self.opt.grid(row = 2, column = 1, columnspan = 2, sticky = NSEW)
    
    # Function to display all the incoming messages for the selected user
    def display_in_messages(self, user_id):
        global obj
        global img

        self.in_messages.configure(state = NORMAL)

        self.in_messages.delete(1.0, END)
        for post in obj.user_list[user_id].in_posts:
            str = ""
            if(post.type == "U"): # personal message
                str = "From User #" + post.sender_id + " (via Personal) : " + "\n"
                if(len(post.text) != 0):
                    str += post.text + "\n"
            else: # message via group
                str = "From User #" + post.sender_id + " (via Group #" + post.receiver_id + ") : \n"
                if(len(post.text) != 0):
                    str += post.text + "\n"
            self.in_messages.insert(END, str)

            # displaying image if present
            if(post.img_path != ""):
                img = Image.open(post.img_path)
                img = img.resize((350, 250), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                in_imgs.append(img)
                self.in_messages.image_create(END, image = in_imgs[-1])
                self.in_messages.insert(END, "\n")
            self.in_messages.insert(END, "\n")

        # Disable the text box so that it cannot be altered during execution
        self.in_messages.configure(state = DISABLED)

    # Function to upload an image from the computer using a dialog box
    def upload_image(self):
        global img
        self.curr_text = self.post_messages.get(1.0, END)
        self.curr_text = self.curr_text.strip("\n")
        file_name = filedialog.askopenfilename(title = "Choose a file")
        if(len(file_name) == 0):
            messagebox.showwarning("WARNING", "You have not selected any image")
        else:
            self.curr_img_path = file_name
            img = Image.open(self.curr_img_path)
            img = img.resize((350, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            post_imgs.append(img)
            self.post_messages.insert(END, "\n")
            self.post_messages.image_create(END, image = post_imgs[-1])
            self.post_messages.insert(END, "\n")

    # Function to post a new message
    def upload_message(self):
        text = ""
        if(self.curr_img_path == ""):
            text = self.post_messages.get(1.0, END)
        else:
            text = self.curr_text
        text = text.strip("\n")
        self.post_messages.delete(1.0, END)
        if(text == "" and self.curr_img_path == ""):
            messagebox.showerror("ERROR", "Cannot post an empty message")
            return
        rec = self.var.get()
        type = rec[0]
        ind = rec.find('#')
        rId = rec[ind + 1 : ]
        curr_post = Post(self.curr_user, type, rId, text, self.curr_img_path)

        if(type == "U"):
            obj.user_list[rId].in_posts.append(curr_post)
        else:
            grp = obj.group_list[rId]
            grp.in_posts.append(curr_post)
            for member_id in grp.members:
                obj.user_list[member_id].in_posts.append(curr_post)
        curr_post.console_message()
        
        # The file messages.txt stores all messages in the folowing format : 
        # <sender_id>$<receiver_type>$<receiver_id>$<text>$<img_path>

        # Append the new message to messages.txt
        file = open("messages.txt", "a")
        print(self.curr_user, type, rId, text, self.curr_img_path)
        new_content = self.curr_user + "$" + type + "$" + rId + "$" + text + "$" + self.curr_img_path + "\n"
        file.write(new_content)
        file.close()

        self.curr_text = ""
        self.curr_img_path = ""

        messagebox.showinfo("INFO", "Your message has been successfully posted")


# A window class to represent the main tkinter window
class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        master.geometry("")
        self.rightFrame = RightFrame(master)
        self.leftFrame = LeftFrame(master, self.rightFrame)
        master.wm_title("Social Network")
        self.grid(row = 0, column = 0, sticky = NSEW)

# Creating an object of the SocialNetwork class for all operations and various preprocessing tasks
obj = SocialNetwork()
obj.parse_user_group_list()
obj.parse_messages()

# Basic tkinter initializations
root  = Tk()
app = Window(root)
root.mainloop()

