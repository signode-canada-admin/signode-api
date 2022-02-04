from tabula import read_pdf, read_pdf_with_template
import os
import glob
import sys

def list_of_files(path, file_ending='*.pdf'):
    '''
    path = directory of files
    file_ending = type of files (default = ".pdf")
    '''
    return glob.glob(os.path.join(path, file_ending))

def enter_directory(path):
    '''
    path = directory to enter(must be r'str')
    '''
    try: 
        os.chdir(path)
    except OSError:       
        print("Entering the directory %s failed" % path)

def move_files(src, dst):
    '''
    src = path to file (.pdf)
    dst = new path to file (.pdf)
    '''
    try:
        os.replace(src, dst)
    except:
        os.rename(src, dst)

def srap_data_2(file, area=(0.3825, 0.765, 693.4725, 611.235) , pages=1):
    
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    
    rows_data = json_data[0]["data"]
    
    invoice_text = [row[2]["text"] for row in rows_data]
    invoice_no = invoice_text[2]

    address_text = [row[1]["text"] for row in rows_data]
    quantity_text = [row[1]["text"] for row in rows_data] 

    item_num_text = [row[0]["text"] for row in rows_data] 
    item_num_txt = [line.strip() for line in item_num_text[5:] if line != ""]
    item_num = item_num_txt[2:]
    line_items = []

    last_line= 'test'
    x = 0
    while last_line != 'Tool:':
        split_phrase = address_text[(8+x)].split(' ')
        last_line = split_phrase[0]
        x += 1
        
    ship_ad = address_text[8:(7+x)]
    ship_x = ship_ad[0].split(' ')
    ship_ad[0]= ''.join(ship_x[2:])

    quantity_txt = quantity_text[(11+x):]


    y = 0
    while last_line != 'Subtotal:':
        last_line = quantity_txt[(0+y)]
        y += 1
        
    quantity_full = quantity_txt[:(y-1)]
    quantity = [z[0] for z in quantity_full]


    for i in range(len(item_num)):
        item_num[i] = item_num[i].replace(",",".")
        line_items.append(
            {
                "quantity": quantity[i],
                "product" : item_num[i]
            }
        )

    return {
        "invoice_no": invoice_no,
        "num_line_items": len(line_items),
        "line_items" :line_items,
        "ship_to": ship_ad,
    }


try:
    print(srap_data_2(rf"{sys.argv[1]}"))  
except Exception as e:
    ret = {
        "success": "false",
        "ship_via": "",
        "po_no": "",
        "num_line_items": 0,
        "line_items": [],
        "error": "Unexpected error occured"
    }
    print(ret)

#print(srap_data_2(r"C:\Users\0235897\Documents\9889.pdf"))   
sys.stdout.flush()

