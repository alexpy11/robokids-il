## Synopsis

Lake is a fun project to help teach kids python. 
Lake.py is the server and the students write their-own clients, based on the 'stupidFish.py' template.

When the system runs, the lake shows every fish swimming.

## Motivation

Beginners learn to examine pre-existing data-strctures and write simple code that controls their own fish. 
More advanced students create swarms of fish and/or reverse the communication protocol. 
Fun for everyone !

## How To Start

On command prompt, run the 'lake.py' server. At another command promp run the 'stupidFish.py' client.
This will cause your fish to swim in the lake. Modify the client to make the fish smarter and master the challanges.
See the "API Reference" section for farther details


## Installation

Server computer dependencies:
- pyhton 2.7.x
- The twisted package
- The pygame package

Client computer dependencis:
- pyhton 2.7.x
- The twisted package

On a recent Ubuntu/Debian system, do:
    `apt-get install python-pygame python-twisted`

## API Reference

- Run one instance of the 'lake.py' server. 
Multiple fish might connect to the server

- One time tasks for each student:
  - Make your own copy of the template 'stupidFish.py'
  - Modify the fish name. 
  - If the fish runs on a different computer, modify the IP to be that of the computer running lake.py.  
- Meeting the challanges:
  - Begginers need to understand and modify only the 'getNextPos' function. More advanced students can examine and modify the rest of the client code.
  - Specifically, the student modifies the 'getNextPos' function to return the deltaX, deltaY (movenent of the fish), after examining the information received from the server
  - See 'challanges.txt' for description of the targets.
  - Once a challange is completed, the lake automatically moves to the next mission.

## Tests

Tested on both windows XP, Windows 7 and Ubuntu 14.04. 
Probably will run on any system w/Python and the needed packages

## Need to be done
- Possible next missions: 
  - Search for feed locations
  - periodical feed
  - 'strangle' another fish by being on two sides of it ?
  - Shoot another fish ? 
- Check spelling/langauge
