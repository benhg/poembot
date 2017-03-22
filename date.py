
#code snippet to get today's date, open up corresponding poem file, and print
# for example, if it's April 4th, it will open and print 4.txt

import time                           
today= time.strftime("%m/%d/%Y")  
mm,dd,yyyy=today.split("/")
print dd  

myFile="allpoems/poems/"+dd+".txt"

## Open the file with read only permit
f = open(myFile)
## Read the first line 
line = f.readline()

## If the file is not empty keep reading line one at a time
## till the file is empty
while line:
    print line
    line = f.readline()
f.close()   