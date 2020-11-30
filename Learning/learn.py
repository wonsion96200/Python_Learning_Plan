import re

content='''10.170.109.202: E11587835LSLDXIANWUJU> st cell
10.170.109.202: 
10.170.109.202: 201109-11:14:37 10.170.109.202 20.0c MSRBS_NODE_MODEL_20.Q2_453.28212.68_480e stopfile=/tmp/41993
10.170.109.202: ===================================================================================
10.170.109.202: Proxy  Adm State     Op. State     MO
10.170.109.202: ===================================================================================
10.170.109.202:   854  1 (UNLOCKED)  1 (ENABLED)   GNBDUFunction=1,NRCellDU=E11587835LSLDxianwuju_111
10.170.109.202:   855  1 (UNLOCKED)  1 (ENABLED)   GNBDUFunction=1,NRCellDU=E11587835LSLDxianwuju_112
10.170.109.202:   856  1 (UNLOCKED)  1 (ENABLED)   GNBDUFunction=1,NRCellDU=E11587835LSLDxianwuju_113
10.170.109.202: ===================================================================================
10.170.109.202: Total: 3 MOs'''

#findall方法

# state_list=re.findall('GNBDUFunction=1,NRCellDU=(.*?_\d\d\d)',content)
# print('cell name is {}'.format(state_list))

#re.S 忽略\n

# state_list1=re.findall('GNBDUFunction=1,NRCellDU=(.*?_\d\d\d)',content,re.S)
# print('cell name is {}'.format(state_list1))

#.*和.*?

# state_list1=re.findall('GNBDUFunction=1,NRCellDU=(.*_\d\d\d)',content,re.S)
# print('cell name is {}'.format(state_list1))

#search方法

# site_search=re.search('GNBDUFunction=1,NRCellDU=(.*?)_\d\d\d\n',content)
# print('site name is {}'.format(site_search.group(1)))
# print('site name is {}'.format(site_search.group()))
# print('site name is {}'.format(site_search.group(0)))

#findall方法2

state_list=re.findall('1 (.*?)  1 (.*?)   GNBDUFunction=1,NRCellDU=(.*?_\d\d\d)',content)
print('cell name is {}'.format(state_list))

#search方法2

site_search=re.search('1 (.*?)  1 (.*?)   GNBDUFunction=1,NRCellDU=(.*?_\d\d\d)',content)
print('site name is {}'.format(site_search.group(1)))
print('site name is {}'.format(site_search.group(2)))
print('site name is {}'.format(site_search.group(3)))
