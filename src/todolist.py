from datetime import datetime
from datetime import timedelta
from enum import IntEnum

from db import Task


class Menu(IntEnum):
    EXIT = 0,
    SHOW_TODAYS_TASKS = 1,
    SHOW_WEEKS_TASKS = 2,
    SHOW_ALL_TASKS = 3,
    SHOW_MISSED_TASKS = 4,
    ADD_TASK = 5,
    DELETE_TASK = 6


class ToDoList:
    def __init__(self) -> None:
        self.menu = {
            Menu.EXIT: self.exit,
            Menu.SHOW_TODAYS_TASKS: self.show_todays_tasks,
            Menu.SHOW_WEEKS_TASKS: self.show_weeks_tasks,
            Menu.SHOW_ALL_TASKS: self.show_all_tasks,
            Menu.SHOW_MISSED_TASKS: self.show_missed_tasks,
            Menu.ADD_TASK: self.add_task,
            Menu.DELETE_TASK: self.delete_task
        }
        self.is_running = True

    def exit(self) -> None:
        self.is_running = False
        print("\nBye!")

    @staticmethod
    def get_int_input(min_: int, max_: int, message: str = "") -> int:
        while True:
            try:
                user_input = int(input(message))
                if min_ <= user_input <= max_:
                    return user_input
                print(f"Error: Invalid input. Only enter a non-negative number of max {max_}.")
            except ValueError:
                print("Error: That is not an integer.")

    def run(self) -> None:
        while self.is_running:
            self.print_menu()
            selection = self.get_int_input(0, len(self.menu) - 1)
            self.menu[selection]()

    @staticmethod
    def show_todays_tasks() -> None:
        today = datetime.today()
        print(f"\nToday {datetime.strftime(today, '%d %b')}:")
        if tasks := Task.find_tasks_by_date(today):
            ToDoList.print_tasks(tasks)
        else:
            print("Nothing to do!\n")

    @staticmethod
    def show_weeks_tasks() -> None:
        today = datetime.today()
        dates = [today + timedelta(day) for day in range(7)]
        for date in dates:
            print(f"{datetime.strftime(date, '%A %d %b')}")
            if tasks := Task.find_tasks_by_date(date):
                ToDoList.print_tasks(tasks)
            else:
                print("Nothing to do!\n")

    @staticmethod
    def show_all_tasks() -> None:
        print("\nAll tasks:")
        if tasks := Task.find_all(sort_by_date=True):
            ToDoList.print_tasks(tasks)
            return
        print("All tasks have been completed!")

    @staticmethod
    def show_missed_tasks() -> None:
        print("\nMissed tasks:")
        if missed_tasks := Task.missed_tasks():
            ToDoList.print_tasks(missed_tasks)
            return
        print("All tasks have been completed!\n")

    @staticmethod
    def print_tasks(tasks: list["Task"]) -> None:
        for index, row in enumerate(tasks):
            print(f"{index + 1}. {row.task}. {row.deadline.strftime('%d %b')}")
        print()  # required by JetBrains Academy test

    @staticmethod
    def add_task() -> None:
        task = input("\nEnter a task\n")
        deadline = input("Enter a deadline\n")
        Task.add_task(task, deadline)
        print("The task has been added!\n")

    @staticmethod
    def delete_task() -> None:
        if tasks := Task.find_all(sort_by_date=True):
            print("\nChoose the number of the task you want to delete:")
            ToDoList.print_tasks(tasks)
            selection = ToDoList.get_int_input(
                1, len(tasks))
            Task.delete_task(selection - 1)
            print("The task has been deleted!\n")
            return
        print("\nNothing to delete\n")

    @staticmethod
    def print_menu() -> None:
        print(("1) Today's tasks\n"
               "2) Week's tasks\n"
               "3) All tasks\n"
               "4) Missed tasks\n"
               "5) Add a task\n"
               "6) Delete a task\n"
               "0) Exit"))
