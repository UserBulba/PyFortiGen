# encoding UTF-8

network = "10.128.0.1"
newfile = open("shop_networks.txt", "w+")

adres = network.split(".")
i = int(adres[1]) -1

w = 0


adres_start = int(adres[1])
adres_stop = int(adres[2])

for x in range(int(i), 255):
    for y in range(0, 16):

        if y != 0:
            adres_stop = adres_stop + 16

        adres_xxx = adres_stop + 15

        for z in range(adres_stop, adres_xxx + 1):

            if z % 16 == 0:
                print("\n")
                newfile.write("\n")

            print(str(10) + "." + str(adres_start) + "." + str(w) + "." + str(1) + "-" + (str(10) + "." + str(adres_start) + "." + str(w) + "." + str(240)))
            newfile.write(str(10) + "." + str(adres_start) + "." + str(w) + "." + str(1) + "-" + (str(10) + "." + str(adres_start) + "." + str(w) + "." + str(240)) + ",")
            w = w + 1



#       print(str(10) + "." + str(adres_start) + "." + str(adres_stop) + "." + str(1) + "," + (str(10) + "." + str(adres_start) + "." + str(adres_xxx) + "." + str(240)))
#        newfile.write(str(10) + "." + str(adres_start) + "." + str(adres_stop) + "." + str(1) + "," + (str(10) + "." + str(adres_start) + "." + str(adres_xxx) + "." + str(240)) + "\n")

    adres_stop = 0
    adres_start = adres_start + 1
    w = 0
