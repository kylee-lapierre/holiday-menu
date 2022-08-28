from dataclasses import dataclass
from datetime import date, datetime
from bs4 import BeautifulSoup
from config import apiKey, locationKey, mainMenuKey
import json
import requests

# ---------------------
# Added these functions
#----------------------
def getAPI():
    file = open(apiKey, 'r')
    apikey = file.read()
    file.close()
    return apikey

def getLOC():
    file = open(locationKey, 'r')
    location = file.read()
    file.close()
    return location

def getMenu():
    global mainMenu
    file = open(mainMenuKey, 'r')
    mainMenu = file.read().splitlines()
    file.close()
    return mainMenu

def startUp():
    print("\nHoliday Management")
    print("="*len("Holiday Management"))

# ----------------------------------------
# Holiday class, added the lambda function
#-----------------------------------------
@dataclass
class Holiday:
    name: str
    date: date
    
    def __str__ (self):
        holiday = lambda inputName, inputDate: str(inputName + " (" + inputDate + ")")
        return holiday(self.name, self.date)
    
    def dictionaryAdd(inputName, inputDate):
        return dict({"name":inputName, "date":inputDate})
                     
# ------------------------------------------
# HolidayList class, added get HTML and JSON
# ------------------------------------------
class HolidayList:
    def __init__(self):
       self.innerHolidays = []
    
    def addHoliday(HolidayName, HolidayDate):
        dateAdded = 'n'
        while dateAdded != 'y':
            if {HolidayName:HolidayDate} not in innerHolidays:
                dateAdded = 'y'
                print(f"{HolidayName} has been added to the list.")
                innerHolidays.append(Holiday.dictionaryAdd(HolidayName, HolidayDate))
            else:
                print("That holiday has already been added.")
                choose = input("Would you like to try again? [y/n] ")
                if choose == 'n':
                    dateAdded = 'y'
                else:
                    HolidayName = input("Holiday: ")
                    HolidayDate = input("Date: ")

    def findHoliday(HolidayName, HolidayDate):
        for i in innerHolidays:
            if HolidayName in i.keys() and HolidayDate in i.values():
                get_holiday = Holiday(i["name"], i["date"]).__str__()
                return get_holiday
            else:
                print("\nThat holiday was not found.\nPlease try again.\n")

    def removeHoliday(HolidayName, HolidayDate):
        foundHoliday = 'n'
        while foundHoliday != 'y':
            try: 
                for i in innerHolidays:
                    if i == {"name":str(HolidayName), "date":str(HolidayDate)}:
                        foundHoliday = 'y'
                        innerHolidays.remove(i)
                        print(f"\nSuccess:\n{HolidayName} has been removed from the holiday list.")
                        return foundHoliday
            except:
                print("\nError:\nThat holiday was not found\nPlease try again.\n")
                HolidayName = input("Holiday name: ")
                HolidayDate = input(f"Date of {HolidayName}: ")
            else:
                print("\nError:\nThat holiday was not found.\nPlease try again.\n")
                HolidayName = input("Holiday name: ")
                HolidayDate = input(f"Date of {HolidayName}: ")

# ADDED TO READ IN HOLIDAY DATA
    def getHTML(url):
        response = requests.get(url)
        return response.text
    
# ADDED TO READ IN WEATHER DATA
    def getJSON(url):
        response = requests.get(url)
        return response.json()

    def read_json(filelocation):
        with open(filelocation, 'r') as file:
            givenHoliday = json.load(file)
        for i in givenHoliday["holidays"]:
            if i not in innerHolidays:
                HolidayList.addHoliday(i["name"], i["date"])
        return innerHolidays

    def save_to_json(filelocation):
        jsonList = []
        for i in innerHolidays:
            if i not in jsonList:
                jsonList.append({"holidays":{
                    "Name":i["name"], 
                    "Date": i["date"]
                }})
        with open(filelocation, 'w') as file:
            json.dump(jsonList, file, indent = 1)
        innerHolidays = []
        return innerHolidays
       
    def scrapeHolidays():
        for years in range(2020, 2025):
            url = BeautifulSoup(HolidayList.getHTML(f"https://www.timeanddate.com/holidays/us/{years}?hol=43119487"), "html.parser")
            dates = url.find("tbody").find_all("tr", attrs = {"class":"showrow"}) 
            for i in dates:
                if i not in innerHolidays:
                    innerHolidays.append(dict({
                        # Name of holiday
                        "name":list(i)[2].text,
                        # Date in YYYY-MM-DD format
                        "date":(datetime.strptime((list(i)[0].text + ', ' + str(years)), '%b %d, %Y').strftime('%Y-%m-%d')) 
                        }))
        return innerHolidays   

    def numHolidays():
        print(f"There are {len(innerHolidays)} holidays stored in the system.")
    
    def filter_holidays_by_week(yearNum, weekNum):
        global listHoliday
        holidays = filter(lambda i: date(int(i["date"][:4]), int(i["date"][5:7]), int(i["date"][8:])).isocalendar().week == int(weekNum) and int(i["date"][:4]) == int(yearNum), innerHolidays)
        listHoliday = list(holidays)
        return listHoliday

    def displayHolidaysInWeek(holidayList):
        global formatHolidays
        formatHolidays = []
        for i in holidayList:
            newHoliday = (Holiday(i["name"], i["date"])).__str__()
            formatHolidays.append(newHoliday)
        return formatHolidays
            
    def getWeather(weekNum, holidayList):
        global formatWeather
        dates = []
        for i in holidayList:
            if (date(int(i["date"][:4]), int(i["date"][5:7]), int(i["date"][8:])).isocalendar().week) == int(weekNum):
                dates.append(i["date"])
        weekNum = dates
        formatWeather = []
        try:
            for i in holidayList:
                if i["date"] in weekNum:
                    dates = i["date"]
                    weather = ((HolidayList.getJSON(f"http://api.weatherapi.com/v1/history.json?key={getAPI()}&q={getLOC()}&dt={dates}"))["forecast"]["forecastday"][0]["day"]["condition"]["text"])
                    formatWeather.append(weather)
        except:
            return formatWeather

    def viewCurrentWeek(inputYear):
        current_week = date.today().isocalendar().week
        HolidayList.filter_holidays_by_week(int(inputYear), current_week)
        HolidayList.displayHolidaysInWeek(listHoliday)
        if int(inputYear) <= int(date.today().year):
            week_weather = input("Would you like to see this week's weather? [y/n]: ")
            while week_weather.lower() != 'n' and week_weather.lower() != 'y':
                print("That is an invalid input, please try again. ")
            if week_weather.lower() == 'y':
                HolidayList.getWeather(current_week, listHoliday)
                for i in range(len(formatHolidays)):
                    print(f"{formatHolidays[i]} - {formatWeather[i]}")

    def exit_menu():
        if len(innerHolidays) == 0:
            choice = input("Are you sure you want to exit? [y/n] ")
            while (choice.lower() != 'n' and choice.lower() != 'y') or choice.isalpha() != True:
                print("That input is incorrect, Please try again.")
                choice = input("Are you sure you want to exit? [y/n] ")
        elif len(innerHolidays) > 0:
            print("Are you sure you want to exit?\nYour changes will be lost.")
            choice = input('[y/n] ')
            while (choice.lower() != 'n' and choice.lower() != 'y') or choice.isalpha() != True:
                print("That input is incorrect, Please try again.")
                choice = input("Are you sure you want to exit? [y/n] ")
        return choice

def main():
    global innerHolidays
    innerHolidays = HolidayList().innerHolidays
    HolidayList.read_json("pre-loaded-holidays.json")
    HolidayList.scrapeHolidays()
    startUp()
    HolidayList.numHolidays()
    choice = 'n'
    while choice != 'y':
        print('\n')
        getMenu()
        for line in mainMenu:
            print(line.format("="*len("Holiday Menu")))
        select = input("\nPlease select a menu: ")
        while select.isnumeric() != True:
            print("That selection is incorrect.\nPlease try again.\n")
            select = input("\nPlease select a menu: ")
        while int(select) not in range(1,6):
            print("That selection is incorrect.\nPlease try again.\n")
            select = input("\nPlease select a menu: ")
        select = int(select)
        if select == 1:
            print("\nAdd a Holiday")
            print("="*len("Add a Holiday"))
            inputName = input("Holiday: ")
            inputDate = input("Date: ")
            HolidayList.addHoliday(inputName, inputDate)
        elif select == 2:
            print("\nRemove a Holiday")
            print("="*len("Remove a Holiday"))
            searchName = input("Holiday name: ")
            searchDate = input(f"Date of {searchName}: ")
            HolidayList.removeHoliday(searchName, searchDate)
        elif select == 3:
            print("\nSaving Holiday List")
            print("="*len("Saving Holiday List"))
            answer = input("Are you sure you want to save your changes? [y/n]: ")
            while answer.lower() != "n" and answer.lower() != "y":
                print("That is an incorrect input, please try again.")
                answer = input("Are you sure you want to save your changes? [y/n]: ")
            if answer.lower() == 'n':
                print("Canceled:\nHoliday list file save cancelled.")
            elif answer.lower() == 'y':
                HolidayList.save_to_json('all-holidays.json')
                print("Succes:\nYour changes have been saved.")
        elif select == 4:
            print("\nView Holidays")
            print("="*len("View Holidays"))
            inputYear = input("Which year?: ")
            inputWeek = input("Which week? #[1-52, leave blank for current week]: ")
            if inputWeek == '':
                HolidayList.viewCurrentWeek(inputYear)
                for i in formatHolidays:
                    print(i)
            else:
                if int(inputYear) <= int(date.today().year) and int(inputWeek) <= int(date.today().isocalendar().week):
                    week_weather = input("Would you like to see this week's weather? [y/n]: ")
                    while week_weather.lower() != 'n' and week_weather.lower() != 'y':
                        print("That is an invalid input, please try again. ")
                    if week_weather.lower() == 'y':
                        holidays = HolidayList.filter_holidays_by_week(inputYear, inputWeek)
                        HolidayList.getWeather(inputWeek, holidays)
                        HolidayList.displayHolidaysInWeek(holidays)
                        for i in range(len(formatHolidays)):
                            print(f"{formatHolidays[i]} - {formatWeather[i]}")
                else:
                    holidays = HolidayList.filter_holidays_by_week(inputYear, inputWeek)
                    HolidayList.displayHolidaysInWeek(holidays)
                    for i in formatHolidays:
                        print(i)
        elif select == 5:
            print("\nExit")
            print("="*len("Exit"))
            choice = HolidayList.exit_menu()
            if choice.lower() == 'n':
                print("\n ----- Returning to main menu ----- \n")
            else:
                print("\nGoodbye!")

if __name__ == "__main__":
    main();