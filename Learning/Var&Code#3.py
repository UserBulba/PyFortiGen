workDays = [19,21,22,21,20,22]
months = ["I","II","III","IV","V","VI"]

monthDays = dict(zip(months,workDays))
print (monthDays)

for key in monthDays:
    print ("Key is", key, "Value is", monthDays[key])

for value in monthDays.values():
    print ("The value is", value)