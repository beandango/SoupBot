# SoupBot
A bot I made that keeps track of my pet snake's health data! Her feedings, weight, poops, sheds, etc.

Her name is Soup :)

### Uses: 

discord.py, datetime, pymongo, QuickChart, Repl.it + UptimeRobot to keep it online, and of course, Python :P

# What does it do???
## Commands

`/feed [yes/no]`
Logs the date/time of a feeding, and whether or not she actually ate it

`/weight [grams]`
Logs the date of a weighing, and how many grams

`/shed [good/bad]`
Logs the date of a commpleted shed, and whether it was a good or bad shed

`/poop`
Logs the date of when a poop is found! Yayyyyyy!

`/show(feedings / weights / sheds / poops`
Shows the logged data for the respective category.

*Note: `/showfeedings` actually generates a piechart of her feeding data*
- You can also use `/showall` to show all of the data categories at once

`/clear(feeding / weight / shed / poop)data`
Clears all the data from the respective category (mainly for testing purposes)

## Settings

Within the discord server itself you can go to Server Settings -> Integrations -> and then hit the "manage" button next to SoupStats
to customize exactly which people/roles on your server can use each command.

I highly recommend making anything that clears or logs data Admin only, if you plan on using this code
for your own animal-tracking bot :p

## Now for some screenshots!

<img src="https://media.discordapp.net/attachments/1075213295318995086/1075464837397762129/Screen_Shot_2023-02-15_at_12.12.42_PM.png" width="500">
<img src="https://media.discordapp.net/attachments/1075213295318995086/1075465119234007090/Screen_Shot_2023-02-15_at_12.14.10_PM.png" width="500">
<img src="https://media.discordapp.net/attachments/1075213295318995086/1075465627025813635/Screen_Shot_2023-02-15_at_12.16.21_PM.png" width="500">
<img src="https://media.discordapp.net/attachments/1075213295318995086/1075465930135589014/Screen_Shot_2023-02-15_at_12.17.35_PM.png" width="500">
