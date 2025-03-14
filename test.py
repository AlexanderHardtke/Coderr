import re
string="Max Mustermann"


first =  re.split('(?=[A-Z])', string)
print(first[0])