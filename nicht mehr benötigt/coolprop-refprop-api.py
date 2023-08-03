from CoolProp.CoolProp import PropsSI as CPSI

# API Test
print(CPSI("T","P",101325,"Q",0,"HEOS::Water"))
print(CPSI("T","P",101325,"Q",0,"REFPROP::Water"))

# R1233ZD(E) issue
h=343258.91285678255
p=8.1*1e5

#print(CPSI("T", "P", p, "H", h, "HEOS::R1233ZD(E)"))
print(CPSI("T", "P", p, "H", h, "REFPROP::R1233ZD(E)"))



