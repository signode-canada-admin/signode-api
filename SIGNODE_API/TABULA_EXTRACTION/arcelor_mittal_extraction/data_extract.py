from tabula import read_pdf, read_pdf_with_template

def arcelor_mittal_data(file, area=(84.11812499999999, 6.85125, 746.405625, 562.56375) , pages=1):

    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")

    cnt = 0
    rows_data = json_data[cnt]["data"]

    text_list = [row[0]["text"] for row in rows_data]
    po = text_list[0]
    header_index = 0 #will have index of the headers, Poste Article Quantité UM Taxe Prix Par UM

    print(text_list)

    for index,text in enumerate(text_list):
        if str(text) == 'Poste Article Quantité UM Taxe Prix Par UM' or str(text) == 'Item Material Quantity UM Tax Price Per UM': 
            #important info is in the index after these headers 100% of time
            header_index = index
            print("***************----------------------------************************")
            print(header_index)
            text_list = text_list[header_index+1:]#cut information before the headers (also cuts off headers) from list
    
    
    quantity_list = []
    item_count = 1 #keeps track of which item we are on
    info_index = 0 #grabs index of list with quantity
    item_number_list = []
    

    print("***************----------------------------************************")
    
    for index, info in enumerate(text_list):
        try:
            #checks if the first item in that list is equal to the item count, as each order has a 1,2,3, or 4, etc.
            if int(info.split(" ")[0]) == item_count:
                #length is 9 if material isn't blank
                if len(info.split(" ")) == 9:
                    quantity_list.append(info.split(" ")[2])#grabs quantity only
                    item_count += 1
                    item_number_list.append((text_list[index+1].split("#")[1]).split(",")[0].split(" ")[0].strip())
                    #order numbers always come right after the '#' symbol, so we take the [1] index
                    #order numbers come BEFORE commas or spaces, so we take the [0] index
                    pass
                #length is 8 if material is blank
                if len(info.split(" ")) == 8:
                    quantity_list.append(info.split(" ")[1])#grabs quantity only
                    item_count += 1
                    item_number_list.append((text_list[index+1].split("#")[1]).split(",")[0].split(" ")[0].strip())
                    
        except:
            #couldn't parse info.split(" ")[0] into int, which we expect for strings we go over
            pass
    
    print(item_number_list)
    print(quantity_list)
    
    items = []
    
    for x in range(len(quantity_list)):
        items.append({
            "quantity": quantity_list[x],
            "product": item_number_list[x],
        })
    
    return{
        "po_no": po,
        "num_line_items": item_count - 1,
        "line_items": items,
    }
    

#print(arcelor_mittal_data(file = r"C:\Users\0235898\OneDrive - Signode Industrial Group\Downloads\Arcelor_Mittal_multiline_POs\PO-4500777088.pdf"))
#print(arcelor_mittal_data(file = r"C:\Users\0235898\OneDrive - Signode Industrial Group\Downloads\Arcelor_Mittal_multiline_POs\PO-4500851218.pdf"))
print(arcelor_mittal_data(file = r"C:\Users\0235898\OneDrive - Signode Industrial Group\Downloads\4500872859.pdf"))