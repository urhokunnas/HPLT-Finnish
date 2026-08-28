import json

with open ("C:/Users/shkunn/Downloads/edu_output.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    edu_dictionary = {}
    for edu, value in file.items(): 
        edu_dictionary[edu] = {"IP": 0, "NA":0, "IN":0, "HI":0,
                               "ID":0, "MT":0, "LY":0,"SP":0,"OP": 0, "Hybrid": 0}
        for register, count in value["register"].items(): 
            register_list = register.split("-")
            if len(register_list) == 1:
                main_register = register_list[0] #if the register has only one component, that is the same as the main register
            else:
                capitalised_registers = []
                for reg in register_list:
                    if reg.isupper() == True:
                        capitalised_registers.append(reg)
                if len(capitalised_registers) == 1:
                    main_register = capitalised_registers[0]
                else:
                    main_register = "Hybrid"
            edu_dictionary[edu][main_register] += count

with open("C:/Users/shkunn/Documents/results/sorted/edu_charting.txt", "w") as f:
    for edu, regs in edu_dictionary.items():
        for reg, count in regs.items():
            f.write(f"{edu};{reg};{count}\n")