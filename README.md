# Nokia homework
## Commands:
'l' - lists movies  
'l -v' - lists movies with additional info (you can use also use it after the switches)   
'l -t "insert regex for title" - lists movies with the right regex match   
'l -a "insert regex for actor name" - lists movies with the right regex match    
'l -t "insert regex for director name" - lists movies with the right regex match  
'l -la' - lists records in ascending order by movies length  
'l -ld' - lists records in descending order by movies length  
'a -p' - adds actor to the database    
'a -m' - adds movie to the database    
'd -p' - removes actor from the database except the actor is also a director

## Example inputs
```bash
# Add a movie (Make sure you have added the starring actors beforehand)
project.py a -m
Title: Star Wars 1.
Director: George Luca
We could not find 'George Luca', try again!
George Lucas
Released in: 1999
Length: 13
Bad input format (hh:mm), try again!
Length: 02:16
Starring: Liam Neeson
Nataliah Portman
This actor is not in the database, try again!
Natalie Portman  
exit
```

```bash
# Check results
project.py l -v
Pulp Fiction by Quentin Tarantino in 1994, 02:34
         Starring:
                 - John Travolta at age 40
                 - Uma Thurman at age 24
                 - Samuel L. Jackson at age 46
                 - Bruce Willis at age 39
                 - Ving Rhames at age 35
Star Wars 1. by George Lucas in 1999, 02:16
         Starring:
                 - Liam Neeson at age 47
                 - Natalie Portman at age 18
The Dark Knight by Christopher Nolan in 2008, 02:32
         Starring:
                 - Christian Bale at age 34
                 - Heath Ledger at age 29
                 - Aaron Eckhart at age 40
                 - Michael Caine at age 75
                 - Maggie Gyllenhaal at age 31
```

```bash
# Remove Natalie Portman
project.py d -p "Natalie Portman"
```

```bash
# Check result
project.py l -v
Pulp Fiction by Quentin Tarantino in 1994, 02:34
         Starring:
                 - John Travolta at age 40
                 - Uma Thurman at age 24
                 - Samuel L. Jackson at age 46
                 - Bruce Willis at age 39
                 - Ving Rhames at age 35
Star Wars 1. by George Lucas in 1999, 02:16
         Starring:
                 - Liam Neeson at age 47
The Dark Knight by Christopher Nolan in 2008, 02:32
         Starring:
                 - Christian Bale at age 34
                 - Heath Ledger at age 29
                 - Aaron Eckhart at age 40
                 - Michael Caine at age 75
                 - Maggie Gyllenhaal at age 31
```






