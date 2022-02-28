import pandas as pd
import numpy
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

# print(os.getenv('BASE_URL')) 

def insert_to_mongo(df):
    '''
    df -> # df = pd.read_excel("./EXCEL/Bunzul Product Cross Reference.xlsx")
    # cols = df.columns.tolist()
    {
        _id: Customer Product, (2)
        customer: Customer, (0)
        name: name, (1)
        Sig_prod: Signode Product, (3)
        desc: Descrip, (4)
        category: Category (5)
    }
    '''
    cluster = MongoClient("mongodb://127.0.0.1:27017/")
    db = cluster["signode"]
    collection_GF_EDI = db["BunzlProductCrossReference"]

    ret_list = []
    cols = df.columns.tolist()
    values_lst = df.values.tolist()
    for val in values_lst:
        query = {
            "_id": val[2],
            "customer": val[0],
            "name": val[1],
            "sig_prod": val[3],
            "desc": val[4],
            "category": val[5],
            "order_category": val[6]
        }
        ret_list.append(query)
        collection_GF_EDI.insert_one(query)
    return len(ret_list)


import urllib.request
import json
def db_find_one(id):
    # content = urllib.request.urlopen(fr"http://localhost:4000/api/edi/bunzlcrossref?_id={id}").read()
    content = urllib.request.urlopen(fr"{os.getenv('BASE_URL')}/edi/bunzlcrossref?_id={id}").read()
    result = json.loads(content)["data"]
    if result:
        return result[0]
    return result


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



def GENERAL_data(file, area=(215.3475, 42.4575, 666.6975, 147.2625) , pages=1):
    '''
    file: source file (type: .pdf)
    pages: 1, 2, .. 1-2,   "all"
    return PP first column data (type: .json)
    
    area (line items) => area = (215.3475, 42.075, 668.2275, 127.755) (default)
    area (ship Via) => area = (665.3007518796992, 42.94736842105263, 741.2255639097745, 406.4661654135338)
    '''
    
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    rows_text = [row[0]["text"] for row in rows_data]
    return rows_text


def GF_data(file, area=(278.0775, 0.3825, 724.0725, 187.8075) , pages="all"):
    '''
    file: source file (type: .pdf)
    pages: 1, 2, .. 1-2,   "all"
    return PP first column data (type: .json)
    
    area (line items) => area = (215.3475, 42.075, 668.2275, 127.755) (default)
    area (ship Via) => area = (665.3007518796992, 42.94736842105263, 741.2255639097745, 406.4661654135338)
    '''
    
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]
    rows_text = [[row[0]["text"], row[1]["text"]] for row in rows_data]
    return rows_text
    

def ret_index(data):
    '''
    data (type: []): first column of the table
    return (type: int): return index of the po_no
    
    item list starts at ret_index(data)+2
    '''
    if 'quantity' in data[0][0].lower() or 'stock' in data[0][1].lower():
        if "---" in data[1][0].lower():
            return 2
        return 1
    elif "---" in data[0][0].lower():
        return 1
    return 0



def get_only_line_items(rows):
    rows = rows[ret_index(rows):]
    ret_arr = []
    temp = []
    for row in rows:
        if "---" in row[0]:
            ret_arr.append(temp)
            temp = []
        else:
            temp.append(row)
    return ret_arr


def GF_data_multi_page(file, area=(278.0775, 0.3825, 724.0725, 187.8075) , pages="all"):
    '''
    file: source file (type: .pdf)
    pages: 1, 2, .. 1-2,   "all"
    return PP first column data (type: .json)
    
    area (line items) => area = (215.3475, 42.075, 668.2275, 127.755) (default)
    area (ship Via) => area = (665.3007518796992, 42.94736842105263, 741.2255639097745, 406.4661654135338)
    '''
    
    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    return json_data
#     rows_data = json_data[0]["data"]
#     rows_text = [[row[0]["text"], row[1]["text"]] for row in rows_data]
#     return rows_text

def ret_data(file):
    ret_array = []
    pages = GF_data_multi_page(file)
    cnt = 1
    for page in pages:
        rows_data = page["data"]
        rows_text = [[row[0]["text"], row[1]["text"], cnt] for row in rows_data]
        ret_array += get_only_line_items(rows_text)
        cnt+=1
    return ret_array
        
    


def return_GF_dict(data=None, ship_via=None, po_no=None):
    '''
    data (type: []): first two columns of the table func => get_only_line_items(GF_data())
    
    return (type: {}): 
    {
        "ship_via": Ship Via
        "po_no": 'Order No',
        "num_line_items": #,
        "line_items": [
            {"qty": #,
            "part_no": "str"}
        ], .....
    }
    '''
#     data = get_only_line_items(data)

    line_items = []
    consumables = []
    other = []
    parts = []
    errors = []
    for row in data:
        try:
            qty = row[0][0].split()[1]
        except IndexError as e:
            errors.append({"error": "sig quantity not found", "type": "quantity", "item": row[0], "mssg": repr(e)})
        
        try:
            id_data = db_find_one(row[0][1].split()[0])
            sig_prod = id_data["sig_prod"]
            category= id_data["order_category"]
        except IndexError as e:
            errors.append({"error": "sig product ref. not found", "type": "product", "item": row[0][1].split()[0], "mssg": "Index Error"})
            sig_prod = row[0][1].split()[0]
            category = "NOT FOUND"
        except TypeError as e:
            errors.append({"error": "sig product ref. not found", "type": "product", "item": row[0][1].split()[0], "mssg": "Type Error"})
            sig_prod = row[0][1].split()[0]
            category = "NOT FOUND"
            
        if category == "NOT FOUND":
            err_found = "true"
        else:
            err_found = "false"


        if (category == "consumables"):
            consumables.append({
            "quantity": qty,
            "product": sig_prod,
            "order_category": category,
            "page": row[0][-1],
            "error": err_found
        })

        elif (category == "parts"):
            parts.append({
            "quantity": qty,
            "product": sig_prod,
            "order_category": category,
            "page": row[0][-1],
            "error": err_found
        })

        else:
            other.append({
            "quantity": qty,
            "product": sig_prod,
            "order_category": category,
            "page": row[0][-1],
            "error": err_found
        })

        line_items.append({
            "quantity": qty,
            "product": sig_prod,
            "order_category": category,
            "page": row[0][-1],
            "error": err_found
        })
        
    
    return {
        "num_line_items": len(line_items),
        "line_items": line_items,
        "errors": errors,
        "ship_via": ship_via,
        "po_no": po_no,
        "consumables": consumables,
        "parts": parts,
        "other": other
    }

  
# def bunzul_industrial_extraction_algo(file):
#     return return_GF_dict(GF_data(file), GENERAL_data(file, area=(226.0575, 124.69500000000001, 277.3125, 279.99))[-1], GENERAL_data(file, area=(61.5825, 469.96498443603514, 101.3625, 611.4899844360351))[0].split('#')[1])
def bunzul_industrial_extraction_algo(file):
    return return_GF_dict(ret_data(file), GENERAL_data(file, area=(226.0575, 124.69500000000001, 277.3125, 279.99))[-1], GENERAL_data(file, area=(61.5825, 469.96498443603514, 101.3625, 611.4899844360351))[0].split('#')[1])


try:
    print(bunzul_industrial_extraction_algo(rf"{sys.argv[1]}"))
    # print(bunzul_industrial_extraction_algo(rf"http://localhost:4000/api/edi/bi/GF2"))
except Exception as e:
    ret = {
        "success": "false",
        "ship_via": "",
        "po_no": "",
        "num_line_items": 0,
        "line_items": [],
        "error": f"Unexpected error occured"
    }
    print(ret)

sys.stdout.flush()

# bunzul_industrial_extraction_algo(rf"http://localhost:4000/api/edi/bi/GF1")