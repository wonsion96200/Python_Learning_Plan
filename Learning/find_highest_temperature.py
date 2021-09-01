

with open("TOL-Power_Radiolog_30M.log", "r") as fileRead:
    power_log = fileRead.readlines()
    fileRead.close()

line_number = 0
radio1 = {}
radio2 = {}
radio3 = {}
rop1 = rop2 = rop3 = 1

for line in power_log:
    if "coli>/fruacc/lhsh BXP_2048 ts r" in line:
        for i in range(1, 27):
            radio1.setdefault(rop1, []).append(power_log[line_number + i].split()[3])
        rop1 += 1

    if "coli>/fruacc/lhsh BXP_2049 ts r" in line:
        for i in range(1, 27):
            radio2.setdefault(rop2, []).append(power_log[line_number + i].split()[3])
        rop2 += 1

    if "coli>/fruacc/lhsh BXP_2050 ts r" in line:
        for i in range(1, 27):
            radio3.setdefault(rop3, []).append(power_log[line_number + i].split()[3])
        rop3 += 1
    line_number += 1

# print(radio1.get(1))
for key, value in radio1.items():
    radio1[key] = max(radio1[key])

for key, value in radio2.items():
    radio2[key] = max(radio2[key])

for key, value in radio3.items():
    radio3[key] = max(radio3[key])

# print(radio1.get(1))
# # radio1.update(radio2)
# print(radio1.get(1))
i = 1
while i <= len(radio1):
    print("rop" + str(i), radio1.get(i), radio2.get(i), radio3.get(i))
    i += 1
