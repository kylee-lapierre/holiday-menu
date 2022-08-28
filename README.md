# Holiday Menu File! # 

Use this code to see the dates for holidays from January 1, 2020 to December 31, 2024! 
The main file with all the code is within HolidayMenu.py and the given holidays are within pre-loaded-holidays.json. 

## Features 
* Presents the user with a list of holidays taht are added then shows menu for adding a holiday, removing a holiday, viewing holidays, saving the holiday list, and then exiting the menu.
    * When adding a holiday, it requires the holiday name and date.
    * When removing a holiday, it requires the holiday name and date. If the name or date don't match up, then it will re-prompt for the correct name and date. 
    * When viewing holidays, it requires the year, week number, and (if possible) if you want to see the weather for those holidays as well. 
        * If the week is left blank, it will print out all holidays related to the current week number for any year from 2020 to 2024.
    * When saving the holidays, it will create a new json file with all holidays from January 1, 2020 to December 31, 2024. 
    * When exiting, it will prompt you if there are 
* Prints holiday names and dates for a chosen year from 2020 to 2024 and a chosen week with weather information for that day, if chosen. 
* Includes weather condition for any holiday before current day, unable to get weather conditions for future.
    * Takes in a year, week, and if you would like to see the weather (if possible) then prints out each holiday on its own line.
