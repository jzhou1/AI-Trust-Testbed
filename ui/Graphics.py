import tkinter as tk
import tkinter.ttk as ttk
import time
import re
import random
import os
import sys
from PIL import Image, ImageTk
from lib.load_ai import get_positions
from pydoc import locate
import pickle

def check():
    # checks every 50 milliseconds for keyboard interrupts (ctrl+q)
    # quits if ctrl+q is pressed
    root.after(50, self.check)

class HoverInfo(tk.Menu):
    #creates a information box when hovering over a widget

    def __init__(self, parent, text):
        tk.Menu.__init__(self, parent, tearoff=0)
        if not isinstance(text, str):
            raise TypeError('Trying to initialise a Hover Menu with a non'
                            ' string type: ' + text.__class__.__name__)
        toktext = re.split('\n', text)
        for t in toktext:
            self.add_command(label=t, font=(None,10))
        self._displayed = False
        self.master.bind("<Enter>",self.Display)
        self.master.bind("<Leave>",self.Remove)

    # shows information box
    def Display(self, event):
        if not self._displayed:
            self._displayed = True
            self.post(event.x_root, event.y_root)

    # removes information box
    def Remove(self, event):
        if self._displayed:
            self._displayed = False
            self.unpost()

class MainWindow:
    
    def __init__(self, master):
        # setting up first windows (welcome and settings)
        self.master = master

        # go to settings screen
        self.s_welcome()

    class Settings:
        def save(self, filename):
            pickle.dump({i: getattr(self,i) for i in self.__dict__ \
                if not callable(getattr(self, i)) and not i.startswith('__')},\
                        open(os.path.join(self.path,filename + '_s.p'), 'wb'))

        def load(self, filename):
            if filename == 'None':
                self.name = 'None'
                MainWindow.load_defaults
            else: 
                temp = pickle.load(open(os.path.join(self.path,filename+'_s.p'), 'rb'))
                print(temp)
                for i in temp.keys():
                    setattr(self, i, temp[i]) 

    def load_settings(self, *event):
        name = self.defaultmenu.get()
        self.revert.config(state='disabled')
        self.apply.config(state='disabled')
        if name == 'None':
            self.Settings.name = name
        elif name == 'Edit Settings':
            self.edit_settings()
        elif os.path.isfile(os.path.join(self.Settings.path, 
                            name + '_s.p')):
            self.Settings.name = name
            self.Settings.load(self.Settings,self.defaultmenu.get())
            self.set_all_defaults()
            self.Settings.name = self.defaultmenu.get()

    def save_settings(self):
        # saving data from settings
        #if not self.errorcheck():
        print(self.Settings.name)
        self.Settings.system_name = self.system_name.get()
        self.Settings.trials = int(self.trials.get())
        self.Settings.accuracy = int(self.accuracy.get())
        self.Settings.checkaccuracy = int(self.checkaccuracy.get())
        self.Settings.displaytime = int(self.displaytime.get())
        self.Settings.displaybeyer = int(self.displaybeyer.get())
        self.Settings.displayorder = int(self.displayorder.get())
        self.Settings.purse = round(float(self.purse.get()), 2)
        self.Settings.betting_option = self.option_betting.get()
        self.Settings.betting_amount = int(self.betting.get())
        self.Settings.num_of_horses = int(self.horses.get())
        self.Settings.time_limit = int(self.time.get())
        self.Settings.option_suggestion = self.option_suggestion.get()
        if self.Settings.name != 'None':
            self.Settings.save(self.Settings, self.Settings.name)
        self.revert.config(state='disabled')
        self.apply.config(state='disabled')

    def check_settings(self):
        # check if settings have changed
        print(self.Settings.name)
        return (self.Settings.trials == int(self.trials.get()) \
           and self.Settings.system_name == self.system_name.get() \
           and self.Settings.betting_option == self.option_betting.get() \
           and (self.Settings.betting_option == '0' \
            or self.Settings.betting_amount == int(self.betting.get())) \
           and self.Settings.purse == float(self.purse.get()) \
           and self.Settings.time_limit == int(self.time.get()) \
           and self.Settings.num_of_horses == int(self.horses.get()) \
           and self.Settings.checkaccuracy == int(self.checkaccuracy.get()) \
           and (self.Settings.checkaccuracy == '1' \
            or self.Settings.accuracy == int(self.accuracy.get())) \
           and self.Settings.displaytime == int(self.displaytime.get()) \
           and self.Settings.displaybeyer == int(self.displaybeyer.get()) \
           and self.Settings.displayorder == int(self.displayorder.get()) \
           and self.Settings.option_suggestion == self.option_suggestion.get())

    def load_defaults(self):
        self.Settings.system_name = 'AIde'
        self.Settings.trials = 3
        self.Settings.accuracy = 50
        self.Settings.checkaccuracy = 0
        self.Settings.displaytime = 0
        self.Settings.displaybeyer = 0
        self.Settings.displayorder = 0
        self.Settings.purse = 25
        self.Settings.purse = round(self.Settings.purse, 2)
        self.Settings.betting_option = 'Fixed'
        self.Settings.betting_amount = 2
        self.Settings.num_of_horses = 3
        self.Settings.time_limit = 15
        self.Settings.option_suggestion = 'After'

    def edit_settings(self):
        #make pop up window to enter name of settings
        def remove():
            f = lb.curselection()
            filen= lb.get(int(f[0]))
            os.remove(os.path.join(self.Settings.path, filen)+'_s.p')
            lb.delete(f[0])
            if self.Settings.name == filen:
                if lb.size() > 0:
                    self.Settings.name = lb.get(0)
                else:
                    self.Settings.name = 'None'

        def close():
            self.Settings.load(self.Settings, self.Settings.name)
            self.defaultmenu.set(self.Settings.name)       
            self.defaultmenu.set(self.Settings.name)
            self.default_select.destroy()
            defaults = [f.replace('_s.p','') for f in os.listdir(self.Settings.path) \
                if f.endswith('_s.p')]+['None', 'Edit Settings']
            self.default_select = tk.OptionMenu(self.settings, self.defaultmenu, 
                                          *defaults, command=self.load_settings)
            self.default_select.grid(row=0, column=2, pady=10, sticky = tk.W)
            save_window.destroy()

        def save_file():
            n = name.get()
            if n == '':
                self.error_window("Enter a file name")
            elif n + '_s.p' in os.listdir(self.Settings.path):
                self.error_window("File already exixts")
            else:
                name.delete(0,'end')
                name.grid_remove()
                lb.insert('end', n)
                lb.config(height=lb.size()+1)
                self.Settings.name = n
                self.load_defaults()
                self.Settings.save(self.Settings, self.Settings.name)
                done_button.grid_remove()
                add_button.grid()
                remove_button.grid()
                cancel_button.grid()
                

        def add():
            name.grid(row=1,column=1,sticky=tk.S)
            add_button.grid_remove()
            cancel_button.grid_remove()
            remove_button.grid_remove()
            done_button.grid(row=2,column=1,padx=(0,20),sticky=tk.E)


        save_window = tk.Tk()
        save_window.wm_attributes("-topmost", 1)
        save_window.geometry('315x290')
        save_window.grid()
        save_window.title('Edit Settings')
        save_window.bind('<Control-q>', sys.exit)
        lb = tk.Listbox(save_window,width=30)
        lb.grid(row=1,column=1,sticky=tk.N,padx=20)
        tk.Label(save_window,text='Files:').grid(
                                row=0,column=1,sticky=tk.W,padx=20,pady=(10,0))
        for f in [f.replace('_s.p','') for f in os.listdir(self.Settings.path) \
                                                if f.endswith('_s.p')]:
            print(f)
            lb.insert('end',f)
        lb.config(height=lb.size()+1)
        cancel_button = tk.Button(save_window, text='Done',command=close)
        cancel_button.grid(row=2,column=1,padx=(1,20),sticky=tk.E)
        add_button = tk.Button(save_window, text='Add',command=add)
        add_button.grid(row=2,column=1,padx=(20,1),sticky=tk.W)
        remove_button = tk.Button(save_window, text='Remove',command=remove)
        remove_button.grid(row=2,column=1,padx=1)
        done_button = tk.Button(save_window, text='Enter',command=save_file)
        name = tk.Entry(save_window,width=30)

    def update_settings(self):
        self.Settings.load(self.Settings,self.Settings.name)
        self.set_all_defaults()

    def enable_checking(self):
         self.trials.trace_id = self.trials.trace('w',self.toggleapplyrevert)
         self.betting.trace_id = self.betting.trace('w',self.toggleapplyrevert)
         self.purse.trace_id = self.purse.trace('w',self.toggleapplyrevert)
         self.time.trace_id = self.time.trace('w',self.toggleapplyrevert)
         self.horses.trace_id = self.horses.trace('w',self.toggleapplyrevert)
         self.checkaccuracy.trace_id = self.checkaccuracy.trace('w',self.toggleapplyrevert)
         self.displaytime.trace_id = self.displaytime.trace('w',self.toggleapplyrevert)
         self.displaybeyer.trace_id = self.displaybeyer.trace('w',self.toggleapplyrevert)
         self.displayorder.trace_id = self.displayorder.trace('w',self.toggleapplyrevert)
         self.option_betting.trace_id = self.option_betting.trace('w',self.toggleapplyrevert)
         self.option_suggestion.trace_id = self.option_suggestion.trace('w',self.toggleapplyrevert)
         self.system_name.trace_id = self.system_name.trace('w',self.toggleapplyrevert)

    def disable_checking(self):
        self.trials.trace_vdelete("w", self.trials.trace_id)
        self.betting.trace_vdelete('w', self.betting.trace_id)
        self.purse.trace_vdelete('w', self.purse.trace_id)
        self.time.trace_vdelete('w', self.time.trace_id)
        self.horses.trace_vdelete('w', self.horses.trace_id)
        self.checkaccuracy.trace_vdelete('w', self.checkaccuracy.trace_id)
        self.displayorder.trace_vdelete('w', self.displayorder.trace_id)
        self.displaytime.trace_vdelete('w', self.displaytime.trace_id)
        self.displaybeyer.trace_vdelete('w', self.displaybeyer.trace_id)
        self.option_betting.trace_vdelete('w', self.option_betting.trace_id)
        self.option_suggestion.trace_vdelete('w', self.option_suggestion.trace_id)
        self.system_name.trace_vdelete('w', self.system_name.trace_id)

    def set_all_defaults(self):
        print('setting defaults')
        self.disable_checking()
        self.system_name.set(self.Settings.system_name)
        # trials entry box
        self.trials.set(self.Settings.trials)
        # accuracy slider
        self.accuracy.set(self.Settings.accuracy)

        # use accuracy of classifer
        if not self.Settings.checkaccuracy:
            self.CA.deselect()
        else:
            self.CA.select()

        # show time
        if not self.Settings.displaytime:
            self.C1.deselect()
        else:
            self.C1.select()

        # show beyer
        if not self.Settings.displaybeyer:
            self.C2.deselect()
        else:
            self.C2.select()

        # show order of horses
        if not self.Settings.displayorder:
            self.C3.deselect()
        else:
            self.C3.select()

        self.accuracy.set(self.Settings.accuracy)
        # betting options
        self.option_betting.set(self.Settings.betting_option)
        
        # fixed bet entry box
        self.betting.set(self.Settings.betting_amount)

        # purse size
        self.purse.set("{0:.02f}".format(self.Settings.purse))

        # number of horses
        self.horses.set(self.Settings.num_of_horses)

        # time per race
        self.time.set(self.Settings.time_limit)
        if self.Settings.betting_option == 'Fixed':
            self.betting_box.configure(state='normal')
            self.betting_box.update()
        else:
            self.betting_box.configure(state='disabled')
            self.betting_box.update()

        if self.checkaccuracy.get() == '1':
            self.accuracy.config(state='disabled')
            
            #grey out the bar
            self.accuracy.config(foreground='gainsboro')
        else:
            self.accuracy.config(state='normal')
            
            #make the bar normal colored
            self.accuracy.config(foreground='black')
        self.option_suggestion.set(self.Settings.option_suggestion)
        self.revert.config(state='disabled')
        self.apply.config(state='disabled')
        self.enable_checking()

    def toggleapplyrevert(self,*a):
        if (self.errorcheck() is None and self.check_settings()) or self.Settings.name == 'None':
            self.revert.config(state='disabled')
            self.apply.config(state='disabled')
        else:
            self.revert.config(state='normal')
            if self.errorcheck() is None:
                self.apply.config(state='normal')
            else:
                self.apply.config(state='disabled')

    def s_welcome(self):
        if hasattr(self, 'settings'):
            self.settings.destroy()

        global screen_width
        global screen_height

        self.master.geometry("{}x{}".format(screen_width, screen_height))

        self.welcome = tk.Frame(self.master)
        self.welcome.grid()
        for i in range(2):
            self.welcome.grid_rowconfigure(
                                    i, minsize=int(screen_height/2))
            self.welcome.grid_columnconfigure(
                                    i, minsize=int(screen_width/2))
        tk.Label(self.welcome, text='Welcome!', font=(None,40))\
                .grid(row=0, column=0, columnspan=2, padx=20, pady=50, 
                      sticky=tk.W + tk.E + tk.S)
        tk.Button(self.welcome, text='Settings', font=(None,30), 
                  command=self.s_settings)\
                 .grid(row=1, column=0, padx=30, pady=10, sticky=tk.N + tk.E)
        tk.Button(self.welcome, text='Experiment', font=(None,30), 
                  command=self.instructions)\
                 .grid(row=1, column=1, padx=30, pady=10, sticky=tk.N + tk.W)

    def load_instructions(self):
        error = self.errorcheck()
        if error != None:
            self.error_window(error)
        elif self.Settings.name == 'None':
            self.save_settings()
            self.s_welcome()
        elif not self.check_settings():
            self.error_window("Apply or revert your changes before continuing")
        else:
            self.s_welcome()

    def s_settings(self):
        if hasattr(self, 'welcome'):
            self.welcome.destroy()

        self.Settings.path = os.path.join('ui','settings')
        self.Settings.name = 'None'
        self.load_defaults()

        # create settings window
        self.master.geometry("635x700")
        self.settings = tk.Frame(self.master)
        self.settings.grid()
        self.settings.grid_columnconfigure(0, minsize=50)
        self.settings.grid_columnconfigure(5, minsize=50)

        tk.Label(self.settings).grid(rowspan=22, columnspan=3, padx=20, pady=20,
                                     sticky=tk.N+tk.S+tk.W+tk.E)

        # drop-down of default settings
        select_settings = tk.Label(self.settings, text="Select settings: ")
        select_settings.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        HoverInfo(select_settings, "Select settings from previous stored saves")
        defaults = [f.replace('_s.p', '') for f in os.listdir(self.Settings.path)\
                    if f.endswith('_s.p')]
        defaults.append('None')
        defaults.append('Edit Settings')
        self.defaultmenu = tk.StringVar(self.settings)
       
        self.defaultmenu.set(self.Settings.name)
        self.default_select = tk.OptionMenu(self.settings, self.defaultmenu, 
                                          *defaults, command=self.load_settings)
        self.default_select.grid(row=0, column=2, pady=10, sticky = tk.W)

        ttk.Separator(self.settings).grid(row=1, columnspan=6, 
                                          sticky=tk.W + tk.E, pady=10, padx=10)

        # name of system prompt
        sys_name = tk.Label(self.settings, text='System name: ')
        sys_name.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        HoverInfo(sys_name, "Name of system")

        # name of system entry box
        self.system_name = tk.StringVar()
        system_name = tk.Entry(self.settings, text=self.system_name, width=20)
        system_name.grid(row=2, column=2, sticky=tk.W)

        ttk.Separator(self.settings).grid(row=3, columnspan=6, 
                                          sticky=tk.W + tk.E, pady=10, padx=10)

        # number of trials prompt
        num_trials = tk.Label(self.settings, text='Number of trials: ')
        num_trials.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        HoverInfo(num_trials, "Number of races a user will bet on")

        # number of trials text box
        self.trials = tk.StringVar()
        trials = tk.Entry(self.settings, textvariable=self.trials, width=3)
        
        trials.grid(row=4, column=2, sticky=tk.W)

        ttk.Separator(self.settings).grid(row=3, columnspan=6, sticky=tk.W + 
                                          tk.E, pady=10, padx=10)

        ttk.Separator(self.settings).grid(row=5, columnspan=6, 
                                          sticky=tk.W + tk.E, pady=10, padx=10)

        # disabling and enabling accuracy bar
        def toggleslider():
            self.toggleapplyrevert()
            if self.checkaccuracy.get() == '1':
                self.accuracy.config(state='disabled')
                
                #grey out the bar
                self.accuracy.config(foreground='gainsboro')
            else:
                self.accuracy.config(state='normal')
                
                #make the bar normal colored
                self.accuracy.config(foreground='black')

        # check button for using accuracy of classifer
        # if checked, accuracy bar is disabled
        self.checkaccuracy = tk.StringVar(self.settings)
        self.CA = tk.Checkbutton(self.settings, 
                                 text="Use accuracy of classifer.", 
                                 variable=self.checkaccuracy, onvalue=True, 
                                 offvalue=False, command=toggleslider)
        self.CA.grid(row=7, column=2, columnspan=2, sticky=tk.W)

        # accuracy prompt
        accuracy = tk.Label(self.settings, text='Accuracy: ')
        accuracy.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)
        HoverInfo(accuracy, "Override classifer's accuracy - percentage \nof"\
                  " when the system guesses correctly")

        # accuracy slider
        self.accuracy = tk.Scale(self.settings, orient=tk.HORIZONTAL, command=self.toggleapplyrevert,
                                 resolution=10, showvalue=0, tickinterval=10, 
                                 length=300)
        self.accuracy.grid(row=6, column=2, columnspan=2, padx=10, sticky=tk.W)

        ttk.Separator(self.settings).grid(row=8, columnspan=6, 
                                          sticky=tk.W + tk.E, pady=10, padx=10)

        # what data to show prompt
        display = tk.Label(self.settings, text='Display: ')
        display.grid(row=9, column=1, padx=10, pady=5,sticky=tk.W)
        HoverInfo(display, "Predicted features to show on betting screen")
        tk.Label(self.settings, text='Note: default is one horse', 
                 font=(None,10))\
                .grid(row=11, column=1, padx=10, pady=5, sticky=tk.S + tk.W)

        # show check buttons - time, beyer, and show order
        self.displaytime = tk.StringVar(self.settings)
        self.displaybeyer = tk.StringVar(self.settings)
        self.displayorder = tk.StringVar(self.settings)
        
        #create the time button
        self.C1 = tk.Checkbutton(self.settings, text='Time', 
                                 variable=self.displaytime, onvalue=True, 
                                 offvalue=False)
        self.C1.grid(row=9, column=2, sticky=tk.W)

        #create the Beyer figure button
        self.C2 = tk.Checkbutton(self.settings, text='Beyer', 
                                 variable=self.displaybeyer, onvalue=True, 
                                 offvalue=False)
        self.C2.grid(row=10, column=2, sticky=tk.W)
        
        #create the order button
        self.C3 = tk.Checkbutton(self.settings, text="Complete Order",
                                 variable=self.displayorder, onvalue=True, 
                                 offvalue=False)
        self.C3.grid(row=11, column=2, columnspan=2, sticky=tk.W)

        ttk.Separator(self.settings).grid(row=12, columnspan=6, 
                                          sticky=tk.W + tk.E, pady=10, padx=10)

        # suggestion prompt
        suggestion = tk.Label(self.settings, text='AIde\'s suggestion: ')
        suggestion.grid(row=13, column=1, padx=10, pady=5, sticky=tk.W)
        HoverInfo(suggestion, "When AIde's suggestion \nis shown to user")
        self.option_suggestion=tk.StringVar()

        # change betting option
        tk.Radiobutton(self.settings, variable=self.option_suggestion, 
                       text='Bet screen', value='Bet')\
                      .grid(row=13, column=2, sticky=tk.W)
        
        # fixed dollar amount betting option
        tk.Radiobutton(self.settings, variable=self.option_suggestion,
                       text='After bet screen', value='After')\
                      .grid(row=13, column=3, sticky=tk.W)

        ttk.Separator(self.settings).grid(row=14, columnspan=6, 
                                          sticky=tk.W + tk.E, pady=10, padx=10)

        # betting amount prompt
        betting = tk.Label(self.settings, text='Betting Amount: ')
        betting.grid(row=15, column=1, padx=10, pady=5, sticky=tk.W)
        HoverInfo(betting, "Amount a user can bet each race")
   
        # betting amount options
        # enabling and disenabling text box for fixed option
        def enableEntry():
            self.betting_box.configure(state='normal')
            self.betting_box.update()
        def disableEntry():
            self.betting_box.configure(state='disabled')
            self.betting_box.update()

        tk.Label(self.settings, text='$').grid(row=15, column=3, padx=(55,0))
        self.betting = tk.StringVar()
        self.betting_box = tk.Entry(self.settings, text=self.betting, width=3)
        self.betting_box.grid(row=15, column=3, padx=(0,10), sticky=tk.E)
        self.option_betting=tk.StringVar()

        # variable betting option
        tk.Radiobutton(self.settings, variable=self.option_betting, 
                       text='Variable', value='Variable', command=disableEntry)\
                      .grid(row=15, column=2, sticky=tk.W)
        
        # fixed dollar amount betting option
        tk.Radiobutton(self.settings, variable=self.option_betting,
                       text='Fixed', value='Fixed', command=enableEntry)\
                      .grid(row=15, column=3, sticky=tk.W)

        ttk.Separator(self.settings).grid(row=16, columnspan=6, 
                                          sticky=tk.W + tk.E, pady=10, padx=10)

        # purse size prompt
        purse = tk.Label(self.settings, text='Initial Purse Size: ')
        purse.grid(row=17, column=1, padx=10, pady=5, sticky=tk.W)
        HoverInfo(purse, "Starting purse size for user")

        # purse size entry box
        tk.Label(self.settings, text='$').grid(row=17, column=2, sticky=tk.W)
        self.purse = tk.StringVar()
        purse_box = tk.Entry(self.settings, text=self.purse, width=5)
        purse_box.grid(row=17, column=2, sticky=tk.W, padx=15)


        ttk.Separator(self.settings).grid(row=18, columnspan=6, 
                                          sticky=tk.W + tk.E, pady=10, padx=10)

        # number of horses prompt
        num_horses = tk.Label(self.settings, text='Number of Horses: ')
        num_horses.grid(row=19, column=1, padx=10, pady=5, sticky=tk.W)
        HoverInfo(num_horses, "Number of horses per race")

        # number of horses entry box
        self.horses = tk.StringVar() 
        horse_box = tk.Entry(self.settings, text=self.horses, width=3)
        horse_box.grid(row=19, column=2, sticky=tk.W)
        tk.Label(self.settings, text='horses').grid(row=19, column=2,

                 padx=40, sticky=tk.W)

        ttk.Separator(self.settings)\
           .grid(row=20, columnspan=6, sticky=tk.W + tk.E, pady=10, padx=10)

        # time limit per race prompt
        time_limit = tk.Label(self.settings, text='Time Limit per Race: ')
        time_limit.grid(row=21, column=1, padx=10, pady=5, sticky=tk.W)
        HoverInfo(time_limit, "Time limit for each race")

        # time limit per race entry box
        self.time = tk.StringVar()
        time = tk.Entry(self.settings, text=self.time, width=3)
        time.grid(row=21, column=2, sticky=tk.W)
        tk.Label(self.settings, text='minutes').grid(row=21, column=2, 
                padx=40, sticky=tk.W)

        ttk.Separator(self.settings)\
           .grid(row=22, columnspan=6, sticky=tk.W + tk.E, pady=10, padx=10)

        # submit button
        self.revert = tk.Button(self.settings, text='Revert', 
                                command=self.update_settings)
        self.revert.grid(row=23, column=1, padx=10, pady=10, sticky=tk.E)

        self.apply = tk.Button(self.settings, text='Apply', 
                               command=self.save_settings)
        self.apply.grid(row=23, column=2, padx=10, pady=10, sticky=tk.E)

        tk.Button(self.settings, text='Continue', command=self.load_instructions).grid \
                 (row=23, column=3, padx=10, pady=10, sticky=tk.E)

        # set all of the defaults
        self.enable_checking()
        self.set_all_defaults()

    def error_window(self, message):
        error = tk.Tk()
        error.title('ERROR')
        error.bind('<Control-q>', quit)
        tk.Label(error, text = message, 
            font = (None, 20)).pack(padx = 10, pady = 10)
        tk.Button(error, text='OK', command=lambda : 
            error.destroy()).pack(padx=10, pady=10)


    def errorcheck(self):
        # checks to make sure the settings were correct
        elementlist = [(self.system_name.get(),'system name',str),
                       (self.trials.get(),'number of trials',int,1,50), 
                       (self.purse.get(),'purse',float,2), 
                       (self.horses.get(),'number of horses',int,2), 
                       (self.time.get(),'time limit',int,1,60)]
        if self.checkaccuracy.get() == '0':
            elementlist.append((self.accuracy.get(),'accuracy of the classifier',int,0,100))
        if self.option_betting.get() == 'Fixed':
            elementlist.append((self.betting.get(),'betting amount',int,2,self.purse.get()))

        for element in elementlist:
            print(element)
            e = element[0]
            name = element[1]
            t = element[2]
            # check if any element is empty
            if e != 0 and not e:
                #display the error essage
                return "Enter a value for {}".format(name)
            else:
                # make sure elements are the right type and value.
                try:
                    e = t(e)
                    print(e)
                    if len(element) > 3 and e < element[3]:
                        return 'The ' + name + ' must be greater than or equal to ' + str(element[3])
                    elif len(element) > 4 and float(e) > float(element[4]):
                        return 'The ' + name + ' must be less than or equal to ' + str(element[4])
                except:
                    return 'The ' + name + ' must be '+ str(t)
        return None

    def instructions(self):
        # screen that displays the instructions
        # clearing screen and making a new instructions window
        if hasattr(self, 'settings'):
            self.settings.destroy()
        else:
            self.Settings.path = os.path.join('ui','settings')
            self.load_defaults()

        self.welcome.destroy()

        # configure instructions frame
        self.instructions = tk.Frame(self.master)
        self.instructions.grid()
        for i in range(3):
            self.instructions.grid_rowconfigure(
                                    i, minsize=int(screen_height/3))
            self.instructions.grid_columnconfigure(
                                    i, minsize=int(screen_width/3))

        # instructions label
        betValue = ("fixed at ${:.2f}".format(self.Settings.betting_amount)
                    if self.Settings.betting_option == "Fixed" else
                    "up to you")
        welcomeText = "As a reminder, your bets are {}." + \
                      "\nYour task is to pick, as best you can, the " + \
                      "winner of the race.\nYou will have up to {} " + \
                      "minute(s) to look at all the data and make your " + \
                      "choice.\nPress start when you are ready."

        tk.Label(self.instructions, 
                 text=welcomeText.format(betValue, self.Settings.time_limit),
                 font=(None,font_body))\
                .grid(row=1, column=0, columnspan=3)

        tk.Button(self.instructions, text='Start', 
                  font=(None,font_body-5), command=self.betting_screen)\
                 .grid(row=1, column=0, columnspan=3, sticky=tk.S)

    def generateforms(self):
        # creates forms with random horses
        # folder where forms are found
        folder = "data/split_jpgs"
        # randomly generate race forms
        pattern = re.compile(r'([A-Z]+)(\d+)_(\d+)_(\d*|header)?\.jpg')

        #race = random.choice(os.listdir(folder))
        race = "ARP170618_1_1.jpg"
        m = pattern.match(race)

        # get filepaths and make sure they exist before continuing
        sep = "_" if len(m.group(1)) < 3 else ""
        p = "data/" + m.group(1) + "/" + m.group(2) + "/" + m.group(1) + sep + \
            m.group(2) + "_SF.CSV"
        ltp = "data/" + m.group(1) + "/" + m.group(2) + "/" + \
              m.group(1) + sep + m.group(2) + "_" + m.group(3) + "_LT.CSV"
        lbp = "data/" + m.group(1) + "/" + m.group(2) + "/" + \
              m.group(1) + sep + m.group(2) + "_" + m.group(3) + "_LB.CSV"

        print("Looking for:",p)
        print("           :",ltp)
        print("           :",lbp)
        print("           :",folder+"/ARP170618_3_header.jpg")

        # find a race, and ensure that the files necessary exist
        while not (os.path.isfile(p) and os.path.isfile(ltp) 
                   and os.path.isfile(lbp)):
            # get new race
            print("File doesn't exist! Trying again...")
            race = random.choice(os.listdir(folder))
            m = pattern.match(race)

            # get filepaths, and make sure they exist before continuing
            sep = "_" if len(m.group(1)) < 3 else ""
            p = "data/" + m.group(1) + "/" + m.group(2) + "/" + m.group(1) + \
                sep + m.group(2) + "_SF.CSV"
            ltp = "data/" + m.group(1) + "/" + m.group(2) + "/" + \
                  m.group(1) + sep + m.group(2) + "_" + m.group(3) + "_LT.CSV"
            lbp = "data/" + m.group(1) + "/" + m.group(2) + "/" + \
                  m.group(1) + sep + m.group(2) + "_" + m.group(3) + "_LB.CSV"

        beginning = time.time()

        # pick random horses and make a form
        convert_string = "convert -append " + os.path.join(folder, m.group(1) \
                         + m.group(2) + '_' + m.group(3) + "_header.jpg ")
            
        # generate a list of possible filenames
        filenames = [f for f in os.listdir(folder) 
                        if f.endswith(".jpg") and \
                           f.startswith(m.group(1)+m.group(2)+'_'+m.group(3)) \
                           and not f.endswith("_header.jpg")]

        # shuffle the list
        random.shuffle(filenames)
        nums = []
        # 
        for filename in sorted(filenames[:self.Settings.num_of_horses]):
            convert_string += os.path.join(folder, filename) + " "
            m = pattern.match(filename)
            nums += m.group(4)

        convert_string += "test.jpg"
        # TODO: why does this convert the jpgs while running? 
        #       conversion should be done beforehand for limited cases
        os.system(convert_string)

        # find horses in csv files
        self.superhorses = get_positions(m.group(1), m.group(2), m.group(3))
        self.horses_racing = []
        for horse in self.superhorses:
            if (horse['B_ProgNum'] in nums):
                self.horses_racing.append(horse)

        # find actual winning horse
        self.horses_racing.sort(key=lambda x:x['L_Rank'])
        if not self.Settings.displayorder:
            self.horse_win = self.horses_racing[0]['B_Horse']
        else:
            self.horse_win = self.horses_racing[0]['B_Horse']
            self.horse_winl = ""
            for horse in self.horses_racing[:-1]:
                self.horse_winl += (horse['B_Horse'] + "\n")
            self.horse_winl += self.horses_racing[-1]['B_Horse']

        # if show time, find times
        if self.Settings.displaytime:
            self.horse_time = ""
            if not self.Settings.displayorder:
                self.horse_time += self.horses_racing[0]['P_Time']
            else:
                for horse in self.horses_racing[:-1]:
                    self.horse_time += (horse['L_Time'] + "\n")
                self.horse_time += self.horses_racing[-1]['P_Time']

        # if show beyer, find beyer figures
        if self.Settings.displaybeyer:
            self.horse_beyer = ""
            if not self.Settings.displayorder:
                self.horse_beyer += str(self.horses_racing[0]['P_BSF'])
            else:
                for horse in self.horses_racing[:-1]:
                    self.horse_beyer += (str(horse['P_BSF']) + "\n")
                self.horse_beyer += str(self.horses_racing[-1]['P_BSF'])

        # find predicted winning horse
        if self.Settings.checkaccuracy:
            self.horses_racing.sort(key=lambda x:x['P_Time'])
            self.horse_pwin = self.horses_racing[0]['B_Horse']
        elif self.Settings.accuracy == 100:
            self.horse_pwin = self.horse_win
        else:
            horse_list = []
            probablity= int((100-self.Settings.accuracy)/(len(self.horses_racing)-1))
            for horse in self.horses_racing:
                if horse['B_Horse'] == self.horse_win:
                    horse_list += ([self.horse_win]*self.Settings.accuracy)
                else:
                    horse_list += ([horse['B_Horse']]*probablity)
            self.horse_pwin = random.choice(horse_list)

        # find odds and winnings for horses
        self.horses_odds = ""
        self.horses_winnings = ""
        self.horses_racing.sort(key=lambda x:x['B_ProgNum'])
        for horse in self.horses_racing:
            odds = horse['B_MLOdds'].split('-')
            if horse == self.horses_racing[-1]:
                self.horses_odds += (horse['B_Horse'] + " : " + horse['B_MLOdds'])
                self.horses_winnings += (str((self.Settings.betting_amount * float(odds[0])) / 
                                    float(odds[1])))
            else:
                self.horses_odds += (horse['B_Horse'] + " : " + 
                                 horse['B_MLOdds'] + "\n ")
                self.horses_winnings += (str((self.Settings.betting_amount * float(odds[0])) / 
                                    float(odds[1])) + "\n $")

        end = time.time()

    def scrolledcanvas(self):
        # generate forms
        self.generateforms()

        # create a canvas for the form
        self.canv = tk.Canvas(self.bet, relief='sunken')
        self.canv.config(width=int(screen_width*(5/7)), height=screen_height)
        self.canv.config(highlightthickness=0)

        # create a scroll bar to view the form
        sbarV = tk.Scrollbar(self.bet, orient='vertical', 
                             command=self.canv.yview)
        sbarV.grid(row=0, column=0, rowspan=10, sticky=tk.N + tk.S + tk.E)
        self.canv.config(yscrollcommand=sbarV.set)

        # load the form onto the canvas and resize it to fit the screen
        self.canv.grid(row=0, column=0, rowspan=10, 
                       sticky=tk.N + tk.S + tk.W + tk.E)
        self.im = Image.open("test.jpg")
        self.im = self.im.resize((int(screen_width*(5/7)), 
                                  int((int(screen_width*(5/7))/self.im.width)*self.im.height)),
                                 Image.ANTIALIAS)
        width, height = self.im.size
        self.canv.config(scrollregion=(0, 0, width, height))
        self.im2 = ImageTk.PhotoImage(self.im)
        self.imgtag = self.canv.create_image(0, 0, anchor='nw', image=self.im2)

    def countdown(self):
        # countdown timer
        self.t -= 1
        mins, secs = divmod(self.t, 60)
        self.timer_label['text'] = '{:02d}:{:02d}'.format(mins, secs)
        if hasattr(self, 'bet'):
            self.bet.after(1000, self.countdown)
        else:
            self.s_suggest.after(1000, self.countdown)
        if self.t == -1:
            if self.horsemenu.get() == "Select horse":
                error = tk.Tk()
                error.title("ERROR")
                error.bind('<Control-q>', sys.exit)
                tk.Label(error, text="No horse was selected.\n Betting amount is"
                         " still deducted", font=(None,20))\
                        .pack(padx=10, pady=10)
                tk.Button(error, text="OK", command=lambda: error.destroy())\
                         .pack(padx=10, pady=10)
            self.retrieving_data()

    def betting_screen(self):
        # check if result and instructions screen has been destroyed
        # destroy them if they are created to show new race
        if hasattr(self, 'result'):
            self.result.destroy()

        # clear instructions screen
        if hasattr(self, 'instructions'):
            self.instructions.destroy()

        # betting screen
        self.bet = tk.Frame(self.master)
        self.bet.grid()
        self.bet.grid_columnconfigure(0, minsize=(screen_width*(5/7)))
        self.bet.grid_columnconfigure(1, minsize=(screen_width*(1/7)))
        self.bet.grid_columnconfigure(2, minsize=(screen_width*(1/7)))

        # set up for countdown timer
        self.t = self.Settings.time_limit * 60
        self.timer_label = tk.Label(self.bet, textvariable="", 
                                    font=(None,font_body), justify='right')
        self.timer_label.grid(row=0, column=2, padx=15, pady=10, 
                              sticky=tk.N + tk.E)
        self.countdown()

        # show forms
        self.scrolledcanvas()

        # drop down menu of horses
        self.horse_names = []
        for horse in self.horses_racing:
            self.horse_names.append(horse['B_Horse'])

        self.horsemenu = tk.StringVar(self.bet)
        self.horsemenu.set("Select horse")
        self.horse_select = tk.OptionMenu(self.bet, self.horsemenu, 
                                          *self.horse_names)
        self.horse_select.config(font=(None,font_body))

        # show race information on side
        tk.Label(self.bet, font=(None,font_body),
                 text="Purse Total: ${:.2f}".format(self.Settings.purse))\
                .grid(row=1, column=1, columnspan=2, padx=10, pady=10, 
                      sticky=tk.W)
        if self.Settings.betting_option == 'Fixed':
            tk.Label(self.bet, text="Betting Amount: ${:.2f}"\
                     .format(self.Settings.betting_amount), font=(None,font_body))\
                    .grid(row=2, column=1, columnspan=2, padx=20, pady=10, 
                          sticky=tk.W)
        else:
            tk.Label(self.bet, text="Betting Amount: $", font=(None,font_body))\
                     .grid(row=2, column=1, columnspan=2, sticky=tk.W, 
                           padx=20, pady=10)
            self.new_bet = tk.Spinbox(self.bet, state='readonly',
                                      from_=2.00, to=self.Settings.purse,
                                      width=5, format="%.2f", font=(None,font_body))
            self.new_bet.grid(row=2, column=2, columnspan=2, padx=20, 
                              sticky=tk.W)
        tk.Label(self.bet, text="Odds:\n {}".format(self.horses_odds),\
                 justify='left', font=(None,font_body))\
                .grid(row=3, column=1, columnspan=2, padx=20, pady=10, 
                      sticky=tk.W)
        tk.Label(self.bet, justify='left', font=(None,font_body),
                 text="Possible Winnings:\n ${}".format(self.horses_winnings))\
                .grid(row=3, column=2, padx=20, sticky=tk.W)

        if self.Settings.option_suggestion == "Bet":
            tk.Label(self.bet, justify='left', font=(None,font_body),
                     text="AIde's Suggestion: {}".format(self.horse_pwin))\
                    .grid(row=4, column=1, columnspan=2, padx=20, pady=10, 
                          sticky=tk.W)
            tk.Label(self.bet, text="Horse you want to bet on:", 
                     font=(None,font_body))\
                    .grid(row=5, column=1, columnspan=2, padx=20, sticky=tk.W)

            self.horse_select.grid(row=5, column=1, columnspan=2, 
                                   padx=35, pady=5, sticky=tk.W + tk.S)

            # submit button
            tk.Button(self.bet, text='Submit', 
                      command=self.retrieving_data, font=(None,font_body-5))\
                     .grid(row=7, column=1, columnspan=2, padx=10, pady=10)
        else:
            tk.Label(self.bet, text="Horse you want to bet on:", 
                     font=(None,font_body))\
                    .grid(row=4, column=1, columnspan=2, padx=20, sticky=tk.W)

            self.horse_select.grid(row=5, column=1, columnspan=2, 
                                   padx=35, sticky=tk.W + tk.N)

            # submit button
            tk.Button(self.bet, text='Submit', 
                      command=self.s_suggestion, font=(None,font_body))\
                     .grid(row=6, column=1, columnspan=2, padx=10, pady=10)

    def s_suggestion(self):
        # check if a horse is selected
        if self.horsemenu.get() == "Select horse":
            error = tk.Tk()
            error.title("ERROR")
            error.bind('<Control-q>', sys.exit)
            error.resizable(width=False, height=False)
            tk.Label(error, text="Please select a horse.", 
                     font=(None,font_body))\
                    .pack(padx=10, pady=10)
            tk.Button(error, text="OK", command=lambda: error.destroy())\
                     .pack(padx=10, pady=10)

        else:
            # check how long the user took to submit
            print(self.timer_label['text'])

            if self.Settings.betting_option == 'Variable':
                self.Settings.betting_amount = float(self.new_bet.get())

            # delete old frame
            self.bet.destroy()

            # create new frame for suggestion
            self.s_suggest = tk.Frame(self.master)
            self.s_suggest.grid()
            for i in range(3):
                self.s_suggest.grid_columnconfigure(
                        i, minsize=int(screen_width/3))
            for i in range(4):
                if i == 0 or i == 3:
                    self.s_suggest.grid_rowconfigure(
                        i, minsize=int(screen_height/4))

            self.t = 120
            self.timer_label = tk.Label(self.s_suggest, textvariable="", 
                                        font=(None,font_body), justify='right')
            self.timer_label.grid(row=0, column=0, 
                                  sticky=tk.N + tk.W)
            self.countdown()

            suggestion_text = "AIde's suggestion: {}\n\nYour choice: {}" +\
                              "\n\nWould you like to change your choice?"
            suggestion_text = suggestion_text.format(self.horse_pwin, 
                                                     self.horsemenu.get())
            lines = suggestion_text.split("\n")

            # manipulating the suggestion text as a list of lines, 
            # depending on what the settings say to display. 
            # having a list was easier to manage, afterwards 
            # the list is joined back into a big string

            # Complete Order
            if self.Settings.displayorder: 
                lines.insert(1, "Predicted placing:")

                header = " "*25 # 18 spaces
                if self.Settings.displaytime:
                    header += "(T)"
                if self.Settings.displaybeyer:
                    header += "          (B)"
                lines.insert(2, header)

                pRank = len(self.horses_racing)
                for horse in sorted(self.horses_racing, 
                                    key=lambda h:h['P_Time'], reverse=True):
                    hStr = "{}: {:>18}".format(pRank, horse['B_Horse'])
                    if self.Settings.displaytime:
                       hStr += "      {}".format(horse['P_Time'])
                    if self.Settings.displaybeyer:
                       hStr += "      {:.2f}".format(horse['P_BSF'])
                    lines.insert(3, hStr)
                    pRank -= 1
            else:
                self.horses_racing.sort(key=lambda h:h['P_Time'])
                # Time
                if self.Settings.displaytime: 
                    lines.insert(1, "With a time of {}."
                                   .format(self.horses_racing[0]['P_Time']))
                    if self.Settings.displaybeyer:
                        # change last character of previous line to a comma
                        lines[1] = lines[1][:-1] + ","
                        lines.insert(2, "and a BSF of {}."
                                   .format(self.horses_racing[0]['P_BSF']))
                else:
                    # Beyer
                    if self.Settings.displaybeyer: 
                        lines.insert(1, "With a BSF of {}."
                                   .format(self.horses_racing[0]['P_BSF']))

            suggestion_text = "\n".join(lines)

            tk.Label(self.s_suggest, font=(None,font_title), text=suggestion_text)\
                    .grid(row=1, column=1)
            self.horse_select = tk.OptionMenu(self.s_suggest, self.horsemenu, 
                                          *self.horse_names)
            self.horse_select.config(font=(None,font_body+5))
            self.horse_select.grid(row=2, column=1)
            tk.Button(self.s_suggest, text="Submit", command=self.retrieving_data,
                     font=(None,font_body)).grid(row=3, column=1)

    def retrieving_data(self):

        # check if suggestion screen needs to be deleted
        if hasattr(self, 's_suggest'):
            self.s_suggest.destroy()
            self.t = self.Settings.time_limit * 60
        else:
            # check how long the user took to submit
            print(self.timer_label['text'])

            if self.Settings.betting_option == 'Variable':
                self.Settings.betting_amount = float(self.new_bet.get())

        # check if a horse is selected
        if self.horsemenu.get() == "Select horse" and self.t != -1:
            error = tk.Tk()
            error.title("ERROR")
            error.bind('<Control-q>', sys.exit)
            error.resizable(width=False, height=False)
            tk.Label(error, text="Please select a horse.", 
                     font=(None,font_body))\
                    .pack(padx=10, pady=10)
            tk.Button(error, text="OK", command=lambda: error.destroy())\
                     .pack(padx=10, pady=10)
        else:
            # delete old frame
            self.bet.destroy()

            # variable to keep track if there are more races
            self.next_race = True

            # create a new window for retrieving data
            self.retrieve = tk.Tk()
            self.retrieve.title("Retrieving Data")
            self.retrieve.bind('<Control-q>', sys.exit)
            self.retrieve.resizable(width=False, height=False)

            tk.Label(self.retrieve, text="Retrieving Data...", 
                     font=(None,40))\
                    .pack(padx=10, pady=10)

            # delete window after 2 seconds
            self.retrieve.after(2000, lambda: self.results())
            self.retrieve.mainloop()

    def update_purse(self):
        """ updates the purse """
        # take away money used to bet
        self.Settings.purse -= self.Settings.betting_amount

        # if bet on the right horse, calculate winnings
        if self.horse_win == self.horsemenu.get():
            for horse in self.superhorses:
                if horse['B_Horse'] == self.horsemenu.get():
                    odds = horse['B_MLOdds'].split('-')
            if self.Settings.betting_amount != 0:
                self.Settings.purse = (((self.Settings.betting_amount * 
                                         float(odds[0])) / 
                                        float(odds[1])) + 
                                       self.Settings.purse)

        if self.Settings.purse == 0:
            no_money = tk.Tk()
            no_money.title('No Money')
            no_money.bind('<Control-q>', sys.exit)
            no_money.resizable(width=False, height=False)
            tk.Label(no_money, text="You ran out of money! Game over.", 
                    font = (None, 20)).pack(padx = 10, pady = 10)
            tk.Button(no_money, text='OK', command=lambda : 
                    no_money.destroy()).pack(padx=10, pady=10)
            self.Settings.trials = 1

    def results(self):
        """ displays the results of the race """
        # destroy the retrieving screen and create a new screen for results
        self.retrieve.destroy()
        self.result = tk.Frame(self.master)
        self.result.grid()
        # nine rows
        for i in range(8):
            if i == 0 or i == 7:
                self.result.grid_rowconfigure(
                    i, minsize=int(screen_height/5))
            else:
                self.result.grid_rowconfigure(
                    i, minsize=int(((3/5)*screen_height)/5))
        # different number of columns for different settings
        for i in range(4):
            if i == 0 or i == 3:
                self.result.grid_columnconfigure(
                    i, minsize=int(screen_width/3))
            else:
                self.result.grid_columnconfigure(
                     i, minsize=int(((1/3)*screen_width)/2))

        # result labels
        # different spacing for different settings
        tk.Label(self.result, text='Results', font=(None,font_title))\
                .grid(row=1, column=1, columnspan=2, pady=(50, 20))

        tk.Label(self.result, text='Actual result:', font=(None,font_body))\
                .grid(row=2, column=1, pady=10, sticky=tk.N + tk.W)
        tk.Label(self.result, text='{}'.format(self.horse_win), 
                 font=(None,font_body), fg='red', justify='left')\
                .grid(row=2, column=2, pady=10, sticky=tk.N + tk.W)

        tk.Label(self.result, text="AIde's suggestion: ", font=(None,font_body))\
                .grid(row=3, column=1, pady=10, sticky=tk.N + tk.W)
        tk.Label(self.result, text='{}'.format(self.horse_pwin), 
                 font=(None,font_body), fg='red')\
                .grid(row=3, column=2, pady=10, sticky=tk.N + tk.W)

        tk.Label(self.result, text='Your choice: ', font=(None,font_body))\
                .grid(row=4, column=1, pady=10, sticky = tk.N + tk.W)
        if self.horsemenu.get() == 'Select horse':
            tk.Label(self.result, text='None', font=(None,font_body), fg='red')\
                .grid(row=4, column=2, pady=10, sticky=tk.N + tk.W)
        else:
            tk.Label(self.result, text='{}'.format(self.horsemenu.get()), 
                     font=(None,font_body), fg='red')\
                    .grid(row=4, column=2, pady=10, sticky=tk.N + tk.W)

        # update the users purse
        self.update_purse()
        tk.Label(self.result, text='Current Purse: ', font=(None,font_body))\
                .grid(row=5, column=1, pady=10, sticky=tk.N + tk.W)
        tk.Label(self.result, text='${:.2f}'.format(self.Settings.purse),
                 font=(None,font_body), fg='red')\
                .grid(row=5, column=2, pady=10, sticky=tk.N + tk.W)

        # check if there are more races to display 'next race' or 'exit'
        # different spacing for different settings
        if self.Settings.trials == 1:
            tk.Button(self.result, text='Exit', 
                      font=(None,font_body), command=self.exit)\
                     .grid(row=6, column=1, columnspan=2, pady=10, sticky=tk.N)
        else:
            tk.Button(self.result, text='Next Race', 
                      font=(None,font_body), command=self.races)\
                     .grid(row=6, column=1, columnspan=2, pady=10, sticky=tk.N)

    def races(self):
        # if there are more races, decrement trials and load another race
        if self.Settings.trials > 0:
            self.betting_screen()
            self.Settings.trials -= 1

    def exit(self):
        # destroy result screen and make a new exit screen
        if hasattr(self, 'result'):
            self.result.destroy()
        self.exit = tk.Frame(self.master)
        self.exit.grid()
        for i in range(3):
            self.exit.grid_rowconfigure(i, minsize=int(screen_height/3))
            self.exit.grid_columnconfigure(i, minsize=int(screen_width/3))
            
        # instructions for inserting ID number
        tk.Label(self.exit, text='Thank you!\nPlease notify the researcher.'
                 '\nPlease enter the ID number in order to save.',
                 font=(None,font_title+5))\
                .grid(row=1, column=0, columnspan=3)

        self.save=tk.Entry(self.exit, width=30)
        self.save.grid(row=1, column=0, columnspan=3, sticky=tk.S)

        # save button
        tk.Button(self.exit, text='Save', font=(None,font_body), 
                  command=self.checksave)\
                 .grid(row=2, column=0, columnspan=3, pady=15, sticky=tk.N)

    def checksave(self):
        # check the ID number
        # if ID number is -0, don't save
        # otherwise, save
        # check if -0 
        if self.save.get() == "-0":
            print("NO SAVE")
            self.exit.destroy()

        # check if no entry
        elif self.save.get() == "":
            error = tk.Tk()
            error.title("ERROR")
            error.bind('<Control-q>', sys.exit)
            error.resizable(width=False, height=False)
            tk.Label(error, text="Please insert ID number.", font=(None,font_body))\
                    .pack(padx=10, pady=10)
            tk.Button(error, text="OK", command=lambda: error.destroy())\
                     .pack(padx=10, pady=10)

        # save if pass all tests
        else:
            # check if entry is numbers
            try:
                int(self.save.get())
                print("SAVE")
                self.master.destroy()
            except ValueError:
                error = tk.Tk()
                error.title("ERROR")
                error.bind('<Control-q>', sys.exit)
                error.resizable(width=False, height=False)
                tk.Label(error, text="Please insert numbers.", font=(None,font_body))\
                        .pack(padx=10, pady=10)
                tk.Button(error, text="OK", command=lambda: self.master.destroy())\
                         .pack(padx=10, pady=10)


root = tk.Tk()
# find screen size
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()
if screen_height <= 800:
    font_body=15
    font_title=25
elif screen_height >= 801:
    font_body=22
    font_title=30


def run():
    root.title("Horse Racing")
    # full screen window
    root.geometry("%dx%d+0+0" % (screen_width, screen_height))
    root.bind('<Control-q>', sys.exit)
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    run()
