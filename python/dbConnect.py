import csv
from os import linesep

file = 'C:\\Users\\Dan\\Dev\\Python\\HappyHourCSV\\TheDomain.csv'

def openCSV(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_count = 0

        bars = []
        barsFoo = []

        # tempDict = {'name':'The Market'}

        # barsFoo.append({'name':'The Market', 'address':'319 Colorado St, Austin, TX 78701','city':'Austin', 'zipcode':'78759', 'phone':'(512) 472-6662', 'facebook':'https://www.facebook.com/TheMarketAustin/', 'website':'',
        #     'twitter':'https://twitter.com/TheMarketAustin', 'google':'', 'Monday':'''No Specials''', 'Tuesday':'''4-8pm 1/2 off Specialty Cocktails, $4 Jager, $4 Fireball
        #     $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Wednesday':'''$3  Local Beers, $4 Local Liquers
        #     $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Thursday':'''$2 Moonshine, $4 Kettle One, 1$ off all other liquer
        #     $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Friday':'''$2 Moonshine, $4 Kettle One, 1$ off all other liquer
        #     $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Saturday':'''4-8pm $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Sunday':'''No Specials''' })


        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                temp = queryCreationString(row)
                bars.append(temp)
                print(temp)

            line_count +=1
    for bar_item in bars:
            print(f'----------------- {bar_item}')



    # foo =  {'name':'The Market', 'address':'319 Colorado St, Austin, TX 78701','city':'Austin', 'zipcode':'78759', 'phone':'(512) 472-6662', 'facebook':'https://www.facebook.com/TheMarketAustin/', 'website':'',
    #     'twitter':'https://twitter.com/TheMarketAustin', 'google':'', 'Monday':'''No Specials''', 'Tuesday':'''4-8pm 1/2 off Specialty Cocktails, $4 Jager, $4 Fireball
    #     $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Wednesday':'''$3  Local Beers, $4 Local Liquers
    #     $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Thursday':'''$2 Moonshine, $4 Kettle One, 1$ off all other liquer
    #     $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Friday':'''$2 Moonshine, $4 Kettle One, 1$ off all other liquer
    #     $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Saturday':'''4-8pm $3.50 doms, $4.25 Imports, $4.50 Wells, $5 House Wine''', 'Sunday':'''No Specials'''}

    print("all done")

def queryCreationString(row):
    name = row[0]
    Monday = row[1]
    Tuesday = row[2]
    Wednesday = row[3]
    Thursday = row[4]
    Friday = row[4]
    Saturday = row[5]
    Sunday = row[6]
    OpenHours = row[7]
    phone = row[9]
    website = row[10]
    address = row[11]
    facebook = row[12]
    twitter = row[13]
    google = row[14]
    email = row[15]
    ourPageDONTNEED = row[16]
    theirWebsite = row[17]


    # bar_dict_item= f""" {{"name":'{name}', 'address':'{address}','city':'Austin', 'zipcode':'78759', 'phone':'{phone}', 'facebook':'{facebook}', 'website':'{theirWebsite}', 
    # 'twitter':'{twitter}', 'google':'{google}', 'Monday':'''{Monday}''', 'Tuesday':'''{Tuesday}''', 'Wednesday':'''{Wednesday}''', 'Thursday':'''{Thursday}''', 'Friday':'''{Friday}''', 'Saturday':'''{Saturday}''', 'Sunday':'''{Sunday}'''}} \n """
    bar_dict_item= f""" {{"name":'{name}', 'address':'{address}','city':'Austin', 'zipcode':'78759', 'phone':'{phone}', 'facebook':'{facebook}', 'website':'{theirWebsite}', 
    'twitter':'{twitter}', 'google':'{google}'}} \n """

    return bar_dict_item
    

if __name__ == "__main__":
    openCSV(file)
