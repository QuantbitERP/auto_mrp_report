# Copyright (c) 2024, vivek.kumbhar@erpdata.in and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import calendar
import datetime
from frappe import _
class OTMonthlySheet(Document):
	
	@frappe.whitelist()
	def get_salary_comp(self):
		for i in self.get("items"):
			salary_assignment = frappe.get_value("Salary Structure Assignment",{"employee":i.employee},"salary_structure")
			if salary_assignment:
				salary_comp = frappe.get_all("Salary Detail",{"parent":salary_assignment},["abbr","amount"])
				for j in salary_comp:
					if j.abbr == "B":
						i.b = j.amount
					elif j.abbr == "HRA":
						i.hra = j.amount 
					elif j.abbr == "DA":
						i.da = j.amount 
					elif j.abbr == "LA":
						i.la = j.amount 
					elif j.abbr == "CA":
						i.ca = j.amount 
     
	@frappe.whitelist()
	def get_month_dates(self, input_date):
		selected_date = str(input_date)
		date_li = selected_date.split("-")
		year = int(date_li[0])
		month_num = int(date_li[1])
		num_days_in_month = calendar.monthrange(year, month_num)[1]
		start_date = datetime.datetime(year, month_num, 1).date()
		end_date = datetime.datetime(year, month_num, num_days_in_month).date()
		date_li = str(start_date).split("-")
		self.year = date_li[0]
		month_num = int(date_li[1])
		self.month = _(calendar.month_name[month_num])
		self.from_date = start_date
		self.to_date = end_date
		self.monthdays = (end_date - start_date).days + 1
  
	@frappe.whitelist()
	def overtime_calculate(self):
		for i in self.get("items"):
			total_salary = 0
			if i.ot_hrs:
				total_salary = i.b + i.hra + i.da + i.la + i.ca
				per_day = total_salary /self.monthdays
				per_hr = per_day/8
				i.ot_amount = round((2*per_hr*i.ot_hrs),2)
			
    
	def before_save(self):
		for i in self.get("items"):
			i.from_date = self.from_date
			i.to_date = self.to_date
        