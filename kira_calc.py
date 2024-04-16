import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import os
import datetime
import math
import json
import ttkwidgets

import ctypes

myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class Application(tk.Frame):
	def __init__(self, master=None):	
		super().__init__(master)
		self.master = master
		self.pack()
		self.master.title("Kirara Calculator")
		self.master.iconphoto(False, tk.PhotoImage(file='kirara_icon.png'))
		self.master.iconbitmap(default='kirara_icon.ico')
		
		self.auto_complete_flag = 0
		self.auto_counter = 0
		self.waifu_check_flag = 1
		self.hour = datetime.datetime.today().hour
		
		try:
			self.fp = open("data.json", "r+")
			self.data = json.load(self.fp)
		except IOError:
			self.fp = open("data.json", "w")
			self.data = {}
			self.data["userrank"] = 1
			self.data["expleft"] = 100
			self.data["questexp"] = 25
			self.data["questcost"] = 10
			self.data["questtime"] = 30
			
			self.data["eventcost"] = 25
			self.data["ticketrate"] = 0.15
			self.fp.close()
			self.fp = open("data.json", "r+")
	
		self.create_widgets()
		self.calc_values()
		
	def __del__(self):
		print("Closing Program")
		
		self.fp.seek(0)
		self.fp.truncate(0)
		json.dump(self.data, self.fp)
		
		self.fp.close()

	def create_widgets(self):
		#self.label_rank_title = tk.Label(text="kirara calculator")
		#self.label_rank_title.pack()
		window = tk.Frame(master=self.master)
		window.pack()
		
		tab_parent = ttk.Notebook(master = self.master)
		frame_rank = tk.Frame(tab_parent)
		frame_event = tk.Frame(tab_parent)
		
		tab_parent.add(frame_rank, text="Rank Calculator")
		tab_parent.add(frame_event, text="Event Calculator")
		
		tab_parent.pack(expand=1, fill='both')
		
		
		self.label_rank_userrank = tk.Label(master=frame_rank, text="User Rank")
		self.label_rank_userrank.pack()
		self.entry_rank_userrank = tk.Entry(master=frame_rank)
		self.entry_rank_userrank.insert(0, self.data["userrank"])
		self.entry_rank_userrank.pack()
		
		self.label_rank_expleft = tk.Label(master=frame_rank, text="Experience Left")
		self.label_rank_expleft.pack()
		self.entry_rank_expleft = tk.Entry(master=frame_rank)
		self.entry_rank_expleft.insert(0, self.data["expleft"])
		self.entry_rank_expleft.pack()
		
		self.label_rank_questexp = tk.Label(master=frame_rank, text="Quest Experience")
		self.label_rank_questexp.pack()
		self.entry_rank_questexp = tk.Entry(master=frame_rank)
		self.entry_rank_questexp.insert(0, self.data["questexp"])
		self.entry_rank_questexp.pack()
		
		self.label_rank_questcost = tk.Label(master=frame_rank, text="Quest Stamina Cost")
		self.label_rank_questcost.pack()
		self.entry_rank_questcost = tk.Entry(master=frame_rank)
		self.entry_rank_questcost.insert(0, self.data["questcost"])
		self.entry_rank_questcost.pack()
		
		self.label_rank_questtime = tk.Label(master=frame_rank, text="Expected Quest Time")
		self.label_rank_questtime.pack()
		self.entry_rank_questtime = tk.Entry(master=frame_rank)
		self.entry_rank_questtime.insert(0, self.data["questtime"])
		self.entry_rank_questtime.pack()
		
		
		
		#self.entry_rank_exp = tk.Entry()
		#self.entry_rank_exp.pack()
		
		
		window = tk.Frame(master=frame_rank)
		window.pack()
		
		frame_buttons = tk.Frame(master = window)
		
		frame_buttons.grid(row=0, column=0)
		self.button_rank_calcVal = tk.Button(master = frame_buttons, text="Calculate Values", command=self.calc_values)
		self.button_rank_calcVal.pack()
		
		frame_buttons = tk.Frame(master = window)
		
		frame_buttons.grid(row=0, column=1)
		self.button_rank_questComplete = tk.Button(master = frame_buttons, text="Complete Quest", command=self.quest_complete)
		self.button_rank_questComplete.pack()
		
		frame_buttons = tk.Frame(master = window)
		
		frame_buttons.grid(row=0, column=2)
		self.button_rank_toggleAuto = tk.Button(master = frame_buttons, text="Toggle Auto", bg="#FA7272", command=self.toggle_auto)
		self.button_rank_toggleAuto.pack()
		
		frame_buttons = tk.Frame(master = window)
		
		frame_buttons.grid(row=0, column=3)
		#self.button_rank_waifuCheck = tk.Button(master = frame_buttons, text="Check Waifus!", bg="#B5FA70", command=self.toggle_waifu_check)
		#self.button_rank_waifuCheck.pack()
		
		self.label_rank_questreq = tk.Label(master=frame_rank, text="Quests remaining: ")
		self.label_rank_stamreq = tk.Label(master=frame_rank, text="Stamina remaining: ")
		self.label_rank_questreq.pack()
		self.label_rank_stamreq.pack()
		
		self.label_rank_timeLeft = tk.Label(master=frame_rank, text="Time remaining: ")
		self.label_rank_timeLeft.pack()
		
		self.label_rank_timeLeftS = tk.Label(master=frame_rank, text="Seconds Remaining: ")
		self.label_rank_timeLeftM = tk.Label(master=frame_rank, text="Minutes Remaining: ")
		self.label_rank_timeLeftH = tk.Label(master=frame_rank, text="Hours Remaining: ")
		self.label_rank_timeLeftD = tk.Label(master=frame_rank, text="Days Remaining: ")
		self.label_rank_timeLeftS.pack()
		self.label_rank_timeLeftM.pack()
		self.label_rank_timeLeftH.pack()
		self.label_rank_timeLeftD.pack()
		
		self.label_rank_stamCap = tk.Label(master=frame_rank, text="Stamina Capacity: ")
		self.label_rank_stamCap.pack()
		
		window = tk.Frame(master=frame_rank)
		window.pack()
		
		frame = tk.Frame(master = window, relief=tk.RAISED, borderwidth=1)
		frame.grid(row = 0, column = 0)
		
		
		self.label_rank_clockreq = tk.Label(master=frame, text="Clocks Required")
		self.label_rank_clockreq.pack()
		
		self.label_rank_goldClockReq = tk.Label(master=frame, text="Gold: ")
		self.label_rank_silverClockReq = tk.Label(master=frame, text="Silver: ")
		self.label_rank_bronzeClockReq = tk.Label(master=frame, text="Bronze: ")
		self.label_rank_goldClockReq.pack()
		self.label_rank_silverClockReq.pack()
		self.label_rank_bronzeClockReq.pack()
		
		frame = tk.Frame(master = window, relief=tk.RAISED, borderwidth=1)
		frame.grid(row = 0, column = 1)
		
		self.label_rank_clockRegenReq = tk.Label(master=frame, text="Clocks w/Regen Required")
		self.label_rank_clockRegenReq.pack()
		
		self.label_rank_goldStamClockReq = tk.Label(master=frame, text="Gold: ")
		self.label_rank_silverStamClockReq = tk.Label(master=frame, text="Silver: ")
		self.label_rank_bronzeStamClockReq = tk.Label(master=frame, text="Bronze: ")
		self.label_rank_goldStamClockReq.pack()
		self.label_rank_silverStamClockReq.pack()
		self.label_rank_bronzeStamClockReq.pack()
		
		self.label_rank_stamRegen = tk.Label(master=frame_rank, text="Stamina Regenerated: ")
		self.label_rank_stamRegen.pack()
				
		self.label_rank_stamToEnd = tk.Label(master=frame_rank, text="Expected Completion Time: ")
		self.label_rank_stamToEnd.pack()
		
		#-------------Start event packing-------------
		
		self.label_event_userrank = tk.Label(master=frame_event, text="User Rank")
		self.label_event_userrank.pack()
		
		self.entry_event_userrank = tk.Entry(master=frame_event)
		self.entry_event_userrank.insert(0, self.data["userrank"])
		self.entry_event_userrank.pack()
		
		
		self.label_event_questcost = tk.Label(master=frame_event, text="Quest Cost")
		self.label_event_questcost.pack()
		
		self.entry_event_questcost = tk.Entry(master=frame_event)
		self.entry_event_questcost.insert(0, self.data["eventcost"])
		self.entry_event_questcost.pack()
		
		
		self.label_event_teamBonus = tk.Label(master=frame_event, text="Team Bonus")
		self.label_event_teamBonus.pack()
		
		
		self.label_event_teamBonusCommon = tk.Label(master=frame_event, text="Common Team Bonus")
		self.label_event_teamBonusCommon.pack()
		self.entry_event_teamBonusCommon = tk.Entry(master=frame_event)
		self.entry_event_teamBonusCommon.insert(0, 0)
		self.entry_event_teamBonusCommon.pack()
		
		self.label_event_teamBonusUncommon = tk.Label(master=frame_event, text="Uncommon Team Bonus")
		self.label_event_teamBonusUncommon.pack()
		self.entry_event_teamBonusUncommon = tk.Entry(master=frame_event)
		self.entry_event_teamBonusUncommon.insert(0, 0)
		self.entry_event_teamBonusUncommon.pack()
		
		
		self.label_event_commonDrop = tk.Label(master=frame_event, text="Common Drop Rate")
		self.label_event_commonDrop.pack()
		
		self.frame_event_commonFrame = tk.Frame(master=frame_event, relief=tk.RAISED, borderwidth=1)
		self.frame_event_commonFrame.pack()
		
		
		self.frame_event_commonDrop = tk.Frame(master=self.frame_event_commonFrame)
		self.frame_event_commonDrop.grid(row = 0, column = 0)
		
		self.label_event_commonBase = tk.Label(master=self.frame_event_commonDrop, text="Base: ")
		self.label_event_commonBase.pack()
		
		self.entry_event_commonBase = tk.Entry(master=self.frame_event_commonDrop)
		self.entry_event_commonBase.insert(0, 0)
		self.entry_event_commonBase.pack()
		
		self.frame_event_commonBonus = tk.Frame(master=self.frame_event_commonFrame)
		self.frame_event_commonBonus.grid(row = 0, column = 1)
		
		self.label_event_commonBonus = tk.Label(master=self.frame_event_commonBonus, text="Bonus: ")
		self.label_event_commonBonus.pack()
		
		self.entry_event_commonBonus = tk.Entry(master=self.frame_event_commonBonus)
		self.entry_event_commonBonus.insert(0, 0)
		self.entry_event_commonBonus.pack()
		
		
		self.label_event_uncommonDrop = tk.Label(master=frame_event, text="Uncommon Drop Rate")
		self.label_event_uncommonDrop.pack()
		
		self.frame_event_uncommonFrame = tk.Frame(master=frame_event, relief=tk.RAISED, borderwidth=1)
		self.frame_event_uncommonFrame.pack()

		self.frame_event_uncommonDrop = tk.Frame(master=self.frame_event_uncommonFrame)
		self.frame_event_uncommonDrop.grid(row = 0, column = 0)

		self.label_event_uncommonBase = tk.Label(master=self.frame_event_uncommonDrop, text="Base: ")
		self.label_event_uncommonBase.pack()

		self.entry_event_uncommonBase = tk.Entry(master=self.frame_event_uncommonDrop)
		self.entry_event_uncommonBase.insert(0, 0)
		self.entry_event_uncommonBase.pack()

		self.frame_event_uncommonBonus = tk.Frame(master=self.frame_event_uncommonFrame)
		self.frame_event_uncommonBonus.grid(row = 0, column = 1)

		self.label_event_uncommonBonus = tk.Label(master=self.frame_event_uncommonBonus, text="Bonus: ")
		self.label_event_uncommonBonus.pack()

		self.entry_event_uncommonBonus = tk.Entry(master=self.frame_event_uncommonBonus)
		self.entry_event_uncommonBonus.insert(0, 0)
		self.entry_event_uncommonBonus.pack()
		
		
		self.label_event_ticketRate = tk.Label(master=frame_event, text="Ticket Drop Rate")
		self.label_event_ticketRate.pack()
		
		self.entry_event_ticketRate = tk.Entry(master=frame_event)
		self.entry_event_ticketRate.insert(0, self.data["ticketrate"])
		self.entry_event_ticketRate.pack()
		
		
		self.label_event_shopitems = tk.Label(master=frame_event, text="Desired Shop Items")
		self.label_event_shopitems.pack()
		
		#tree = ttk.CheckboxTreeview(master=frame_event, columns=('item', 'cost'))
		self.tree = ttkwidgets.CheckboxTreeview(master=frame_event, columns=('desired', 'stock', 'cost', 'item'))
		self.tree.heading("desired", text="Desired")
		self.tree.heading("stock", text="Stock")
		self.tree.heading("cost", text="Cost")
		self.tree.heading("item", text="Item")
		self.tree.column('desired', width=70, anchor='center')
		self.tree.column('stock', width=70, anchor='center')
		self.tree.column('cost', width=70, anchor='center')
		self.tree.column('item', width=70, anchor='center')
		
		
		
		lvlmat = self.tree.insert('', 'end', text="Enhancement Material")
		
		id = self.tree.insert(lvlmat, 'end', text="Sprouts")
		
		self.tree.insert(id, 'end', text="Fire Sprout", values=(50, 50, 30, "common"))
		self.tree.insert(id, 'end', text="Wind Sprout", values=(50, 50, 30, "common"))
		self.tree.insert(id, 'end', text="Earth Sprout", values=(50, 50, 30, "common"))
		self.tree.insert(id, 'end', text="Water Sprout", values=(50, 50, 30, "common"))
		self.tree.insert(id, 'end', text="Moon Sprout", values=(50, 50, 30, "common"))
		self.tree.insert(id, 'end', text="Sun Sprout", values=(50, 50, 30, "common"))
		
		id = self.tree.insert(lvlmat, 'end', text="Large Seeds")
		
		self.tree.insert(id, 'end', text="Large Fire Seed", values=(200, 200, 8, "common"))
		self.tree.insert(id, 'end', text="Large Wind Seed", values=(200, 200, 8, "common"))
		self.tree.insert(id, 'end', text="Large Earth Seed", values=(200, 200, 8, "common"))
		self.tree.insert(id, 'end', text="Large Water Seed", values=(200, 200, 8, "common"))
		self.tree.insert(id, 'end', text="Large Moon Seed", values=(200, 200, 8, "common"))
		self.tree.insert(id, 'end', text="Large Sun Seed", values=(200, 200, 8, "common"))
		
		
		
		lbmat = self.tree.insert('', 'end', text="Limit Break Material")
		
		id = self.tree.insert(lbmat, 'end', text="Fruits")
		self.tree.insert(id, 'end', text="Warrior's Fruit",   values=(50, 50, 2, "uncommon"))
		self.tree.insert(id, 'end', text="Mages's Fruit",     values=(50, 50, 2, "uncommon"))
		self.tree.insert(id, 'end', text="Priest's Fruit",    values=(50, 50, 2, "uncommon"))
		self.tree.insert(id, 'end', text="Knight's Fruit",    values=(50, 50, 2, "uncommon"))
		self.tree.insert(id, 'end', text="Alchemist's Fruit", values=(50, 50, 2, "uncommon"))
		
		self.tree.insert(lbmat, 'end', text="Series-only Star Crystal", values=(8, 8, 1, "rare"))
		
		
		
		evomat = self.tree.insert('', 'end', text="Evolution Material")
		
		id = self.tree.insert(evomat, 'end', text="Super Evolution Gem")
		self.tree.insert(id, 'end', text="Super Fire Evolution Gem",  values=(10, 10, 40, "common"))
		self.tree.insert(id, 'end', text="Super Wind Evolution Gem",  values=(10, 10, 40, "common"))
		self.tree.insert(id, 'end', text="Super Earth Evolution Gem", values=(10, 10, 40, "common"))
		self.tree.insert(id, 'end', text="Super Water Evolution Gem", values=(10, 10, 40, "common"))
		self.tree.insert(id, 'end', text="Super Moon Evolution Gem",  values=(10, 10, 40, "common"))
		self.tree.insert(id, 'end', text="Super Sun Evolution Gem",   values=(10, 10, 40, "common"))
		
		id = self.tree.insert(evomat, 'end', text="Extra Large Evolution Gem")
		self.tree.insert(id, 'end', text="Extra Large Fire Evolution Gem",  values=(20, 20, 15, "common"))
		self.tree.insert(id, 'end', text="Extra Large Wind Evolution Gem",  values=(20, 20, 15, "common"))
		self.tree.insert(id, 'end', text="Extra Large Earth Evolution Gem", values=(20, 20, 15, "common"))
		self.tree.insert(id, 'end', text="Extra Large Water Evolution Gem", values=(20, 20, 15, "common"))
		self.tree.insert(id, 'end', text="Extra Large Moon Evolution Gem",  values=(20, 20, 15, "common"))
		self.tree.insert(id, 'end', text="Extra Large Sun Evolution Gem",   values=(20, 20, 15, "common"))
		
		id = self.tree.insert(evomat, 'end', text="Large Evolution Gem")
		self.tree.insert(id, 'end', text="Large Fire Evolution Gem",  values=(40, 40, 6, "common"))
		self.tree.insert(id, 'end', text="Large Wind Evolution Gem",  values=(40, 40, 6, "common"))
		self.tree.insert(id, 'end', text="Large Earth Evolution Gem", values=(40, 40, 6, "common"))
		self.tree.insert(id, 'end', text="Large Water Evolution Gem", values=(40, 40, 6, "common"))
		self.tree.insert(id, 'end', text="Large Moon Evolution Gem",  values=(40, 40, 6, "common"))
		self.tree.insert(id, 'end', text="Large Sun Evolution Gem",   values=(40, 40, 6, "common"))
		
		id = self.tree.insert(evomat, 'end', text="Evolution Gem")
		self.tree.insert(id, 'end', text="Fire Evolution Gem",  values=(60, 60, 4, "common"))
		self.tree.insert(id, 'end', text="Wind Evolution Gem",  values=(60, 60, 4, "common"))
		self.tree.insert(id, 'end', text="Earth Evolution Gem", values=(60, 60, 4, "common"))
		self.tree.insert(id, 'end', text="Water Evolution Gem", values=(60, 60, 4, "common"))
		self.tree.insert(id, 'end', text="Moon Evolution Gem",  values=(60, 60, 4, "common"))
		self.tree.insert(id, 'end', text="Sun Evolution Gem",   values=(60, 60, 4, "common"))
		
		id = self.tree.insert(evomat, 'end', text="Small Evolution Gem")
		self.tree.insert(id, 'end', text="Small Fire Evolution Gem",  values=(100, 100, 2, "common"))
		self.tree.insert(id, 'end', text="Small Wind Evolution Gem",  values=(100, 100, 2, "common"))
		self.tree.insert(id, 'end', text="Small Earth Evolution Gem", values=(100, 100, 2, "common"))
		self.tree.insert(id, 'end', text="Small Water Evolution Gem", values=(100, 100, 2, "common"))
		self.tree.insert(id, 'end', text="Small Moon Evolution Gem",  values=(100, 100, 2, "common"))
		self.tree.insert(id, 'end', text="Small Sun Evolution Gem",   values=(100, 100, 2, "common"))
		
		id = self.tree.insert(evomat, 'end', text="Gold Statue")
		self.tree.insert(id, 'end', text="Warrior's Gold Statue",   values=(5, 5, 30, "common"))
		self.tree.insert(id, 'end', text="Mage's Gold Statue",      values=(5, 5, 30, "common"))
		self.tree.insert(id, 'end', text="Priest's Gold Statue",    values=(5, 5, 30, "common"))
		self.tree.insert(id, 'end', text="Knight's Gold Statue",    values=(5, 5, 30, "common"))
		self.tree.insert(id, 'end', text="Alchemist's Gold Statue", values=(5, 5, 30, "common"))
		
		id = self.tree.insert(evomat, 'end', text="Silver Statue")
		self.tree.insert(id, 'end', text="Warrior's Silver Statue",   values=(15, 15, 6, "common"))
		self.tree.insert(id, 'end', text="Mage's Silver Statue",      values=(15, 15, 6, "common"))
		self.tree.insert(id, 'end', text="Priest's Silver Statue",    values=(15, 15, 6, "common"))
		self.tree.insert(id, 'end', text="Knight's Silver Statue",    values=(15, 15, 6, "common"))
		self.tree.insert(id, 'end', text="Alchemist's Silver Statue", values=(15, 15, 6, "common"))
		
		id = self.tree.insert(evomat, 'end', text="Bronze Statue")
		self.tree.insert(id, 'end', text="Warrior's Bronze Statue",   values=(25, 25, 3, "common"))
		self.tree.insert(id, 'end', text="Mage's Bronze Statue",      values=(25, 25, 3, "common"))
		self.tree.insert(id, 'end', text="Priest's Bronze Statue",    values=(25, 25, 3, "common"))
		self.tree.insert(id, 'end', text="Knight's Bronze Statue",    values=(25, 25, 3, "common"))
		self.tree.insert(id, 'end', text="Alchemist's Bronze Statue", values=(25, 25, 3, "common"))
		
		
		
		wepmat = self.tree.insert('', 'end', text="Weapon and Material")
		id = self.tree.insert(wepmat, 'end', text="Weapon Crest")
		self.tree.insert(id, 'end', text="Warrior's Crest",   values=(100, 100, 50, "common"))
		self.tree.insert(id, 'end', text="Mage's Crest",      values=(100, 100, 50, "common"))
		self.tree.insert(id, 'end', text="Priest's Crest",    values=(100, 100, 50, "common"))
		self.tree.insert(id, 'end', text="Knight's Crest",    values=(100, 100, 50, "common"))
		self.tree.insert(id, 'end', text="Alchemist's Crest", values=(100, 100, 50, "common"))
		
		id = self.tree.insert(wepmat, 'end', text="Weapon Symbol")
		self.tree.insert(id, 'end', text="Warrior's Crest",   values=(0, 99999, 6, "common"))
		self.tree.insert(id, 'end', text="Mage's Crest",      values=(0, 99999, 6, "common"))
		self.tree.insert(id, 'end', text="Priest's Crest",    values=(0, 99999, 6, "common"))
		self.tree.insert(id, 'end', text="Knight's Crest",    values=(0, 99999, 6, "common"))
		self.tree.insert(id, 'end', text="Alchemist's Crest", values=(0, 99999, 6, "common"))
		
		
		
		others = self.tree.insert('', 'end', text='Others')
		
		self.tree.insert(others, 'end', text="Summon Tickets", values=(5, 5, 200, "common"))
		
		id = self.tree.insert(others, 'end', text="Limit Break Item", values=(5, 5, 1050, "uncommon"))
		self.tree.insert(id, 'end', text="Limit Break Item", values=(1, 1, 500, "uncommon"))
		self.tree.insert(id, 'end', text="Limit Break Item", values=(2, 2, 200, "uncommon"))
		self.tree.insert(id, 'end', text="Limit Break Item", values=(1, 1, 100, "uncommon"))
		self.tree.insert(id, 'end', text="Limit Break Item", values=(1, 1, 50, "uncommon"))
		
		id = self.tree.insert(others, 'end', text="Gaystone", values=(4, 4, 5500, "uncommon"))
		self.tree.insert(id, 'end', text="Gaystone", values=(2, 2, 1000, "uncommon"))
		self.tree.insert(id, 'end', text="Gaystone", values=(1, 1, 1500, "uncommon"))
		self.tree.insert(id, 'end', text="Gaystone", values=(1, 1, 2000, "uncommon"))
		
		self.tree.insert(others, 'end', text="Silver Key", values=(50, 50, 30, "common"))
		self.tree.insert(others, 'end', text="Gold Key", values=(30, 30, 20, "uncommon"))
		self.tree.insert(others, 'end', text="Exchange Medal", values=(150, 150, 5, "uncommon"))
		self.tree.insert(others, 'end', text="10,000 Coins", values=(10, 10, 5, "uncommon"))
		
		self.tree.insert(others, 'end', text="5,000 Coins", values=(0, 99999, 5, "uncommon"))
		self.tree.insert(others, 'end', text="2 Uncommon Event Items", values=(0, 99999, 1, "ticket"))
		
		
		
		self.tree.pack()
		
		self.master.bind("<<TreeviewSelect>>", self.update_desired_items)
		
		
		self.frame_event_desiredItems = tk.Frame(master=frame_event)
		self.frame_event_desiredItems.pack()
		
		self.label_event_desiredItems = tk.Label(master=self.frame_event_desiredItems, text="Items Desired: ")
		self.label_event_desiredItems.pack(side = "left")
		
		self.entry_event_desiredItems = tk.Entry(master=self.frame_event_desiredItems)
		self.entry_event_desiredItems.pack(side = "left")
		
		
		
		self.label_event_commonNeeded = tk.Label(master=frame_event, text="Common Items Needed: ")
		self.label_event_commonNeeded.pack()
		
		self.label_event_uncommonNeeded = tk.Label(master=frame_event, text="Uncommon Items Needed: ")
		self.label_event_uncommonNeeded.pack()
		
		self.label_event_rareNeeded = tk.Label(master=frame_event, text="Rare Items Needed: ")
		self.label_event_rareNeeded.pack()
		
		self.label_event_ticketNeeded = tk.Label(master=frame_event, text="Rare Items Needed: ")
		self.label_event_ticketNeeded.pack()
		
		self.label_event_estCompletion = tk.Label(master=frame_event, text="Estimated Quests Required: ")
		self.label_event_estCompletion.pack()
		
		
		
	def update_desired_items(self, event):
		if len(self.tree.selection()) > 0:
			item = self.tree.selection()[0]
			print(self.tree.get_children(item))
			if len(self.tree.get_children(item)) == 0:
				print("?")
				print(type(self.tree.set(item)))
				self.entry_event_desiredItems.delete(0)
				self.entry_event_desiredItems.insert(0, self.tree.set(item)["desired"])
				
				self.tree.set(item, "desired")

	def calc_values(self):
		#print(self.entry.get())
		print("Begin calcuations")
		
		self.data["userrank"] = userrank = int(self.entry_rank_userrank.get())
		self.data["expleft"] = expleft = int(self.entry_rank_expleft.get())
		self.data["questexp"] = questexp = int(self.entry_rank_questexp.get())
		self.data["questcost"] = questcost = int(self.entry_rank_questcost.get())
		self.data["questtime"] = questtime = float(self.entry_rank_questtime.get())
		
		if self.auto_complete_flag == 1:
			if self.auto_counter > questtime * 10:
				self.quest_complete()
				self.auto_counter = 0
			else:
				self.auto_counter += 1
		
		if self.hour != datetime.datetime.today().hour:
			self.hour = datetime.datetime.today().hour
			self.waifu_check_flag = 1
			#tk.Button(master = frame_buttons, text="Check Waifus!", bg="#B5FA70", command=self.toggle_waifu_check)
			self.button_rank_waifuCheck["text"] = "Check Waifus!"
			self.button_rank_waifuCheck["bg"] = "#B5FA70"
			self.button_rank_waifuCheck["fg"] = "#000000"
		
		questreq = expleft / questexp
		self.label_rank_questreq["text"] = "Quests Remaining: " + str(questreq)
		stamreq = questreq * questcost
		self.label_rank_stamreq["text"] = "Stamina Remaining: " + str(stamreq) 
		sec_left = questtime * questreq
		self.label_rank_timeLeft["text"] = "Time Remaining: " + str(datetime.timedelta(seconds = round(sec_left)))
		self.label_rank_timeLeftS["text"] = "Seconds Remaining: {:.1f}".format(sec_left)
		min_left = sec_left / 60
		self.label_rank_timeLeftM["text"] = "Minutes Remaining: {:.3f}".format(min_left)
		hour_left = min_left / 60
		self.label_rank_timeLeftH["text"] = "Hours Remaining: {:.3f}".format(hour_left)
		day_left = hour_left / 24
		self.label_rank_timeLeftD["text"] = "Days Remaining: {:.3f}".format(day_left)
		
		stamregen = min_left / 5
		self.label_rank_stamRegen["text"] = "Stamina Regenerated: {} ({:.3f})".format(math.floor(stamregen), stamregen)
		
		stam_cap = self.calc_rank_stam()
		gold_val = stam_cap
		silver_val = math.floor((stam_cap * 0.5))
		bronze_val = math.floor((stam_cap * 0.1))
		
		self.label_rank_stamCap["text"] = "Stamina Capacity: {}".format(stam_cap)
		
		gold_amt = stamreq / gold_val
		silver_amt = stamreq / silver_val
		bronze_amt = stamreq / bronze_val
		
		self.label_rank_goldClockReq["text"] = "Gold: {} ({:.3f})".format(math.ceil(gold_amt), gold_amt)
		self.label_rank_silverClockReq["text"] = "Silver: {} ({:.3f})".format(math.ceil(silver_amt), silver_amt)
		self.label_rank_bronzeClockReq["text"] = "Bronze: {} ({:.3f})".format(math.ceil(bronze_amt), bronze_amt)
		
		gold_amt = (stamreq - stamregen) / gold_val
		silver_amt = (stamreq - stamregen) / silver_val
		bronze_amt = (stamreq - stamregen) / bronze_val
		
		self.label_rank_goldStamClockReq["text"] = "Gold: {} ({:.3f})".format(math.ceil(gold_amt), gold_amt)
		self.label_rank_silverStamClockReq["text"] = "Silver: {} ({:.3f})".format(math.ceil(silver_amt), silver_amt)
		self.label_rank_bronzeStamClockReq["text"] = "Bronze: {} ({:.3f})".format(math.ceil(bronze_amt), bronze_amt)
		
		
		
		epoch = datetime.datetime.today().timestamp()
		timestamp = epoch + int(sec_left)
		date = datetime.datetime.fromtimestamp(timestamp).strftime("%A, %B %d, %Y %I:%M:%S%p")
		
		self.label_rank_stamToEnd["text"] = "Expected Completion Time: " + date
		
		
		#--------------event------------------
		
		if len(self.tree.selection()) > 0:
			item = self.tree.selection()[0]
			#self.entry_event_desiredItems
			#item = self.tree.selection()[0]
			#print(self.tree.get_children(item))
			if len(self.tree.get_children(item)) == 0:
				print("?")
				print(type(self.tree.set(item)))
				
				entry = int(self.entry_event_desiredItems.get())
				if entry < 0:
					entry = 0
					#self.entry_event_desiredItems.delete(0)
					#self.entry_event_desiredItems.insert(0, 0)
				if entry > int(self.tree.set(item)["stock"]):
					entry = int(self.tree.set(item)["stock"])
					#self.entry_event_desiredItems.delete(0)
					#self.entry_event_desiredItems.insert(0, int(self.tree.set(item)["stock"]))
				
				
				
				self.tree.set(item, column="desired", value=entry)
				
				#self.entry_event_desiredItems.delete(0)
				#self.entry_event_desiredItems.insert(0, self.tree.set(item)["stock"])
				#
				#self.tree.set(item, "desired")
		
		
		checked_list = self.tree.get_checked()
		shopping = {"common":0, "uncommon":0, "rare":0, "ticket":0}
		for item in checked_list:
			desired = self.tree.set(item)["desired"]
			item_name = self.tree.set(item)["item"]
			item_cost = self.tree.set(item)["cost"]
			
			print(desired)
			print(item_name)
			
			shopping[item_name] += int(desired) * int(item_cost)
			
		self.label_event_commonNeeded["text"] = "Common Items Needed: " + str(shopping["common"])
		self.label_event_uncommonNeeded["text"] = "Uncommon Items Needed: " + str(shopping["uncommon"])
		self.label_event_rareNeeded["text"] = "Rare Items Needed: " + str(shopping["rare"])
		self.label_event_ticketNeeded["text"] = "Ticket Items Needed: " + str(shopping["ticket"])
		#common
		#uncommon
		#rare
		#ticket
		
	
		cBase = float(self.entry_event_commonBase.get())
		cBonus = float(self.entry_event_commonBonus.get())
		
		uBase = float(self.entry_event_uncommonBase.get())
		uBonus = float(self.entry_event_commonBonus.get())

		tBonusC = float(self.entry_event_teamBonusCommon.get())
		tBonusU = float(self.entry_event_teamBonusUncommon.get())
		
		ticketRate = float(self.entry_event_ticketRate.get())

		# base + bonus * team_bonus ---- per quest
		
		questsNeeded = 0
		cNeeded = shopping["common"]
		uNeeded = shopping["uncommon"]
		
		cGot = 0
		uGot = 0
		tCount = 0
		
		tix_cBase = 64.25
		tix_cBonus = 5.4
		tix_uBase = 16.3
		tix_uBonus = 8.9
		
		while cNeeded > cGot or uNeeded > uGot:
			cGot += (cBase + cBonus * tBonusC)
			uGot += (uBase + uBonus * tBonusU)
			tCount += ticketRate
			if tCount > 1:
				cGot += tix_cBase + tix_cBonus * tBonusC
				cGot += tix_uBase + tix_uBonus * tBonusU
				tCount -= 1
			questsNeeded += 1
		print("Quests needed" + str(questsNeeded))
		self.label_event_estCompletion["text"] = "Estimated Quests Required: " + str(questsNeeded)
		print(cNeeded - cGot)
		print(uNeeded - uGot)
		
		#totalCommon = (cBase + cBonus * tBonusC)
		#totalUncommon = (uBase + uBonus * tBonusU)
		#cQuests = 0
		#uQuests = 0
		#if totalCommon != 0:
		#	cQuests = shopping["common"] / totalCommon
		#if totalUncommon != 0:
		#	uQuests = shopping["uncommon"] / totalUncommon
		#
		#tix_obtained = int(cQuests * ticketRate)
		#tix_obtained_old = -1
		#
		#while tix_obtained_old != tix_obtained:
		#	tixTotal = totalCommon + (tix_cBase * tix_obtained) + (tix_cBonus * tBonusC * tix_obtained)
		#	if tixTotal != 0:
		#		cQuests = shopping["common"] / tixTotal
		#	
		#	print("tickets")
		#	print(tix_obtained)
		#	print(tix_obtained_old)
		#	tix_obtained_old = tix_obtained
		#	tix_obtained = int(cQuests * ticketRate)
		#
		
		
		#print("Quests needed for common quests: " + str(cQuests))
		#print("Quests needed for uncommon quests: " + str(uQuests))
		
		# Figure out ticket drops
		# Shimmy down to result?
		# take cQuests required
		# ---begin loop---
		# use number of quests to calculate number of tickets obtained
		# use num of tickets to add mats to totalCommon
		# recalculate number of tickets obtained
		# loop--- until num of tickets obtained no longer changes
		
		# Alternatively iterate until rewards outnumber required amount

		
		
		
		
		
		
		
		
		
		
		
		self.master.after(100, self.calc_values)
		
	def quest_complete(self):
		print("complete quest")
		expleft = int(self.entry_rank_expleft.get())
		questexp = int(self.entry_rank_questexp.get())

		self.entry_rank_expleft.delete(0, END)
		self.entry_rank_expleft.insert(0, expleft - questexp)
		
	def toggle_auto(self):
		if self.auto_complete_flag == 0:
			print("auto on")
			self.auto_complete_flag = 1
			self.button_rank_toggleAuto["bg"] = "#B5FA70"
			self.auto_counter = 0
		else:
			print("auto off")
			self.auto_complete_flag = 0
			self.button_rank_toggleAuto["bg"] = "#FA7272"
			
	def toggle_waifu_check(self):	
		if self.waifu_check_flag == 1:
			self.waifu_check_flag = 0
			self.button_rank_waifuCheck["text"] = "Waifus checked"
			self.button_rank_waifuCheck["bg"] = "#e6e6e6"
			self.button_rank_waifuCheck["fg"] = "#b3b3b3"
		
		
	def calc_rank_stam(self):
		rank = int(self.entry_rank_userrank.get())
	
		if 1 <= rank and rank < 10:
			stam = 10 + (rank - 1) * 2
		if 10 <= rank and rank < 16:
			stam = 29 + (rank - 10) * 2
		if 16 <= rank and rank < 20:
			stam = 40 + (rank - 16)
		if 20 <= rank:
			stam = 45 + (rank - 20)
		
		return stam


root = tk.Tk()
app = Application(master=root)
app.mainloop()