#find alt
f = open("HC.log", "r")
linenumber = 1
start_linenumber = 0
end_lincenumber = 0
data = f.readlines()
for line in data:
    if "> alt" in line:
        start_linenumber = linenumber
#        print(start_linenumber)
    if "Critical" in line:
        end_lincenumber = linenumber
        print(line)
#        print(end_lincenumber)
        break
    if start_linenumber != 0 and end_lincenumber == 0:
        print(line)
    linenumber = linenumber + 1
f.close()