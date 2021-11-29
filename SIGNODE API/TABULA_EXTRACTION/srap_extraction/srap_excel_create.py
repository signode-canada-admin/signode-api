from tabula import read_pdf, read_pdf_with_template
from openpyxl import Workbook
import os
import glob
from datetime import date
import sys
import json

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

def paths():
    code_path = os.getcwd()
    srap_path = rf"Y:\Pick Ticket Project\EDI\Srap" #store this to .env file
    pdf_files_path_srap = os.path.join(srap_path, "PDFS_SRAP")
    po_archive_path_srap = os.path.join(pdf_files_path_srap, "ARCHIVED_SRAP_POs")
    sx_excel_path_srap = os.path.join(srap_path, "EXCEL_SX_SRAP")
    return {
        "root": srap_path,
        "pdfs": pdf_files_path_srap,
        "pdfs_archive": po_archive_path_srap,
        "sx_excel": sx_excel_path_srap
    }

def get_active_sheet(excel_file_name):
    # open workbook Object
    # get active worksheet
    excel_file_extension = 'xls'
    filename = f'{date.today()}_{excel_file_name}.{excel_file_extension}'
    workbook = Workbook()
    sheet = workbook.active
    return (sheet, workbook, filename)





def print_line_items(PP_json, filename):
    '''
    pdf_file = "C:// ........ // PP.pdf",
    excel_file_name = "test"
    
    '''
    #get active sheet and file
    (sheet, workbook, excel_file) = get_active_sheet(filename)
    
    ##get_data_form_po
#     PP_json = premium_plus_extraction_algo(pdf_file)
    LINE_ITEMS = PP_json["line_items"]
    
    MIN_ROW = 9
    MAX_ROW = MIN_ROW + PP_json["num_line_items"] - 1
    MIN_COL = 1
    MAX_COL = 18
    column_name = {
        "product": 1,
        "description": 2,
        "quantity": 3,
        "unit": 4,
        "price": 5,
        "discount": 6,
        "disc_type": 7,
        "vendor": 8,
        "prod_line": 9,
        "prod_cat": 10, 
        "prod_cost": 11,
        "tie_type": 12,
        "tie_whse": 13,
        "drop_ship_option": 14,
        "print_option": 15,
        "required_option": 16,
        "subtotal_option": 17,
        "print_price_option": 18,
    }
    ##print_to_header
    cell_name = {
        "customer_name": "A1",
        "ship_to": "B1",
        "warehouse": "A2",
        "order_type": "B2",
        "customer_po": "A3",
        "ship_via": "A4",
        "terms": "B4",
        "requested_ship_date": "B5"
    }
    sheet[cell_name["customer_name"]] = 6183
    sheet[cell_name["ship_to"]] = '00'
    sheet[cell_name["warehouse"]] = "A001"
    sheet[cell_name["order_type"]] = "SO"
    sheet[cell_name["customer_po"]] = PP_json["po_no"]
    sheet[cell_name["ship_via"]] = PP_json["ship_via"]
    sheet[cell_name["terms"]] = "PPD"
#     sheet[cell_name["requested_ship_date"]] = "NET 30 DAYS"
    
    ##print_to_line_items
    quantity_query = column_name['quantity'] - 1
    product_query = column_name['product'] -1 
    for item, row in enumerate(sheet.iter_rows(min_row=MIN_ROW, max_row=MAX_ROW, min_col=MIN_COL, max_col=MAX_COL, values_only=False)):
        row[product_query].value = LINE_ITEMS[item]['product']
        row[quantity_query].value = LINE_ITEMS[item]['quantity']  
        
    
    #save the excel sheet
    workbook.save(filename=excel_file)
    return excel_file
    

def premium_plus_process(PP_json, filename):
    
    all_paths = paths()
#     pdfs = list_of_files(all_paths["pdfs"])
    # enter excel directory
    enter_directory(all_paths["sx_excel"])
#     if pdfs:
#         for pdf in pdfs:
    ret = print_line_items(PP_json, filename)
    # move pdf file to archive
    pdf = os.path.join(all_paths['pdfs'], f'{filename}.pdf')
    move_files(pdf, os.path.join(all_paths["pdfs_archive"], f'{filename}.pdf'))
    
    # finally enter code_path
    enter_directory(all_paths["code"])
    return ret


try:
    data = premium_plus_process(json.loads(sys.argv[1]), sys.argv[2])
    print({
        "data": data
    })
except Exception as e: 
    print({
        "success": "false",
        "error": "Unexpected Error occured"
    })
# print({"success": True})

# premium_plus_process({"line_items":[{"quantity":"1","product":"428756"},{"quantity":"3","product":"428789"},{"quantity":"7","product":"428811"},{"quantity":"4","product":"428873"},{"quantity":"1","product":"428895"},{"quantity":"2","product":"428909"},{"quantity":"1","product":"428920"}],"ship_via":"PUROLATOR","po_no":"411369","num_line_items":7}, '412711')

# premium_plus_process({"line_items":[{"quantity":"4","product":"2187.004"}],"ship_via":"UPS","po_no":"412749","num_line_items":1}, "412711")

sys.stdout.flush()