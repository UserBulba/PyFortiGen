
#Start network.
network = "10.128.0.1"
#Output file.
newfile = open("shop_networks.txt", "w+")
#Split network address by dots.
adres = network.split(".")
#Start from correct addres, 127.
i = int(adres[1]) -1

#Define variables.
w = 0
adres_start = int(adres[1])
adres_stop = int(adres[2])

#loop from second octet to end of network range.
for x in range(int(i), 255):
    #loop for vLans.
    for y in range(0, 16):
        #Skip first record.
        if y != 0:
            #Add 16 to define next network.
            adres_stop = adres_stop + 16

        adres_xxx = adres_stop + 15

        for z in range(adres_stop, adres_xxx + 1):

            #Check the amount of addresses generated.
            if z % 16 == 0:
                print("\n")
                newfile.write("\n")

            print(str(10) + "." + str(adres_start) + "." + str(w) + "." + str(1) + "-" + (str(10) + "." + str(adres_start) + "." + str(w) + "." + str(240)))
            ## With end of scope :
            #newfile.write(str(10) + "." + str(adres_start) + "." + str(w) + "." + str(1) + "-" + (str(10) + "." + str(adres_start) + "." + str(w) + "." + str(240)) + ",")
            ## Addressation Gateway.
            newfile.write(str(10) + "." + str(adres_start) + "." + str(w) + "." + str(1) + ",")
            w = w + 1

#        print(str(10) + "." + str(adres_start) + "." + str(adres_stop) + "." + str(1) + "," + (str(10) + "." + str(adres_start) + "." + str(adres_xxx) + "." + str(240)))
#        newfile.write(str(10) + "." + str(adres_start) + "." + str(adres_stop) + "." + str(1) + "," + (str(10) + "." + str(adres_start) + "." + str(adres_xxx) + "." + str(240)) + "\n")

    #Clear variables and go to next second octet network.
    adres_stop = 0
    adres_start = adres_start + 1
    w = 0
