from tabula import read_pdf
import sys

# The most optimal area and #of pages to run tabula on
def srap_data_tools(file, area=(0.3825, 0.765, 693.4725, 611.235) , pages=1):
    
# Running the tabula function to get the data from the pdf
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")

# From the raw json_data file, isolate for only data portion
    rows_data = json_data[0]["data"]
    
# Assign the entire column of data that contains the neded specfic data 
# which will be later filtered down to only the specfic data 
    invoice_text = [row[2]["text"] for row in rows_data]
    invoice_no = invoice_text[2]

    address_text = [row[1]["text"] for row in rows_data]
    quantity_text = [row[1]["text"] for row in rows_data] 

    item_num_text = [row[0]["text"] for row in rows_data] 
    item_num_txt = [line.strip() for line in item_num_text[5:] if line != ""]
    item_num = item_num_txt[2:]
    line_items = []

# Get the data for the address in between the 8th line 
# and the line that starts with "Tool:" 
    last_line= 'test'
    x = 0
    while last_line != 'Tool:':
        split_phrase = address_text[(8+x)].split(' ')
        last_line = split_phrase[0]
        x += 1
        
# Seperate the "Sold to:" & "Ship to:" address
    ship_ad = address_text[8:(7+x)]
    ship_w = ship_ad[0].split('Canada ')
    ship_x = ship_ad[1].split('241')
    ship_ad[0]= ship_w[1]
    ship_ad[1]= ship_x[0]
    
    if x >= 4:
        ship_y = ship_ad[2].split('Markham')
        ship_ad[2]= ship_y[0]
        
        if x >= 5:
            ship_z = ship_ad[2].split('Canada')
            ship_ad[3]= ship_z[0]

# Take the values for quantity between three lines below the "Tool:" line 
# and above the "Subtotal:" line 
    quantity_txt = quantity_text[(11+x):]
    
    y = 0
    while last_line != 'Subtotal:':
        last_line = quantity_txt[(0+y)]
        y += 1
        
    quantity_full = quantity_txt[:(y-1)]
    quantity = [z[0] for z in quantity_full]

# Pair the quanity and product number together within the list of "line items"
    for i in range(len(item_num)):
        item_num[i] = item_num[i].replace(",",".")
        line_items.append(
            {
                "quantity": quantity[i],
                "product" : item_num[i]
            }
        )
# Return the Invoice number, total number of items, quanity 
# and product numbers of each item, & the company name/address
    return {
        "po_no": "No Charge",
        "num_line_items": len(line_items),
        "line_items" :line_items,
        # "ship_to": ship_ad,
        "ship_to": "ENTER SHIP_TO NUMBER",
        "ship_via": "ENTER SHIP VIA HERE",
    }

# Error checking
try:
    print(srap_data_tools(rf"{sys.argv[1]}"))  
except Exception as e:
    ret = {
        "success": "false",
        "ship_to": "",
        "po_no": "",
        "num_line_items": 0,
        "line_items": [],
        "error": "Unexpected error occured"
    }
    print(ret)

# To Test on local document uncomment this line and change the file path:    
#print(srap_data_tools(r"C:\Users\0235897\Documents\9889.pdf"))   

sys.stdout.flush()