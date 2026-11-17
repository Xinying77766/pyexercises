# Name: Xinying LI
# Group letter: A

# 1. What goes in?
# My input file is scenarios_A.csv.
# It uses commas as separators and has 14 columns.
# ID and Scenario identify and describe each situation.
# OptionA, OptionB and OptionC contain the choices.
# BudgetA, BudgetB and BudgetC contain the budget changes.
# ReputationA, ReputationB and ReputationC contain reputation changes.
# FeedbackA, FeedbackB and FeedbackC contain the feedback.
# The changes are integers such as -800, 0 and 15.
# I use int() to convert these values before calculating.
# Text containing commas is enclosed in quotation marks.

# 2. What happens?
# Display the day, budget and reputation.
# Display one scenario and its three options.
# Ask for A, B or C and check the answer.
# Update the budget and reputation.
# Keep reputation at a maximum of 100.
# Display feedback and record the move.
# Stop if either gauge reaches zero or below.

# 3. What comes out?
# The game displays the final budget and reputation.
# It displays the reason for being fired or the final score and title.
# It also displays the best and worst moves.
# One row is added to results.csv after each finished game.
# The columns are name, budget, reputation, title and date.

# 4. What could go wrong?
# Invalid choice: keep asking for A, B or C.
# Empty name: ask the player to enter a name.
# Budget or reputation at zero or below: stop the game.
# Reputation above 100: reduce it to 100.
# Missing scenario file: display a message and stop.
# Invalid CSV data: display a message asking to check the file.
# Saving fails: display a message instead of crashing.

# Extra feature: d - Difficulty selection.
# Easy starts with 15000 EUR and hard starts with 6000 EUR.
# I chose this so players can choose their challenge level.

# File reading and writing are adapted from the teacher's
# read_csv_as_dict.py and write_a_csv.py examples.


# I import the modules needed for the game.
import csv
import os
import random
from datetime import date


# I use the teacher's method to locate files beside this Python file.
HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "scenarios_A.csv")
OUTPUT = os.path.join(HERE, "results.csv")


# I read the CSV into a list of dictionaries, as in the teacher's example.
def load_scenarios():
    scenarios = []

    with open(SAMPLE, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=",")

        for row in reader:
            scenarios.append(row)

    # I convert the numeric text and store each option as a tuple.
    for row in scenarios:
        options = {}

        for letter in ("A", "B", "C"):
            text = row["Option" + letter]
            budget_change = int(row["Budget" + letter])
            reputation_change = int(row["Reputation" + letter])
            feedback = row["Feedback" + letter]

            options[letter] = (
                text,
                budget_change,
                reputation_change,
                feedback
            )

        row["options"] = options

        # I check that the situation column exists.
        if not row["Scenario"]:
            raise ValueError("A scenario is missing its description.")

    return scenarios


# I ask for a name and reject an empty answer.
def ask_name():
    name = input("What is your name? ").strip()

    while name == "":
        name = input("Please enter your name: ").strip()

    return name


# I let the player choose the starting budget.
def choose_difficulty():
    print("\nChoose your difficulty:")
    print("Easy: 15000 EUR")
    print("Hard: 6000 EUR")

    difficulty = input("Type easy or hard: ").strip().lower()

    while difficulty not in ("easy", "hard"):
        difficulty = input(
            "Please type easy or hard: "
        ).strip().lower()

    if difficulty == "easy":
        return 15000
    else:
        return 6000


# I repeat the question until the player enters a valid choice.
def ask_choice():
    choice = input("Your choice (A, B or C): ").strip().upper()

    while choice not in ("A", "B", "C"):
        choice = input(
            "Please type A, B or C: "
        ).strip().upper()

    return choice


# I update both gauges and return a tuple.
def apply_choice(budget, reputation, option):
    text, budget_change, reputation_change, feedback = option

    budget = budget + budget_change
    reputation = reputation + reputation_change

    if reputation > 100:
        reputation = 100

    return budget, reputation


# I use the final score to find the surviving player's title.
def get_title(score):
    if score < 95:
        return "Eternal Intern"
    elif score < 120:
        return "Growth Hacker"
    elif score < 140:
        return "CMO Material"
    else:
        return "Viral Legend"


# I compare the reputation changes stored first in each history tuple.
def show_best_and_worst(history):
    best = max(history)
    worst = min(history)

    best_change, best_day, best_text = best
    worst_change, worst_day, worst_text = worst

    print(
        f'\nBest move: day {best_day}, '
        f'"{best_text}" ({best_change:+d})'
    )

    print(
        f'Worst move: day {worst_day}, '
        f'"{worst_text}" ({worst_change:+d})'
    )


# I adapt the teacher's DictWriter example to append one game result.
def save_result(name, budget, reputation, title):
    result = {
        "name": name,
        "budget": budget,
        "reputation": reputation,
        "title": title,
        "date": str(date.today())
    }

    # I only write the header when the file is new or empty.
    needs_header = (
        not os.path.exists(OUTPUT)
        or os.path.getsize(OUTPUT) == 0
    )

    # The append mode keeps results from previous games.
    with open(OUTPUT, "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "name", "budget", "reputation", "title", "date"
            ],
            delimiter=","
        )

        if needs_header:
            writer.writeheader()

        writer.writerow(result)


# I organise the whole game using the smaller functions.
def main():
    print("=" * 45)
    print("SURVIVE THE QUARTER")
    print("Welcome to Croissant Rocket!")
    print("Survive 10 days as our marketing manager.")
    print("=" * 45)

    # I handle problems when opening or reading the scenario file.
    try:
        scenarios = load_scenarios()
    except FileNotFoundError:
        print("Cannot find scenarios_A.csv.")
        print("Put it in the same folder as this Python file.")
        return
    except (KeyError, ValueError, TypeError, csv.Error):
        print("There is a problem with the CSV data.")
        print("Check the column names, numbers and quotation marks.")
        return
    except (OSError, UnicodeError):
        print("The scenario file could not be read.")
        print("Check its permissions and UTF-8 encoding.")
        return

    # I check there are enough scenarios for ten days.
    if len(scenarios) < 10:
        print("The CSV must contain at least 10 scenarios.")
        return

    # I prepare the player and the starting values.
    name = ask_name()
    budget = choose_difficulty()
    reputation = 50
    history = []

    # I shuffle all scenarios, including the three original additions.
    random.shuffle(scenarios)

    # I play ten different scenarios unless the player is fired.
    for day in range(1, 11):
        scenario = scenarios[day - 1]

        print("\n" + "-" * 45)
        print(f"Day {day}")
        print(
            f"Budget: {budget} EUR | "
            f"Reputation: {reputation}/100"
        )
        print(scenario["Scenario"])

        for letter in ("A", "B", "C"):
            option_text = scenario["options"][letter][0]
            print(f"{letter}: {option_text}")

        # I get the choice and unpack the option tuple.
        choice = ask_choice()
        option = scenario["options"][choice]

        text, budget_change, reputation_change, feedback = option

        # I unpack the tuple returned by apply_choice.
        budget, reputation = apply_choice(
            budget, reputation, option
        )

        print(feedback)
        print(
            f"Budget change: {budget_change:+d} EUR | "
            f"Reputation change: {reputation_change:+d}"
        )
        print(
            f"Now: {budget} EUR | "
            f"Reputation: {reputation}/100"
        )

        # I record the option's reputation impact, day and text.
        history.append((reputation_change, day, text))

        # I stop immediately if either gauge is zero or negative.
        if budget <= 0 or reputation <= 0:
            break

    # I display the final result and explain why the player was fired.
    print("\n" + "=" * 45)

    if budget <= 0 or reputation <= 0:
        title = "Fired"
        print(f"{name}, you are fired!")

        if budget <= 0:
            print("Reason: your budget reached zero or below.")

        if reputation <= 0:
            print("Reason: your reputation reached zero or below.")

    else:
        score = reputation + budget // 200
        title = get_title(score)

        print("Quarter survived!")
        print(f"Final score: {score}")
        print(f"{name}, your title: {title}")

    print(f"Final budget: {budget} EUR")
    print(f"Final reputation: {reputation}/100")

    # I show the best and worst moves, including for failed games.
    show_best_and_worst(history)

    # I save the finished game without overwriting earlier results.
    try:
        save_result(name, budget, reputation, title)
        print("\nSaved in results.csv")
    except (OSError, UnicodeError, csv.Error):
        print("\nCould not save results.csv.")
        print("Check that the folder and file are writable.")


# I run the game and handle an interrupted input without a traceback.
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted before completion.")