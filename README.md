# robots-scrapper-python

## Description
Script that scrapes robotics parameters from web-site and turns them in a right format.
Data was taken from [this](https://www.universal-robots.com/articles/ur/application-installation/dh-parameters-for-calculations-of-kinematics-and-dynamics/) web site and used for research purposes. 

## Technical details

### Format
Given web site contains tables with DH parameter (parameters that discribes robot's kinematics). 
One wants to scrap those parameters and turn to the certan format of Markdown table and Macaulay2 (programming language) code.
Wanted format:

```
  ROBOT'S NAME
  
  Parameters:
  
    [TABLE OF PARAMETERS]
    
  Macaulay2 code:
  
    [Macaulay2 code]
```

### Code
I used requests and bs4 libraries. 
One of the problems was to turn radians represented by string to float degrees (solved using fractions lib)

## Result
Script gives following results (for saving place reasons only first two robots are included):

  
    ## UR3e
    ### Parameters
    | i | r | d | alpha | theta |
    |---|---|---|-------|-------|
    | 1 |0.0|0.15185|90.0|0.0|
    | 2 |-0.24355|0.0|0.0|0.0|
    | 3 |-0.2132|0.0|0.0|0.0|
    | 4 |0.0|0.13105|90.0|0.0|
    | 5 |0.0|0.08535|-90.0|0.0|
    | 6 |0.0|0.0921|0.0|0.0|
    
    ### Macaulay2 code
    ```
    dof := 6;
    alpha := {90.0, 0.0, 0.0, 90.0, -90.0, 0.0};
    r := {0.0, -0.24355, -0.2132, 0.0, 0.0, 0.0};
    d := {0.15185, 0.0, 0.0, 0.13105, 0.08535, 0.0921};
    theta := {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    dhParams := {alpha, r, d, theta};
    ```
    
    ## UR5e
    ### Parameters
    | i | r | d | alpha | theta |
    |---|---|---|-------|-------|
    | 1 |0.0|0.1625|90.0|0.0|
    | 2 |-0.425|0.0|0.0|0.0|
    | 3 |-0.3922|0.0|0.0|0.0|
    | 4 |0.0|0.1333|90.0|0.0|
    | 5 |0.0|0.0997|-90.0|0.0|
    | 6 |0.0|0.0996|0.0|0.0|
    
    ### Macaulay2 code
    ```
    dof := 6;
    alpha := {90.0, 0.0, 0.0, 90.0, -90.0, 0.0};
    r := {0.0, -0.425, -0.3922, 0.0, 0.0, 0.0};
    d := {0.1625, 0.0, 0.0, 0.1333, 0.0997, 0.0996};
    theta := {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    dhParams := {alpha, r, d, theta};
    ```


