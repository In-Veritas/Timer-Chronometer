from threading import Event
import time as tm
import keyboard
import _thread



def time_entry(question : str, sixtycap : bool):
    global time, seconds, minutes, hours
    entry = False
    while entry == False:
        result = input(question)
        if result.isnumeric():
            entry = True
            if sixtycap == True:
                if int(result) >= 60:
                    entry = False
        if entry == False:
            print("Invalid entry!")
    if int(result) < 0:
        result = 0
    return int(result)
     
def time_change(time, seconds : int, minutes : int, hours : int, have_laps = False):
    global finish
    valid_entry = False
    while valid_entry == False:
        choice = input("Time Paused: " + time + "\n Press: \n1- Add time\n2- Remove time\n3- Continue\n4- Finish count\n")
        if not (choice == "1" or choice == "2" or choice == "3" or choice =="4"):
            print("INVALID ENTRY")
        else: 
            valid_entry = True
    if choice == "1":
        hours += time_entry("How many hours", False)
        minutes += time_entry("How many minutes", True)
        seconds += time_entry("How many seconds", True)
    elif choice == "2":
        hours -= time_entry("How many hours", False)
        minutes -= time_entry("How many minutes", True)
        seconds -= time_entry("How many seconds", True)
    elif choice == "3":
        pass
    elif choice == "4":
        hours = 0
        minutes = 0
        seconds = 0
        finish = True
    return [hours,minutes,seconds]

def timer():
    global time, seconds, minutes, hours, is_paused, pause_event
    hours = time_entry("How many hours", False)
    minutes = time_entry("How many minutes", True)
    seconds = time_entry("How many seconds", True)
    keyboard.on_press_key("p", pause)
    while not (seconds==0 and minutes==0 and hours==0):
        while pause_event.is_set():
            continue
        if (seconds==0 and minutes==0 and hours==0):
            print("TIME'S UP!")
            break
        time = '{:02d}:{:02d}:{:02d}'.format(hours,minutes, seconds)
        print(time)
        seconds -= 1
        if seconds <= -1:
            seconds = 59
            minutes -=1
            if minutes <= -1:
                minutes = 59
                hours -= 1
        if (seconds==0 and minutes==0 and hours==0):
                print("TIME: " + time)
                break
        tm.sleep(1)
    start()


def laps_counter(event : keyboard.KeyboardEvent):
    global laps, time, seconds, minutes, hours
    laps.append(time)
    seconds = 0
    minutes = 0
    hours = 0
    print("LAP: " + time)   
def chronometer():
    global time, seconds, minutes, hours, laps, finish
    finish = False
    laps = []
    hours = 0
    minutes = 0
    seconds = 0
    first_count = 0
    keyboard.on_press_key("p", pause)
    keyboard.on_press_key("l", laps_counter)
    while True:
        while pause_event.is_set():
            continue
        if finish == True:
            break
        time = '{:02d}:{:02d}:{:02d}'.format(hours,minutes, seconds)
        current_lap = time
        print(time)
        seconds += 1
        first_count += 1
        if seconds == 59:
            seconds = 0
            minutes +=1
            if minutes == 59:
                minutes = 0
                hours += 1
        tm.sleep(1)
    print("TOTAL LAPS:\n")
    secondsum = 0
    minutesum = 0
    hoursum = 0
    for lap in laps:
        timetype = 0
        newlap = lap.split(':')
        for number in newlap:
            if number[0] == "0":
                number = number[-1]
            if timetype == 2:
                secondsum += int(number)
            elif timetype == 1:
                minutesum += int(number)
            elif timetype == 0:
                hoursum += int(number)
            timetype += 1
        print(lap)
    print(current_lap + " (current)")
    print("TOTAL TIME: {:02d}:{:02d}:{:02d}".format(hoursum,minutesum, secondsum))
    start()

    
def start():
    global time, seconds, minutes, hours
    valid_entry = False
    while valid_entry == False:
        choice = input("Choose mode\n1- Chrono Mode\n2- Countdown Mode\n3- Allender Mode\n")
        if not (choice == "1" or choice == "2" or choice == "3"):
            print("Invalid Entry")
        else:
            choice = int(choice)
            valid_entry = True
    if choice == 1:
        print("CHRONOMODE\n Your cutting edge technology chronometer, press l to count a lap, and p to pause\n")
        print("Press r when ready")
        keyboard.wait("r")
        chronometer()
    elif choice == 2:
        print("COUNTDOWN MODE\n prepare to count down to the depths of hell, press p to pause\n")
        timer()
    elif choice == 3:
        return


def pause(event : keyboard.KeyboardEvent): 
    global time, seconds, minutes, hours, pause_event
    pause_event.set()
    current_lap = time
    newtime = time_change(time, seconds, minutes, hours)
    hours = newtime[0]
    minutes = newtime[1]
    seconds = newtime[2]
    time = '{:02d}:{:02d}:{:02d}'.format(hours,minutes, seconds)
    pause_event.clear()
time = ''
hours = None
minutes = None
seconds = None
is_paused = False
laps = None
finish = False
pause_event = Event()
start()