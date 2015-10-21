# Scout Badges

Project to create an automatically updating list of all scout badges from [members.scouts.org.uk](members.scouts.org
.uk) in an open format (json)

Feel free to open an issue or create a pull request if this information is out of date, the script is broken, or you 
want more information from the site.

## format

{
    section:[
        [badgeName, imageUrl]
    ]
}

## pages that are parsed

* Cubs
    * Core Badges
    * Challenge Awards
    * Activity Badges
    * Staged Activity Badges
* Beavers
    * Core Badges
    * Challenge Badges
    * Activity Badges
    * Staged Activity Badges
* Scouts
    * Core Badges
    * Challenge Awards
    * Activity Badges
    * Staged Activity Badges
* Explorers
    * Core badges
    * Awards
    * Activity Badges
    * Staged Activity Badges
    
## Dependencies

* Python3.5
    * Beatifulsoup
    * certifi