workDays = [19,21,22,21,20,22]

print (workDays)
print (workDays[2])

enumeratedDays = list(enumerate(workDays))
print(enumeratedDays)

for pos, value in enumeratedDays:
    print ("Position ",pos, "Value", value)

months = ["I","II","III","IV","V","VI"]
monthsDays = zip(months,workDays)
print (list(monthsDays))

for m, d in monthsDays:
    print ("Month ",m, "days", d)

for pos, (m, d) in enumerate(zip(months, workDays)):
    print ("Position",pos, "month",m, "days",d)