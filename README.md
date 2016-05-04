# Tournament - Project

In this a simple Swiss-system Tournament Simulation for Udacity's full-stack [Nanodegree Program]. This application will simulate multiple rounds and validates the results of the given matches in the tournament.

## Description
This tournament support more than one tournament in the database and also prevent rematches between players. if theres is an odd number of players, is going to asign one player a "bye" and a player should not receive more than one bye in a tournament.

## Installation

Here are the tools you'll need to install to get it running:
* `Git`: If you don't already have Git installed, [download Git from git-scm.com]. Install the version for your operating system.
* `VirtualBox`: Is the software that actually runs the VM. [You can download it from virtualbox.org, here.] Install the version for your operating system.
* `Vagrant`: Is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.  [You can download it from vagrantup.com.] Install the version for your operating system.


### Use Git/GitHub to fetch the VM configuration
This GitHub repository contains all of the code you will need to run the tournament application.

1. Fork this repository (Click **Fork** in the top-right corner)
2. Copy the HTTPS method of your newly forked repository.
3. Then from the terminal run: `git clone PASTE_PATH_TO_REPO_HERE tournament`.

This will give you a directory named **tournament`**. Note: you will want to paste the path you copied from step 2 into `PASTE_PATH_TO_REPO_HERE`.

### Run the virtual machine
To Run the virtual machine follow the next steps:
* Using the terminal, change directory to tournament/vagrant (`cd tournament/vagrant`), then type `vagrant up` to launch your virtual machine.
* Once it is up and running, type `vagrant ssh` to log into it.
* One you log into, then explore the starter code for this project provided type `cd /vargrant/tournament` where you will see there are 3 files you have to work with on this project.
  ```
  Tournament/
  ├── tournament.py  - this file is used to provide access to database
  ├── tournament.sql - this file is used to set up the database schema
  └── tournament_test.py - this is written to test the implementation
  ```
### Create Database and Run application

* To build and access the database we run `psql` followed by `\i tournament.sql` then `\q`.
* Once database schema is created, run the series of tests defined in this test suite, run the program from the command line `$ python tournament_test.py`.You should be able to see the following output once all your tests have passed:
  ```
  vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py

  1 . deleted all information from database

  2. countPlayers() returns 0 after initial deletePlayers() execution.

  3. countPlayers() returns 1 after one player is registered.

  4. countPlayers() returns 2 after two players are registered.

  5. countPlayers() returns zero after registered players are deleted.

  5. Player records successfully deleted.

  6. Newly registered players appear in the standings with no matches.

  7. After a match, players have updated standings.

  8. After match deletion, player standings are properly reset.

  9. Matches are properly deleted.

  ---------Test Even pairings---------

  10. After one match, players with one win are properly paired.

  ---------Test Odd pairings---------

  13. After two matches, prevent a rematch and create another match

  14. After two matches, there are two byes.

  Success!  All tests pass!
  
  ```


[Nanodegree Program]: <https://www.udacity.com/nanodegree>
[download Git from git-scm.com]: <https://git-scm.com/downloads>
[You can download it from virtualbox.org, here.]: <https://www.virtualbox.org/wiki/Downloads>
[You can download it from vagrantup.com.]: <https://www.vagrantup.com/downloads.html>
[Python website]: <https://www.python.org/download/releases/2.7/>
