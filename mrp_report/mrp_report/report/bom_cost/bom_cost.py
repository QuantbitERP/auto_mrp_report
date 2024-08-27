# Copyright (c) 2024, vivek.kumbhar@erpdata.in and contributors
# For license information, please see license.txt

import frappe
from collections import defaultdict 

def execute(filters=None):
        columns, data = [], []
        columns = get_columns()
        data = get_data(filters)
        return columns, data 
 
def get_columns():
    return[
        {
            "fieldname" : "bom",
            "fieldtype" : "Link",
            "options": "BOM",
            "label" : "BOM Id",
            "width":180
        },
        {
            "fieldname" : "idx",
            "fieldtype" : "Data",
            "label" : "Sr No."
        },  
        {
            "fieldname" : "item_code",
            "fieldtype" : "Data",
            # "options" : "Item",
            "label" : "Main Item",
            "width":120
        },
        {
            "fieldname" : "description",
            "fieldtype" : "Data",
            "label" : "Item Description",
            "width":450
        },
        {
            "fieldname" : "uom",
            "fieldtype" : "Data",
            "label" : "UOM"
        },      
        {
            "fieldname" : "qty",
            "fieldtype" : "Data",
            "label" : "BOM Quantity",
            # "precision": 2,
            "width":120
        },
        {
            "fieldname" : "customers_item_code",
            "fieldtype" : "Data",
            "label" : "Customers Item Code",
            # "precision": 2,
            "align":"right",
            "width":200
        },
        {
            "fieldname" : "rate",
            "fieldtype" : "Data",
            "label" : "Item Rate",
            # "precision": 2,
            "align":"right",
            "width":200
        },
        {
            "fieldname" : "amount",
            "fieldtype" : "Data",
            "label" : "Item Value",
            # "precision": 2,
            "align":"right",
            "width":120
        },      
    ] 
 
def add_condition(condition_list, params_list, condition, param_value):
    if param_value:
        condition_list.append(condition)
        params_list.append(param_value) 
        
def get_data(filters):
    BOM = filters.get("bom")
    
    conditions = []
    params = [BOM]  

    sql_query = """
                    SELECT 
                        x.bom AS 'bom',
                        CONCAT(x.idx, '.', x.row_number) AS 'idx',
                        x.item_code AS 'item_code',
                        x.description AS 'description',
                        x.uom AS 'uom',
                        FORMAT(x.qty, 2) AS 'qty',
                        x.citem AS 'customers_item_code',
                        FORMAT(x.rate, 2) AS 'rate',
                        FORMAT(x.amount, 2) AS 'amount' 
                    FROM 
                        (
                            SELECT 
                                x.name AS bom,0 AS idx,x.item 'item_code',x.item_name 'description',x.uom,x.quantity 'qty',0 AS rate,
                                i.customer_code AS citem,x.total_cost 'amount',0 AS row_number 
                            FROM `tabBOM` x
                            left join 
                            `tabItem` i on x.item = i.name
                            WHERE x.name  = %(bom)s
                            
                            UNION
                            
                            SELECT DISTINCT
                                parent AS bom, idx, item_code, description,uom, qty,rate,customers_item_code as citem,amount,0 AS row_number
                            FROM`tabBOM Item`
                            WHERE parent  = %(bom)s
                            
                            UNION
                            
                            SELECT 
                                row.parent AS bom,row.idx,item.item_code,item.description,
                                COALESCE(item.uom, item.stock_uom) AS uom,item.qty,
                                item.rate,item.customers_item_code as citem,
                                item.amount,ROW_NUMBER() OVER (PARTITION BY row.idx ORDER BY row.idx) AS row_number
                            FROM
                                `tabBOM Item` AS row
                            JOIN
                                `tabBOM Item` AS item ON row.bom_no = item.parent 
                            WHERE row.parent  = %(bom)s
                        ) x 
                """
    if conditions:
        sql_query += " AND " + " AND ".join(conditions)

    sql_query += "ORDER BY x.idx"   

    data = frappe.db.sql(sql_query, {"bom": BOM}, as_dict=True)


    # Step 1: Find the smallest idx value in the entire dataset
    min_idx_value = float('inf')

    for d in data:
        try:
            idx_value = float(d['idx'])
            if idx_value < min_idx_value:
                min_idx_value = idx_value
        except (ValueError, TypeError):
            continue

    # Step 2: Group entries by integer part of idx and keep track of all idx values
    groups = defaultdict(list)

    for d in data:
        try:
            idx_value = float(d['idx'])
            int_part = int(idx_value)
            groups[int_part].append(idx_value)
        except (ValueError, TypeError):
            continue

    # Step 3: Identify base idx values with subsequent entries
    bold_values = set()
    for int_part, values in groups.items():
        base_value = float(int_part)
        if any(value > base_value for value in values):
            bold_values.add(base_value)

    # Step 4: Apply bold formatting

    for d in data:
        try:
            idx_value = float(d['idx'])
            int_part = int(idx_value)
            if idx_value == min_idx_value or int_part in bold_values and idx_value == float(int_part):
                d['item_code'] = f"<b>{d['item_code']}</b>"
                d['description'] = f"<b>{d['description']}</b>"
                        
        except (ValueError, TypeError):
            continue    


    # for d in data:
    #   try:
    #       idx_value = float(d['idx'])
    #       int_part = int(idx_value)
    #       if idx_value == min_idx_value or int_part in bold_values and idx_value == float(int_part):
    #           d['item_code'] = f"<b>{d['item_code']}</b>"
    #           d['description'] = f"<b>{d['description']}</b>"
                        
    #   except (ValueError, TypeError):
    #       continue


    # For all rows bold
    # for d in data:
    #   try:
    #       idx_value = float(d['idx'])
    #       frappe.msgprint(str(idx_value))
    #       if idx_value.is_integer():
    #           d['item_code'] = f"<b>{d['item_code']}</b>" 
    #           d['description'] = f"<b>{d['description']}</b>" 
            
    #   except (ValueError, TypeError):
    #       continue
    
    # frappe.msgprint(str(data))

    # data.append({'bom':"TOTAL",'qty':sum(i['qty'] if i['qty'] else 0 for i in data),'rate':sum(i['rate'] if i['rate'] else 0 for i in data), 'amount':sum(i['rate'] if i['rate'] else 0 for i in data)})

    data.append({})

    temp = append_costing_data(data, filters)

    for key,values in temp[0].items():
        dict = {}             

        dict['rate'] = key  
        dict['amount'] = "₹ {:.2f}".format(values)

        dict[key] = values
        if key == 'Raw Material Cost':
            data.append({})
        if key == 'Total Cost (INR)':
            data.append({})
        data.append(dict)

    return data

def append_costing_data(data, filters):
    BOM = filters.get("bom")
    sql_query = """
        SELECT 
            raw_material_cost AS "Material Cost", 
            custom_miscellaneous_cost AS "Miscellaneous Cost", 
            custom_consumable_cost AS "Consumable Cost",
            (raw_material_cost + custom_miscellaneous_cost + custom_consumable_cost) AS "Raw Material Cost",
            custom_transport_cost AS "Transport Cost",
            custom_packing_forwarding AS "Packing Forwarding", 
            custom_labour_production AS "Labour Production", 
            custom_labour_quality AS "Labour Quality",             
            total_cost AS "Total Cost (INR)"        
        FROM 
            `tabBOM`
        WHERE 
            name = %(bom)s        
    """
    costing_data = frappe.db.sql(sql_query, {"bom": BOM}, as_dict=True)
    
    # Add blank row after "Consumable Cost"
    updated_costing_data = []
    for row in costing_data:
        updated_costing_data.append(row)
        # Insert a blank row after the current row
        blank_row = {}
        updated_costing_data.append(blank_row)
    
    return updated_costing_data

def print_bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    print(f"{bold_start}{text}{bold_end}")

# Adding the dictionary to the list
data = []
data.append({'bom': "TOTAL"})

# Use the custom print function
print_bold(data[0]['bom'])