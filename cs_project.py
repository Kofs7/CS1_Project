from tkinter import *
from tkinter import ttk
import requests
import tkinter as tk
import json
import datetime as dt
import os
import webbrowser


API_KEY = input("Please provide your API key:")

class CurrencyConverter():
	def __init__(self, URL = 'https://v6.exchangerate-api.com/v6/'):
		personal_url = URL + str(API_KEY) + '/latest/' + 'USD'
		self.data = requests.get(personal_url).json()
		self.currencies = self.data['conversion_rates']
	
	def convert(self, base_currency, target_currency, amount):
		initial_amount = amount
		# best to convert to USD if not in USD
		# because our base currency is USD
		
		if base_currency != 'USD' :
			amount /= self.currencies[base_currency]
		
		amount = round(amount * self.currencies[target_currency], 4)
		return amount

class CurrencyConverterUI(tk.Tk):
	def __init__(self, converter):
		tk.Tk.__init__(self)
		self.title('Currency Converter / Money Record')
		self.currency_converter = converter
		self.geometry("540x260")
		self.val = tk.IntVar()
		
		# date and title label
		self.intro_label = Label(self, text = 'Real-Time Currency Convertor / Money Record', fg = 'blue', relief = tk.RAISED, borderwidth = 3)
		self.intro_label.config(font = ('Courier', 15, 'bold'))

		self.date_label = Label(self, text=f"{dt.datetime.now():%a, %b %d %Y}", relief = tk.GROOVE, borderwidth = 5)
		self.intro_label.place(x = 10, y = 5)
		self.date_label.place(x = 210, y = 50)
		
		# Entry box
		valid = (self.register(self.restrictNumberOnly), '%d', '%P')
		# restrictNumberOnly function will restrict the user from entering invalid numbers in Amount field
		self.amount_field = Entry(self, bd = 3, relief = tk.RIDGE, justify = tk.CENTER, validate = 'key', validatecommand = valid)
		self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 17, borderwidth = 3)
		
		self.input_amount_label = Label(self, text = "Wallet:", fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 17, borderwidth = 3)
		self.input_amount = Entry(self, bd = 3, relief = tk.RIDGE, justify = tk.CENTER, validate = 'key', validatecommand = valid) 
		
		# dropdown
		self.base_currency_variable = StringVar(self)
		self.base_currency_variable.set("USD")
		self.target_currency_variable = StringVar(self)
		self.target_currency_variable.set("GBP")
		self.input_amount_variable = StringVar(self)
		self.input_amount_variable.set("USD")

		font = ("Courier", 12, "bold")
		self.option_add('*TCombobox * Listbox.font', font)
		self.base_currency_dropdown = ttk.Combobox(self, textvariable = self.base_currency_variable, values = list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
		self.target_currency_dropdown = ttk.Combobox(self, textvariable = self.target_currency_variable, values = list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
		self.input_amount_dropdown = ttk.Combobox(self, textvariable = self.input_amount_variable, values = list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 5, justify = tk.CENTER)		

		# placing
		self.base_currency_dropdown.place(x = 30, y = 120)
		self.amount_field.place(x = 36, y = 150)
		self.target_currency_dropdown.place(x = 340, y = 120)
		#self.converted_amount_field.place(x = 346, y = 150)
		self.converted_amount_field_label.place(x = 346, y = 150)

		self.input_amount_label.place(x = 90, y = 190)
		self.input_amount.place(x = 300, y = 190)

		# Convert Button
		self.convert_button = Button(self, text = "Convert", fg = 'white', bg = 'black', command = self.perform)
		self.convert_button.config(font = ('Courier', 10, 'bold'))
		self.convert_button.place(x = 225, y = 135)

		# Money In and Money Out Button
		self.moneyIn_button = Button(self, text = "Money In", fg = 'black', bg = 'green2', command = self.save_plus)
		self.moneyIn_button.config(font = ('Courier', 10, 'bold'))
		self.moneyIn_button.place(x = 180, y = 220)
		
		self.moneyOut_button = Button(self, text = "Money Out", fg = 'black', bg = 'red2', command = self.save_minus)
		self.moneyOut_button.config(font = ('Courier', 10, 'bold'))
		self.moneyOut_button.place(x = 260, y = 220)

		self.input_amount_dropdown.place(x = 223, y = 190)

		# Show report button
		self.offReport_button = Radiobutton(text = "Offline report", variable = self.val, value = 1, command = self.show_report)
		self.onReport_button = Radiobutton(text = "Online report", variable = self.val, value = 2, command = self.show_report)
		self.offReport_button.place(x = 20, y = 50)
		self.onReport_button.place(x = 20, y = 75)

	def perform(self):
		amount = float(self.amount_field.get())
		base_curr = self.base_currency_variable.get()
		target_curr = self.target_currency_variable.get()
		
		converted_amount = self.currency_converter.convert(base_curr, target_curr, amount)
		converted_amount = round(converted_amount, 2)
		
		self.converted_amount_field_label.config(text = str(converted_amount))

	def restrictNumberOnly(self, action, string):
		regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
		result = regex.match(string)
		return (string == "" or (string.count('.') <= 1 and result is not None))

	# saving deposits to file
	def save_plus(self):
		money = float(self.input_amount.get())
		base_currency = self.input_amount_variable.get()
		target_currency = 'USD'

		converted_money = self.currency_converter.convert(base_currency, target_currency, money)
		converted_money = round(converted_money, 2)
		
		with open('money_report.txt', 'a+') as file:
			result = file.write('Deposit: ' + '+' + str(money) + '(' + base_currency + ') | +' + str(converted_money) + '(' + 'USD' + ')\n')
			return result

		with open('web_money_report.html', 'a+') as ht_file:
			info = ht_file.write(result)
			return info
	
	# saving withdrawals to file
	def save_minus(self):
		money = float(self.input_amount.get())
		base_currency = self.input_amount_variable.get()
		target_currency = 'USD'

		converted_money = self.currency_converter.convert(base_currency, target_currency, money)
		converted_money = round(converted_money, 2)
		
		with open('money_report.txt', 'a+') as file:
			result = file.write('Withdrawal: ' + '-' + str(money) + '(' + base_currency + ') | -' + str(converted_money) + '(' + 'USD' + ')\n')
			return result
		
		with open('web_money_report.html', 'a+') as ht_file:
			info = ht_file.write(result)
			return info

	# show money report file
	def show_report(self):
		if self.val.get() == 1:
			os.system('notepad money_report.txt')
		elif self.val.get() == 2:
			content = open('money_report.txt', 'r')
			with open('web_money_report.html', 'w') as rep:
				for lines in content.readlines():
					if lines[0] == 'D':
						rep.write("<pre>" + '<span style="color:green">' + lines + '</span>' + "</pre>")
					elif lines[0] == 'W':
						rep.write("<pre>" + '<span style="color:red">' + lines + '</span>' + "</pre>")			

			webbrowser.open('C:/Users/user/web_money_report.html', new = 1)
			

#class DepositOrWithdrawal():
	
if __name__ == '__main__':
	converter = CurrencyConverter(URL = 'https://v6.exchangerate-api.com/v6/')

	CurrencyConverterUI(converter)
	mainloop()		
