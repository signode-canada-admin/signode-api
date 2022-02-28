import json
from tabula import read_pdf, read_pdf_with_template
import PyPDF2
#you need to install the PyPDF2 library

#to do list
#display or log an error message if cannot get item number because it doesn't start with a #
#note: since we return stuff based on length of item_number_list, if we don't detect any item numbers cus of no #
#then item_number_list lenght is 0, thus nothing is returned. may have to change code to detect which lines don't have item number with #

#potential improvements to make algorithm faster
#cut down text_list even shorter by removing the end with unneccesary data or blank data;
#e.g. look for the "page" string e.g. page 3/5, or look for the "total" string so we cut all lists after that index

#warning/note
# this program relies on the item number having a '#' come before it. If '#' isn't present at all before the item number, fails to detect item number.

def read_loop(file):
    file_copy = open(file, 'rb')
    readpdf = PyPDF2.PdfFileReader(file_copy)
    totalpages = readpdf.numPages #number of pages in pdf
    quantity_leftover = -1#if a item's quantity is on this page and its item number is on the next page, save that quantity number to this
    #if there isn't any leftover on first page, default value is -1
    line_item_list = [] #holds quantity and item number pair info
    errors = [] #holds any error messages about what went wrong in code

    #for first pages, extract data using stream format. for all other pages, extract data using lattice format.
    #this is because stream consistently outputs a good format for first page, but all other pages have format messed up
    #for lattice, always cuts off the item description first character for first page, but all other pages consistently output a good format
    for i in range(1,totalpages+1):
        if i == 1:
            [line_items,quantity_leftover] = arcelor_mittal_data_stream(file = file, pages=i, quantity_leftover = quantity_leftover)
        else:
            [line_items,quantity_leftover] = arcelor_mittal_data_lattice(file = file, pages=i, quantity_leftover = quantity_leftover)
        line_item_list.extend(line_items)
    
    print("***************----------------------------************************")
    print("***************READ LOOP FILE IS DONE LOOPING************************")
    print("***************----------------------------************************")

    #these 2 lines grab the po from top left of first page
    json_data = read_pdf(file, pages=1, area=(52.906875, 5.328749999999999, 103.910625, 162.14625), stream=True, output_format="json")
    po = json_data[0]["data"][1][0]["text"]

    #all pdfs ive found either have all item numbers be present + have #'s before their numbers, or NONE have #. 
    #thus knowing which item number doesn't have a '#' seems irrelevant.
    if len(line_item_list) == 0:
        errors.append({"error": "# before prod. number not detected", "type": "product", "mssg": "# Not Found Error"})

    return{
        "po_no": po,
        "num_line_items": len(line_item_list),
        "line_items": line_item_list,
        "errors": errors,
    }

def arcelor_mittal_data_stream(file, pages, quantity_leftover, area=(1.903125, 0, 791.319375, 608.23875)):

    json_data = read_pdf(file, pages=f"{pages}", area=area, stream=True, output_format="json")
    rows_data = json_data[0]["data"]

    text_list = [row[0]["text"] for row in rows_data]
    header_index = 0 #will have index of the headers, "Poste Article" or "Item Material"
    item_count = 1

    #print(text_list)

    for index,text in enumerate(text_list):
        if text.find('Poste Article') != -1  or text.find('Item Material') != -1: 
            #important info is in the index after these headers 100% of time
            header_index = index
            #print("***************----------------------------************************")
            #print(header_index)
            text_list = text_list[header_index+1:]#cut information before the headers (also cuts off headers) from list
    
    quantity_list = []
    quantity_found = False #tells us to search for a # if quantity_found is True, doesnt search for # if false
    item_number_list = []
    
    print("***************----------------------------************************")
    #info.split(" ") is already a 1D array
    for index, info in enumerate(text_list):
        #print((info.split(" ")[0]))
        #print("item count: " + str(item_count))
        try:
            #checks if the first item in that list is equal to the item count, as each order has a 1,2,3, or 4, etc.
            #checks if there is not any leftover quantities from last page
            if int(info.split(" ")[0]) == item_count and quantity_leftover == -1:
                #print("below is info")
                #print (info.split(" "))
                for x, data in enumerate(info.split(" ")):
                    try:
                        data = int(data.split(',')[0])
                        #item, material, and quantity values should always be integers or aka only numbers, thus first error 
                        #should occur at the UM column. Thus we get index of UM column and subtract that by 1 to get index of quantity column
                        #note: all data in the arrays are initially strings
                        #note: sometimes quantities have ',' in them e.g. 117,000 is a quantity of 117. however, trying to parse
                        #117,000 into int gives error so code screws up. thus split at ',' and take [0] index cause main numbers come before ','
                        #this assumes that there will be no order that orders over a thousand quantity that uses ',' 
                    except:#if code goes to except, string was found
                        quantity_list.append(info.split(" ")[x-1].split(',')[0])#add quantity, split is done for same reasoning as above comment
                        item_count += 1
                        quantity_found = True       
                        break#stop for loop, aka stop searching for string
                    
        except:
            #couldn't parse info.split(" ")[0] into int, which we expect for strings we go over
            pass

        #if item quantity was already found and if the current string in list contains a '#'
        #quantity_found is to assure only the first # found after the item quantity index is used, so multiple irrelevant #'s found aren't added
        #print("info:" + str(info))
        if quantity_found and info.find("#") != -1:
            quantity_found = False
            item_number_list.append(text_list[index].split("#")[1].strip().split(",")[0].split(" ")[0].strip().split("--")[0])
            #for explanation of this split and strip code, check comments for (almost) the same line under the lattice function

    #print(item_number_list)
    #print(quantity_list)
    
    items = []

    #if there aren't equal amount of quantity's and item number's
    if len(item_number_list) != len(quantity_list):
        quantity_leftover = quantity_list[-1]
    else:
        quantity_leftover = -1
    
    for x in range(len(item_number_list)):
        items.append({
            "quantity": quantity_list[x],
            "product": item_number_list[x],
        })
    
    print(items)
    
    return items,quantity_leftover

def arcelor_mittal_data_lattice(file, pages, quantity_leftover, area=(100.865625, 12.000345000000006, 770.004375, 560.100345)):
#def arcelor_mittal_data2(file, pages, item_count, area=(334.569375, 9.89625, 785.990625, 605.19375)):

    json_data = read_pdf(file, pages=f"{pages}", area=area, lattice=True, output_format="json")
    text_list = [] # holds important info lists
    broken = False #lets us keep track if we found the "Poste" or 'Item' header index
    #if False, we haven't found it; if True we have it so stop searching for texts with "item" or 'Poste' in it
    
    #there are multiple lists under 'data' so we have to find the one that has the headers 'Poste' or 'Item', and use that one
    for info in json_data:
        for index,info2 in enumerate(info["data"]):
            for info3 in info2:
                if info3["text"].find('Poste') != -1 or info3["text"].find('Item') != -1: 
                    #search for 'Poste' or 'Item' header, so we know that the list after that in info2 is where key info starts
                    #print("found text")
                    text_list = info["data"][index+1:]
                    broken = True
                    break
            if broken:
                break
        if broken:
            break
    
    #print(text_list)
    
    quantity_list=[] #holds quantities of items
    item_number_list=[] #holds item numbers
    items = [] #holds final data returned, of pairs of quantities and the corresponding item number

    #if quantity from last page detected, add it to the start of quantity list
    if quantity_leftover != -1:
        quantity_list.append(quantity_leftover)
    
    for info in text_list:
        try:
            quantity_list.append(int(info[4]["text"].split(',')[0]))#only adds text to list if it successfully parses into an int
            #split ',' incase e.g. 117,000 for quantity 117; better explanation in stream func
        except:
            pass #isn't an integer, thus isn't a quantity; don't do anything
        
        #search the list texts for if they contain '#'
        if info[2]["text"].find("#") != -1:
            item_number_list.append(info[2]["text"].split("#")[1].strip().split(",")[0].split(" ")[0].strip().split("\r")[0].split("--")[0])
            #order numbers always come AFTER the '#' symbol, so we take the [1] index
            #strip any spaces to left and right of string; thus if any spaces were between the # and product number we remove those
            #order numbers come BEFORE commas or spaces, so we take the [0] index
            #strip again just in case to clean string format
            #\r is a enter/line gap, these come AFTER the order number so we take [0] index
            #sometimes product numbers have -- AFTER them, e.g. 567545--Bracket, so we take [0] index
        #print(item_number_list)

    #if there aren't equal amount of quantity's and item number's
    if len(item_number_list) != len(quantity_list):
        quantity_leftover = quantity_list[-1]
        print("leftover found: " + str(quantity_leftover))
        #print(quantity_list)
    else:
        quantity_leftover = -1 #say there is no leftover

    for x in range(len(item_number_list)):
        items.append({
            "quantity": quantity_list[x],
            "product": item_number_list[x],
        })
    
    print(items)

    return items,quantity_leftover

#below are working pdfs
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/PO-4500787334.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/PO-4500566393.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/PO-4500723182.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/PO-4500637531.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/PO-4500795262.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/PO-4500797947.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/PO-4500710418.pdf"))

#print(read_loop(file = r"C:\Users\0235898\test_Arcelor_Mittal_POs\New\PO-4500735314.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500737138.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500740330.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500741643.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500789934.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500790440.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500790495.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500790496.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500806151.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500819918.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500819960.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New/PO-4500812436.pdf"))

#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500721683.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500731611.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500731613.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500731614.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500733689.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500734135.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500736480.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500738127.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500740015.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500741095.pdf"))
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/New2/PO-4500748660.pdf"))

#problems below
#print(read_loop(file = r"C:/Users/0235898/test_Arcelor_Mittal_POs/Exceptions/PO-4500746034.pdf"))