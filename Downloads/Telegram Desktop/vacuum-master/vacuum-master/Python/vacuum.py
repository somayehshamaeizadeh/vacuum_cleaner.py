from random import randint
from sys import platform
from os import system
from time import sleep

isclean = False
while not isclean:
    num = input("Enter room number: ")
    check_digit=num.isdigit()
    if check_digit:
        size = int(num)
        isclean = True
    else:
        print("Please enter an integer which idicated the number of rooms must be cleaned.")

    if platform=="win32":
        x="cls"
    else:
        x="clear"
state = {
    "status": "Moving...",
    "clearCommand": x,
    "reverse": False,
    "boxes": [],
    "canvas": "",
    "agentLocation": [],
}


def creat_Boxes(boxesStatus: list = None) -> list:
    global size
    boxes = []
    for i in range(size):
        boxes.append([])
        for j in range(size):
            boxes[i].append(randint(0, 1))
    return boxes


def total_view(rooms: list, vacumecleaner_location: list) -> str:
    global state
    view = ""
    for i in range(len(rooms)):
        view += "\n"
        for j in range(len(rooms[i])):
            view += (
                "● "
                if i == vacumecleaner_location[0] and j == vacumecleaner_location[1]
                else "x "
                if rooms[i][j] == 1
                else "  "
            )
    return view


def moving_vacume_cleaner(current_vacumecleaner_Location: list = None) -> list:
    global state
    if current_vacumecleaner_Location == []:
        newLocation = [0, 0]
    else:
        newLocation = [current_vacumecleaner_Location[0], current_vacumecleaner_Location[1]]
        if current_vacumecleaner_Location[0] == (size - 1) and current_vacumecleaner_Location[1] == (
            0 if size % 2 == 0 else (size - 1)
        ):
            state["status"] = "cleaning is done"
        else:
            if current_vacumecleaner_Location[1] == (size - 1) and state["reverse"] == False:
                newLocation[0] = current_vacumecleaner_Location[0] + 1
                newLocation[1] = current_vacumecleaner_Location[1]
                state["reverse"] = True
            elif current_vacumecleaner_Location[1] == 0 and state["reverse"] == True:
                newLocation[0] =current_vacumecleaner_Location[0] + 1
                newLocation[1] = current_vacumecleaner_Location[1]
                state["reverse"] = False
            elif current_vacumecleaner_Location[1] <= (size - 1) and state["reverse"] == True:
                newLocation[0] = current_vacumecleaner_Location[0]
                newLocation[1] = current_vacumecleaner_Location[1] - 1
            elif current_vacumecleaner_Location[1] >= 0 and state["reverse"] == False:
                newLocation[0] = current_vacumecleaner_Location[0]
                newLocation[1] = current_vacumecleaner_Location[1] + 1
    return newLocation


def make_change_vacume_statuse(currentStatus: str, boxesStatus: list, agentLocation: list) -> str:
    if currentStatus != "cleaning is done":
        if currentStatus == "Moving...":
            newStatus = "Checking..."
        elif currentStatus == "Checking...":
            if boxesStatus[agentLocation[0]][agentLocation[1]] == 1:
                newStatus = "Cleaning..."
            else:
                newStatus = "Moving..."
        elif currentStatus == "Cleaning...":
            boxesStatus[agentLocation[0]][agentLocation[1]] = 0
            newStatus = "Moving..."
    else:
        newStatus = currentStatus
    return newStatus


def take_action() -> None:
    global state
    sleep(1)
    system(state["clearCommand"])
    if state["status"] == "Moving...":
        y=moving_vacume_cleaner(state["agentLocation"])
    else:
        y=state["agentLocation"]
    if state["boxes"] == []:
        z=creat_Boxes()
    else:
        z=state["boxes"]
    state["agentLocation"] = y
    state["boxes"] = z
    canvas = total_view(state["boxes"], state["agentLocation"])
    print(
        "Room size: " + str(size) + "x" + str(size),
        canvas,
        "Status: " + state["status"],
        sep="\n",
    )
    state["status"] = make_change_vacume_statuse(
        state["status"], state["boxes"], state["agentLocation"]
    )


def run_vacume_cleaner() -> None:
    global state
    while state["status"] != "cleaning is done":
        take_action()


run_vacume_cleaner()
