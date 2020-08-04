from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import os
import time
import datetime

# Courses definition file
COURSES_CONFIG_PATH = os.path.expanduser("~/.config/classbar/courses.yml")

# Exit program if no config
if not os.path.exists(COURSES_CONFIG_PATH):
    print("No CONFIG")
    exit(0)

# Determine the current time and day
time = int(time.strftime('%H%M'))
# time = 1045
day = datetime.datetime.today().weekday() + 1

# Load the config file
courses = load(open(COURSES_CONFIG_PATH, "r"), Loader=Loader)

# Find the current course
current_course = None
next_course = None


# Look for the current course
for course in courses:
    # Make sure this is a valid day
    if day in courses[course]["days"]:
        # Check if it is the correct time
        if courses[course]["start"] <= time and time <= courses[course]["end"]:
            current_course = courses[course]
            break


# Look for the next course
for course in courses:
    # Make sure this is a valid day
    if day in courses[course]["days"] and time <= courses[course]["start"]:
        next_course = courses[course]
        break

# Handle no current class
if current_course == None and next_course != None:

    # Calculate timestr (we have to do some string magic to get time data back from ints)
    nhr = int(next_course["start"]  / 100)
    nm = int(str(next_course["start"])[-2:])
    _chr = int(time / 100)
    cm = int(str(time)[-2:])

    # Create a "now" and "next" datetime
    now = datetime.datetime(year=2000,month=1,day=1,hour=_chr, minute=cm)
    _next = datetime.datetime(year=2000, month=1, day=1, hour=nhr, minute=nm)
    dt:datetime.timedelta = (_next - now)

    t_str = f"in {int(dt.seconds / 3600)}:{int(dt.seconds / 60)}h"

    # Calculate roomstr
    room = next_course.get("room", "")
    if room:
        room_str = f"in room {room}"
    else:
        room_str = ""

    print("{name} {time} {room}".format(name=next_course.get("name", "?"), time=t_str, room=room_str))
    exit(0)

# Handle course switch
if current_course != None and next_course != None:

    # Calculate timestr (we have to do some string magic to get time data back from ints)
    nhr = int(current_course["end"]  / 100)
    nm = int(str(current_course["end"])[-2:])
    _chr = int(time / 100)
    cm = int(str(time)[-2:])

    # Create a "now" and "next" datetime
    now = datetime.datetime(year=2000,month=1,day=1,hour=_chr, minute=cm)
    _next = datetime.datetime(year=2000, month=1, day=1, hour=nhr, minute=nm)
    dt:datetime.timedelta = (_next - now)

    if int(dt.seconds / 3600) > 0:
        t_str = f"in {int(dt.seconds / 3600)}:{int(dt.seconds / 60)}h"
    else:
        t_str = f"in {int(dt.seconds / 60)}m"


    # Calculate roomstr
    room = next_course.get("room", "")
    if room:
        room_str = f"in room {room}"
    else:
        room_str = ""

    print("{course} ends {time}. Next: {name} {room}".format(course=current_course["name"] ,name=next_course.get("name", "?"), time=t_str, room=room_str))
    exit(0)

# Handle no next course
if current_course != None and next_course == None:

    # Calculate timestr (we have to do some string magic to get time data back from ints)
    nhr = int(current_course["end"]  / 100)
    nm = int(str(current_course["end"])[-2:])
    _chr = int(time / 100)
    cm = int(str(time)[-2:])

    # Create a "now" and "next" datetime
    now = datetime.datetime(year=2000,month=1,day=1,hour=_chr, minute=cm)
    _next = datetime.datetime(year=2000, month=1, day=1, hour=nhr, minute=nm)
    dt:datetime.timedelta = (_next - now)

    if int(dt.seconds / 3600) > 0:
        t_str = f"in {int(dt.seconds / 3600)}:{int(dt.seconds / 60)}h"
    else:
        t_str = f"in {int(dt.seconds / 60)}m"


    print("{course} ends {time}!".format(course=current_course["name"], time=t_str))
    exit(0)

