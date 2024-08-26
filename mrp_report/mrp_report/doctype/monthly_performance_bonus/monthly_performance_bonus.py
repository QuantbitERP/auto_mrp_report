# Copyright (c) 2024, vivek.kumbhar@erpdata.in and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MonthlyPerformanceBonus(Document):
	
	def before_save(self):
		total = 0
		for item in self.items:
			total += item.total_weightage
		if total != self.max_bonus:
			frappe.throw(f"Total Weightage (%) Should be Equal to Max Bonus %: Total Weightage = {total}, Max Bonus = {self.max_bonus}")
		if self.bonus_per > self.max_bonus:
			frappe.throw(f"Result Weightage (%) Should be less than or Equal to Max Bonus %: Result Weightage = {self.bonus_per}, Max Bonus = {self.max_bonus}")
   
	@frappe.whitelist()
	def bonus_calculate(self):
		self.calculated_bonus = self.bonus_per*(self.performance_bonus/100) if self.bonus_per and self.performance_bonus else 0
