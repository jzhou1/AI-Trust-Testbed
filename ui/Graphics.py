import tkinter as tk
import time
from PIL import Image, ImageTk
from lib.load_ai import get_positions
import re
import random
import os

def check():
    # checks for keyboard interrupts (ctrl+q)
    root.after(50, self.check)
    Window1.exit()

class Window1:
    def __init__(self, master):
        # master frame
        self.master = master
        self.settings = tk.Frame(self.master)
        self.settings.grid()
        self.s_settings()
    def s_settings(self):
        try:
            if self.setactivate == False:
                root = tk.Tk()
                root.title("Horse Racing")
                root.geometry("500x425")
                root.bind('<Control-q>', quit)
        except AttributeError:
            pass
        # check if root and settings frame is deleted
        # if so recreate them
        try:
            if hasattr(self, 'window'):
                self.window.destroy()
        except AttributeError:
            pass
        # setting title
        tk.Label(self.settings, text = 'Settings', font = (None, 15)).grid(row = 1, column = 1, columnspan = 2, pady = 10)
        # number of trials prompt
        tk.Label(self.settings, text = 'Number of trials: ').grid(row = 2, column = 1, padx = 10, pady = 5, sticky = tk.W)
        # number of trials text box
        self.trials = tk.Entry(self.settings, width = 3)
        self.trials.grid(row = 2, column = 2, sticky = tk.W)
        def toggleslider():
            if self.activate == True:
                self.accuracy.config(state = 'disabled')
                self.activate = False
            else:
                self.accuracy.config(state = 'normal')
                self.activate = True
        # accuracy prompt
        tk.Label(self.settings, text = 'Accuracy: ').grid(row = 3, column = 1, padx = 10, pady = 5, sticky = tk.W)
        # accuracy slider
        self.accuracy = tk.Scale(self.settings, orient = tk.HORIZONTAL, resolution = 10, 
            showvalue = 0, tickinterval = 10, length = 300)
        self.accuracy.grid(row = 3, column = 2, columnspan = 2, sticky = tk.W)
        self.activate = True
        self.checkaccuracy = tk.StringVar(self.settings)
        self.CA = tk.Checkbutton(self.settings, text = "Use accuracy of classifer.", variable = self.checkaccuracy, onvalue = True, offvalue = False, command = toggleslider)
        self.CA.grid(row = 4, column = 2, columnspan = 2, sticky = tk.W)
        # show prompt
        tk.Label(self.settings, text = 'Show: ').grid(row = 5, column = 1, padx = 10, pady = 5,sticky = tk.W)
        tk.Label(self.settings, text = 'Note: default is one horse', font = (None, 10)).grid(row = 7, column = 1, padx = 10, pady = 5, sticky = tk.S + tk.W)
        # show check buttons
        self.showtime = tk.StringVar(self.settings)
        self.showbeyer = tk.StringVar(self.settings)
        self.showorder = tk.StringVar(self.settings)
        self.C1 = tk.Checkbutton(self.settings, text = "Time", variable = self.showtime, onvalue = True, offvalue = False)
        self.C1.grid(row = 5, column = 2, sticky = tk.W)
        self.C2 = tk.Checkbutton(self.settings, text = "Beyer", variable = self.showbeyer, onvalue = True, offvalue = False)
        self.C2.grid(row = 6, column = 2, sticky = tk.W)
        self.C3 = tk.Checkbutton(self.settings, text = "Complete Order", variable = self.showorder, onvalue = True, offvalue = False)
        self.C3.grid(row = 7, column = 2, sticky = tk.W)
        # betting amount prompt
        tk.Label(self.settings, text = 'Betting Amount: ').grid(row = 8, column = 1, padx = 10, pady = 5, sticky = tk.W)
        # betting amount options
        # enabling and disenabling text box for fixed option
        def enableEntry():
            self.betting.configure(state = "normal")
            self.betting.update()
        def disableEntry():
            self.betting.configure(state = "disabled")
            self.betting.update()
        self.betting = tk.Entry(self.settings, width = 3)
        self.betting.grid(row = 9, column = 2, padx = 100, sticky = tk.W)
        self.option_betting = tk.StringVar()
        tk.Radiobutton(self.settings, variable = self.option_betting, text = 'Change', value = 'Change',
            command = disableEntry).grid(row = 8, column = 2, sticky = tk.W)
        tk.Radiobutton(self.settings, variable = self.option_betting, text = 'Fixed', value = 'Fixed', 
            command = enableEntry).grid(row = 9, column = 2, sticky = tk.W)
        # purse size prompt
        tk.Label(self.settings, text = 'Purse Size: ').grid(row = 10, column = 1, padx = 10, pady = 5, sticky = tk.W)
        # purse size entry
        tk.Label(self.settings, text = '$').grid(row = 10, column = 2, sticky = tk.W)
        self.purse = tk.Entry(self.settings, width = 5)
        self.purse.grid(row = 10, column = 2, sticky = tk.W, padx = 15)
        # number of horses prompt
        tk.Label(self.settings, text = 'Number of Horses: ').grid(row = 11, column = 1, padx = 10, pady = 5, sticky = tk.W)
        # number of horses entry
        self.horses = tk.Entry(self.settings, width = 3)
        self.horses.grid(row = 11, column = 2, sticky = tk.W)
        # time limit per race prompt
        tk.Label(self.settings, text = 'Time Limit per Race: ').grid(row = 12, column = 1, padx = 10, pady = 5, sticky = tk.W)
        # time limit per race entry
        self.time = tk.Entry(self.settings, width = 3)
        self.time.grid(row = 12, column = 2, sticky = tk.W)
        tk.Label(self.settings, text = 'minutes').grid(row = 12, column = 2, padx = 30, sticky = tk.W)

        # variable of when settings and root need to be recreated
        self.setactivate = False

        # submit button
        tk.Button(self.settings, text = 'Submit', command = self.instructions).grid(row = 14, 
            column = 1, columnspan = 2, pady = 10)

        # defaults
        self.trials.insert(0, 5)
        self.accuracy.set(50)
        self.CA.deselect()
        self.C1.deselect()
        self.C2.deselect()
        self.C3.deselect()
        self.option_betting.set('Fixed')
        self.betting.insert(0, 2)
        self.purse.insert(0, "{0:.02f}".format(25.00))
        self.horses.insert(0, 3)
        self.time.insert(0, 15)

    def errorcheck(self):
        # check if all elements are given
        elementlist = [self.trials.get(), self.accuracy.get(), self.checkaccuracy.get(), self.showtime.get(), self.showbeyer.get(), self.showorder.get(), self.purse.get(), self.betting.get(), self.horses.get(), self.time.get()]
        for element in elementlist:
            # check if elements are empty
            if not element:
                error = tk.Tk()
                error.title("ERROR")
                error.bind('<Control-q>', quit)
                tk.Label(error, text = "Fill in all settings.").pack(padx = 10, pady = 10)
                tk.Button(error, text = "OK", command = lambda : error.destroy()).pack(padx = 10, pady = 10)
                return False
            # check if purse is a float number
            if element == self.purse.get():
                try:
                    float(element)
                except:
                    error = tk.Tk()
                    error.title("ERROR")
                    error.bind('<Control-q>', quit)
                    tk.Label(error, text = "Please correct format for purse.").pack(padx = 10, pady = 10)
                    tk.Button(error, text = "OK", command = lambda : error.destroy()).pack(padx = 10, pady = 10)
                    return False
            # check if other elements are integers (not letters)
            elif element != self.showtime.get() or element != self.showbeyer.get() or element != self.showorder.get():
                try:
                    int(element)
                except:
                    error = tk.Tk()
                    error.title("ERROR")
                    error.bind('<Control-q>', quit)
                    tk.Label(error, text = "Please enter integers.").pack(padx = 10, pady = 10)
                    tk.Button(error, text = "OK", command = lambda : error.destroy()).pack(padx = 10, pady = 10)
                    return False

    def instructions(self):
        # screen that displays the instructions
        """SAVE DATA"""
        # checking if all entries are filled out
        if not self.errorcheck():
            # saving data from settings
            self.trials1 = int(self.trials.get())
            self.accuracy1 = int(self.accuracy.get())
            self.checkaccuracy1 = self.checkaccuracy.get()
            self.showtime1 = self.showtime.get()
            self.showbeyer1 = self.showbeyer.get()
            self.showorder1 = self.showorder.get()
            self.purse1 = float(self.purse.get())
            self.purse1 = round(self.purse1, 2)
            self.betting_option = self.option_betting.get()
            if not (self.betting.get()):
                self.betting1 = 0
            else:
                self.betting1 = int(self.betting.get())
            self.horses1 = int(self.horses.get())
            self.time1 = int(self.time.get())

            # checking values
            print("Trials: ", self.trials1, 
                "\nAccuracy: ", self.accuracy1,
                "\nCheck Accuracy: ", self.checkaccuracy1,
                "\nTime: ", self.showtime1,
                "\nBeyer: ", self.showbeyer1,
                "\nOrder: ", self.showorder1,
                "\nBetting Style: ", self.betting_option,
                "\nBetting Amount: ", self.betting1,
                "\nPurse: ", self.purse1,
                "\nNumber of Horses: ", self.horses1,
                "\nTime Limit per Race: ", self.time1)

            # clearing screen and making a new instructions window
            self.settings.destroy()
            root.destroy()
            self.setactivate = True
            self.window = tk.Tk()
            self.window.title("Horse Racing")
            self.window.bind('<Control-q>', quit)
            self.window.attributes("-fullscreen", True)
            self.instructions = tk.Frame(self.window)
            self.instructions.grid()
            self.instructions.grid_rowconfigure(0, weight = 1)
            self.instructions.grid_columnconfigure(0, weight = 1)
            # instructions label
            tk.Label(self.instructions, text = 'Welcome!\n Please decide the winner.'
                "\n You will have %s minutes per race. \nThere are %s races." 
                "\n Press start when you are ready."
                % (self.time1, self.trials1), font = (None, 50)).grid(row = 1, column = 1, padx = (500, 450), pady = (300, 100))
            tk.Button(self.instructions, text = 'Start', font = (None, 25), command = self.betting_screen).grid(row = 1, column = 1, sticky = tk.S)

            tk.Button(self.instructions, text = "settings", command = self.s_settings).grid(row = 0, column = 1, pady= 10, sticky = tk.N + tk.E)

    def generateforms(self):
        folder = "split_jpgs"
        # randomly generate race forms
        pattern = re.compile(r'([A-Z]+\d+_\d+)_(\d*|header)?\.jpg')
        race = random.choice(os.listdir(folder))
        m = pattern.match(race)
        string = "convert -append " + os.path.join(folder, m.group(1) + "_header.jpg ")
        filenames = [f for f in os.listdir(folder) if f.endswith(".jpg") and f.startswith(m.group(1)) and not f.endswith("_header.jpg")]
        random.shuffle(filenames)
        for filename in sorted(filenames[:self.horses1]):
            string += os.path.join(folder, filename) + " "
        string += "test.jpg"

        os.system(string)

    def scrolledcanvas(self):
        # generate forms
        self.generateforms()

        # create a canvas for the form
        self.canv = tk.Canvas(self.bet, relief = 'sunken')
        self.canv.config(width = 1500, height = 1125)
        self.canv.config(highlightthickness = 0)

        # create a scroll bar to view the form
        sbarV = tk.Scrollbar(self.bet, orient = 'vertical', command = self.canv.yview)
        sbarV.grid(row = 0, column = 5, rowspan = 5, sticky = tk.N + tk.S + tk.W)
        self.canv.config(yscrollcommand = sbarV.set)

        # load the form onto the canvas and resize it to fit the screen
        self.canv.grid(row = 0, column = 0, rowspan = 5, sticky = tk.N + tk.S + tk.W + tk.E)
        self.im = Image.open("test.jpg")
        self.im = self.im.resize((1500, int((1500/self.im.width)*self.im.height)), Image.ANTIALIAS)
        width, height = self.im.size
        self.canv.config(scrollregion = (0, 0, width, height))
        self.im2 = ImageTk.PhotoImage(self.im)
        self.imgtag = self.canv.create_image(0, 0, anchor = "nw", image = self.im2)

    def countdown(self):
        # count down timer
        mins, secs = divmod(self.t, 60)
        self.timeformat = '{:02d}:{:02d}'.format(mins, secs)
        # when timer reaches 0
        if self.t <= 0:
            self.retrieving_data()
        # updating timer
        else:
            self.timer_label['text'] = self.timeformat
            self.t = self.t - 1
            root.after(1000, self.countdown)

    def betting_screen(self):
        # check if result and instructions screen has been destroyed
        # destroy them if they are created
        try:
            if hasattr(self, 'result'):
                self.result.destroy()
        except AttributeError:
            pass
        # clear instructions screen
        try:
            if hasattr(self, 'instructions'):
                self.instructions.destroy()
        except AttributeError:
            pass
        # betting screen
        self.bet = tk.Frame(self.window)
        self.bet.grid()
        self.bet.grid_rowconfigure(0, weight = 1)
        self.bet.grid_columnconfigure(0, weight = 1)
        # timer
        self.t = self.time1 * 60
        self.timer_label = tk.Label(self.bet, text = "", font = (None, 25), width = 10)
        self.timer_label.grid(row = 0, column = 5, padx = 10, pady = 10, sticky = tk.N + tk.E)
        self.countdown()
        # show forms
        self.scrolledcanvas()
        # show race information on side
        tk.Label(self.bet, text = 'Purse Total: $%s\n\n\nOdds:\nHorse 1: %s\n\n\nSystem recommendation: '
        '%s\n\n\nHorse you want to bet on: \n\n\n' %(format(self.purse1, '.2f'), self.purse1, self.purse1), font = (None, 20), justify = 'left').grid(row = 0, column = 5, padx = 40, pady = 10, sticky = tk.E)
        # submit button
        tk.Button(self.bet, text = 'Submit', command = self.retrieving_data).grid(row = 0, column = 5, padx = 10, pady= 10, sticky = tk.S)

    def retrieving_data(self):
        # check how long the user took to submit
        print(self.timeformat)
        # delete old frame
        self.bet.destroy()
        # variable to keep track if there are more races
        self.next_race = True
        # create a new window for retrieving data
        self.retrieve = tk.Tk()
        self.retrieve.title("Retrieving Data")
        self.retrieve.bind('<Control-q>', quit)
        tk.Label(self.retrieve, text = "Retrieving Data...", font = (None, 50)).pack(padx = 10, pady = 10)
        # delete window after 2 seconds
        self.retrieve.after(2000, lambda: self.results())
        self.retrieve.mainloop()

    def results(self):
        # destroy the retrieving screen and create a new screen for results
        self.retrieve.destroy()
        self.result = tk.Frame(self.window)
        self.result.grid()
        self.result.grid_rowconfigure(0, weight = 1)
        self.result.grid_columnconfigure(0, weight = 1)
        # result labels
        tk.Label(self.result, text = 'Results', font = (None, 35)).grid(row = 1, column = 1, columnspan = 2, pady= (400, 10))
        tk.Label(self.result, text = 'Actual result: ', font = (None, 25)).grid(row = 2, column = 0, padx = (700, 10), pady= 10)
        tk.Label(self.result, text = 'System\'s choice: ', font = (None, 25)).grid(row = 3, column = 0, padx = (700, 10), pady= 10)
        tk.Label(self.result, text = 'Your choice: ', font = (None, 25)).grid(row = 4, column = 0, padx = (700, 10), pady= 10)
        tk.Label(self.result, text = 'Updated Purse: ', font = (None, 25)).grid(row = 5, column = 0, padx = (700, 10), pady= 10)
        # check if there are more races
        if self.trials1 == 1:
            tk.Button(self.result, text = 'Exit', font = (None, 20), command = self.exit).grid(row = 6, column = 1, padx = 10, pady = 10)
        else:
            tk.Button(self.result, text = 'Next Race', font = (None, 20), command = self.races).grid(row = 6, column = 1, padx = 10, pady = 10)

    def races(self):
        # if there are more races, decrement trails and load another race
        if self.trials1 > 0:
            self.betting_screen()
            self.trials1 -= 1

    def exit(self):
        # destroy result screen and make a new screen
        self.result.destroy()
        self.exit = tk.Frame(self.window)
        self.exit.grid()
        self.exit.grid_rowconfigure(0, weight = 1)
        self.exit.grid_columnconfigure(0, weight = 1)
        # instructions for what to do next
        tk.Label(self.exit, text = 'Thank you!\nPlease notify the researcher.', font = (None, 50)).grid(row = 0, column = 1, columnspan = 2, padx = (600, 100), pady = (400, 10))
        tk.Label(self.exit, text = 'Please enter ID number in order to save.').grid(row = 2, column = 1, columnspan = 2, padx = (600, 100))
        self.save = tk.Entry(self.exit, width = 30)
        self.save.grid(row = 3, column = 1, columnspan = 2, padx = (500, 10))
        # save button
        tk.Button(self.exit, text = 'Save', font = (None, 15), command = self.checksave).grid(row = 4, column = 1, columnspan = 2, padx = (550, 50), pady = 10)

    def checksave(self):
        # check the ID number
        # if ID number is -0, don't save
        # otherwise, save
        self.window.destroy()
        if self.save.get() == "-0":
            print("NO SAVE")
            self.exit.destroy()
        if self.save.get() == "":
            pass
        else: 
            print("SAVE")
            self.exit.destroy()

root = tk.Tk()

def run():
    superhorses = get_positions("PRX", "170508", 4)
    root.title("Horse Racing")
    root.geometry("500x425")
    root.bind('<Control-q>', quit)
    app = Window1(root)
    root.mainloop()

if __name__ == "__main__":
    run()