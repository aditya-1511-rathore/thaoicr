import cv2 as cv
import os


import easyocr
reader = easyocr.Reader(['en'])
import re

def get_id(inputs):
    x = re.search(r"[0-9]\s[0-9][0-9][0-9][0-9]\s[0-9][0-9][0-9][0-9][0-9]\s[0-9][0-9]\s[0-9]", inputs)
    if x is not None:
        id = x.group()

    return id


def get_name(inputs):
    if "Name" in inputs:
        return inputs[inputs.index("Name")+1]
    if "name" in inputs:
        return inputs[inputs.index("name")+1]
    

def last_name(inputs):
    if "Last name" in inputs:
        return inputs[inputs.index("Last name")+1]
    if "last name" in inputs:
        return inputs[inputs.index("last name")+1]
    if "Last Name" in inputs:
        return inputs[inputs.index("Last Name")+1]
    if "last Name" in inputs:
        return inputs[inputs.index("last Name")+1]
    

def dates(inputs):
    dats = []
    regex_statement = r"[0-9][0-9]\s[a-z][a-z][a-z]\s[0-9][0-9][0-9][0-9]"
    for m in re.finditer(regex_statement,inputs):
        dats.append(inputs[int(m.start()): int(m.end())+1].replace(",","").replace(".",""))
        print(dats)
    
    return dats


def process_image(image_data, binary_conversion):
    status = False
    image_path = os.getcwd()+"\\ocr_images\\"+str(image_data)

    # load image to open to to make it binary with the set threshold
    if binary_conversion:
        # pass
        img = cv.imread(image_path)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(img_gray, 115, 255, cv.THRESH_BINARY)

        cv.imwrite(image_path, thresh) #save image to the same name and location 

    result = reader.readtext(image_path, detail = 0)

    res = " ".join(result).replace(".","").replace(",","").replace(":","")
    print(res)
    try:
        id_number = get_id(res)
    except:
        return "Error"
    
    try:
        name = get_name(result)
    except:
        name = "Unknown"

    try:
        last_name_value = last_name(result)
    except:
        last_name_value = "Unknown"
    try:
        new_dats = []
        months = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
        dats = dates(res.lower())
        for i in dats: 
            if i.split(" ")[1].lower() in months:
                new_dats.append(i)
        print(dats)
        if len(new_dats)==2:
            new_dats.append("")
            status = False
        elif len(new_dats) < 2:
            new_dats.append("")
            new_dats.append("")
            new_dats.append("")
            status = False
        else:
            status = True
    except:
        new_dats = ["","","","","",""]
        status = False
    result = {
        'id': id_number,
        'name': name,
        'last_name': last_name_value,
        'date-of-birth' : new_dats[0],
        'date-of-issue': new_dats[1],
        'date-of-expiry': new_dats[2],
        "status":status
    }

    return result, ""