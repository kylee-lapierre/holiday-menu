# Holiday Menu File! # 

Use this code to see the dates for holidays from January 1, 2020 to December 31, 2024! 
The main file with all the code is within HolidayMenu.py and the given holidays are within pre-loaded-holidays.json. 

## Modules and Python Version
* Modules:
   * imported dataclass from dataclasses
   * imported date and datetime from datetime
   * imported BeautifulSoup from bs4
   * imported json
   * imported requests
* Python version: 3.9.12

## Features 
* Presents the user with a list of holidays that are added then shows a menu for adding or removing a holiday, viewing holidays, saving the holiday list, and then exiting the menu.
    * When adding or removing, it requires the holiday name and date.
         * If the name or date don't match up when removing a holiday, then it will re-prompt for the correct name and date. 
    * When viewing holidays, it requires the year, week number, and (if possible) the weather condition for the holidays within that week. 
         * If the week is left blank, it will print out all holidays related to the current week number for any year from 2020 to 2024.
         * No weather conditions are given for any holidays after current week.
    * When saving the holidays, it will create a new json file with all holidays from January 1, 2020 to December 31, 2024. 
    * When exiting, it will ask if you are sure you want to exit if there are unsaved changes or will ask if you want to exit.
* Prints holiday names and dates for a chosen year from 2020 to 2024 and a chosen week with weather information if the chosen date is before current day, unable to get weather conditions for future.

## Have fun!
