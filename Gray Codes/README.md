The program call is done by executing: 

**python beckett_gray.py [-a | -b | -u | -c | -p] [-r] [-f] [-m] number_of_bits**

### Examples
* python beckett_gray.py -u 3
  - Exit code

    U 0102101
    
* python beckett_gray.py -a 3
  - Exit code

    C 01020102  
    P 0102101  
    C 0121012
    
* python beckett_gray.py -u -f -m 3
  - Exit code

    U 000 001 011 010 110 100 101 111  
    U 0102101         
    0 1 1 0 0 0 1 1   
    0 0 1 1 1 0 0 1  
    0 0 0 0 1 1 1 1  
