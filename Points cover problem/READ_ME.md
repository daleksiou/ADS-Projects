The program call is done by executing: 

**python points_cover.py [-f] [-g] points_file**

### Examples
* python points_cover.py example_1.txt
  - Exit code

    (1, 1) (2, 2) (3, 3) (4, 4) (5, 5) (6, 6) 

    (7, 1) (8, 3) (9, 5)

    (7, 2) (8, 4) (9, 6)

    (10, 1) (10, 2) (10, 3)

    (11, 4) (11, 5) (11, 6)
    
* python points_cover.py -f -g example_2.txt
  - Exit code

    (1, 1) (10, 1)

    (2, 2) (10, 2)

    (3, 3) (10, 3)

    (4, 4) (11, 4)

    (5, 5) (11, 5)

    (6, 6) (11, 6)

    (7, 7) (12, 7)

    (8, 8) (12, 8)

    (9, 9) (12, 9)
