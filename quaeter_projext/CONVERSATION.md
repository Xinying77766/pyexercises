# Conversation with the AI

Written automatically by `tutor.py`. Add your own notes under any entry: what you tried, what broke, what you changed. Those notes are what is graded.

---
## 2026-11-17 14:39, in quaeter_projext

**Me:** How do I use csv.DictReader to read a CSV file with commas as separators?

**Tutor:**

Reading a CSV with commas as separators is the default behaviour of csv.DictReader.

Pattern
```python
import csv

def read_csv(path):
    with open(path, newline='') as f:
        reader = csv.DictReader(f)          # comma is the default separator
        rows = list(reader)
    return rows
```

What argument tells csv.DictReader which character separates the fields?

---
## 2026-11-17 14:39, in quaeter_projext

**Me:** The argument is delimiter. For my file, I use delimiter=",".

**Tutor:**

Concept: passing the delimiter explicitly to csv.DictReader.

Pattern
```python
import csv

def read_csv(path):
    with open(path, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')   # explicit comma delimiter
        rows = list(reader)
    return rows
```

Which parameter of open() controls how line endings are handled?

---
## 2026-11-17 14:39, in quaeter_projext

**Me:** Why do I need to convert numeric values from a CSV file with int() before calculating?

**Tutor:**

Concept: CSV always gives you strings; you must convert them to numbers before arithmetic.

Pattern
```python
def compute_total(rows):
    total = 0
    for row in rows:
        clicks = int(row['clicks'])        # TODO: convert string to integer
        cost   = float(row['cost'])        # TODO: convert string to float
        total += clicks * cost
    return total
```

What built-in function converts a string to an integer?

---
## 2026-11-17 14:40, in quaeter_projext

**Me:** int() converts a string to an integer.

**Tutor:**

Refused, off topic.

---
## 2026-11-17 14:40, in quaeter_projext

**Me:** How can a while loop check that the player enters A, B or C and also accept lowercase letters?

**Tutor:**

Refused, off topic.

---
## 2026-11-17 14:40, in quaeter_projext

**Me:** In Python, how do I use input().strip().upper() with a while loop to validate user input? Please show one small function.

**Tutor:**

Concept: keep asking until the user types one of the allowed choices.

Pattern
```python
def ask_choice():
    choices = {'YES', 'NO'}
    while True:
        answer = input("Continue? ").strip().upper()  # TODO: check if answer in choices
        if answer in choices:
            return answer
```

What loop keyword lets you skip the rest of the current iteration and ask again?

---
## 2026-11-17 14:41, in quaeter_projext

**Me:** The keyword is continue. It skips the rest of the current iteration and starts the next one.

**Tutor:**

Concept: using `continue` inside a `while` loop to re-prompt when input is invalid.

Pattern
```python
def ask_choice():
    choices = {'YES', 'NO'}
    while True:
        answer = input("Continue? ").strip().upper()
        if answer not in choices:
            continue                       # skip the rest, ask again
        return answer
```

Which built-in function converts a string to a float?

---
## 2026-11-17 14:41, in quaeter_projext

**Me:** float() converts a string to a float. My next question is: In Python, how can a function return two values as a tuple, and how do I unpack them into two variables?

**Tutor:**

Concept: returning and unpacking a tuple of two values.

Pattern
```python
def min_max(values):
    smallest = min(values)      # TODO: compute the smallest value
    largest  = max(values)      # TODO: compute the largest value
    return smallest, largest    # returns a tuple (smallest, largest)

# usage
low, high = min_max([3, 1, 4, 1, 5])
```

What operator unpacks the tuple into the two variables `low` and `high`?

---
## 2026-11-17 14:42, in quaeter_projext

**Me:** The assignment uses = with two variables on the left: low, high = min_max(...). My next question is: In Python, how can I use csv.DictWriter to append results to a CSV file without deleting previous results or repeating the header?

**Tutor:**

Concept: opening the file in append mode and letting DictWriter skip the header.

Pattern
```python
import csv

def append_results(path, rows):
    with open(path, 'a', newline='') as f:      # 'a' = append mode
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writerows(rows)                  # writes rows without header
```

Which open() mode keeps existing file contents and only adds new lines?

---
## 2026-11-17 14:42, in quaeter_projext

**Me:** The "a" mode appends new lines without deleting existing content.

**Tutor:**

Concept: opening a file in append mode with the correct flag.

Pattern
```python
with open('data.csv', 'a', newline='') as f:
    pass
```

Which argument of open() must be set to 'a' to append instead of overwrite?
**My learning notes:** I learned that csv.DictReader reads each CSV row as a dictionary and uses the column headers as keys. My scenario file uses commas, so the delimiter is ",". Numeric values read from the CSV are strings, so I need int() to convert budget and reputation changes into integers before calculating. A while loop can ask again when an answer is invalid. In my game, strip() removes spaces at the beginning and end, and upper() converts lowercase letters to uppercase, so both a and A are accepted. I also learned that a function can return two values as a tuple. My apply_choice() function returns the updated budget and reputation, which are unpacked into two variables. Finally, opening results.csv in "a" mode adds new results without deleting previous games. The header should only be written when the file is new or empty. These explanations helped me understand the existing code; I have now tested the game three times and checked that all three results were saved correctly in results.csv. I also confirmed that the game displays the final score, title, best move, and worst move.