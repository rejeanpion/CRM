# basic structure of the game - you can make it as complex as you want

name = input("Hello! what is your name: ")
print("Welcome", name, "to this adventure!")

answer1 = input(
    "You come to a dirty road and it comes to an end. You can turn left or right. Which way would you like to go? ").lower()

if answer1 == "left":
    answer2 = input(
        "You come to a river, you can walk around it or swim accross? Type walk to walk around and swim to swim across: ").lower()
    if answer2 == "walk":
        print("You walked for many miles, ran out of water and you lost the game.")
    elif answer2 == "swim":
        print("You went into the river and got eaten by an alligator! You have lost.")
    else:
        print("You did not answer me correctly! You lose.")    
elif answer1 == "right":
    answer3 = input(
        "You come to a bridge, it looks wobbly, do you want to cross it or head back (cross/back)? ").lower()
    if answer3 == "back":
        print("You go back and get attack by a dog. You get very injured and die.")
    elif answer3 == "cross":
        answer4 = input("You cross the bridge and meet strangers. Do you talk to them (Yes/No)? ").lower()
        if answer4 == "yes":
            print("You talk to the strangers and they help you. You WIN!")
        elif answer4 == "no":
            print("You say no to the strangers and they are offended and kill you. You LOSE!")
        else:
            print("You did not answer me correctly! You lose.")
    else:
        print("You did not answer me correctly! You lose.")   
else:
    print("You did not answer me correctly! You lose.")
