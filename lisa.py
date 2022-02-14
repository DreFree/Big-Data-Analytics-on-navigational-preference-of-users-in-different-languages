import random 
print('Hello User, Welcome to Extrasensory Perception ESP')
print ('The program has randomly picked a color')
colorCount=0
for x in range (0,10):
    num=random.randint(0,4)
    userColor=(input('Please select one of the following colors that the computer has entered: red, green, yellow, orange or blue:'))
    if num==0:
        color='red'     
    else:
        if num==1:
            color='green'           
        else:
            if num==2:
                color ='blue'             
            else:
                if num==3: 
                    color='orange'                  
                else:
                    if num==4:
                        color='yellow'                
    print('The name of the randomly selected color is:',color)
    if userColor== color:
        colorCount=colorCount+1
print ('The number of times the user correctly guessed the selected color:',colorCount)