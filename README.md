# lunchTag

A lunch pair generator for the 2021 summer interns at Intuit, used weekly.
`lunchTag.py` is a basic program that will uses a general file called `lunchTag_submissions.csv` with a similar format to `Interns_lunchTag.py`
`Interns_lunchTag.py` is used for intern-intern matches based on categories.
`FTE_lunchTag.py` is used for intern-full-time-employee matches.

## Expected Input

### Interns_lunchTag.py

`.csv` file containing 3 columns (based on Google Forms)

Column 1: submission date

Column 2: name

Column 3: email

### FTE_lunchTag.py

`.csv` file containing 3 columns (based on Google Forms)

Column 1: submission date

Column 2: name

Column 3: email

Column 4: category (ex: software engineering, product management, etc.)

Column 5: match preference (3 options: same category only, same category or general pool, general pool)

Column 6: one thing to ask the FTE (only for interns)

Column 7: one thing to talk about with the intern (only for FTEs)

## Output
`.csv` file containing 3 columns, each with relevant information based on submissions

Column 1: Person 1 (the 'sender.' This person is responsible for setting up the lunch with the other two columns for a given row)

Column 2: Person 2 (the 'recipient.' This is the person who column 1 will reach out to)

Column 3: Person 3 (only if there are an odd # of submissions)

## Usage

#### Interns_lunchTag.py

`python3 Interns_lunchTag.py {original document name} {category}`

#### FTE_lunchTag.py

`python3 FTE_lunchTag.py {original document name}`

### Output File Name

#### Interns_lunchTag.py

Using the category inputted on the command line, the output file name will have the following format:

`{category}-lunch_pairs-{date}.csv`

for example:

`SWE-lunch_pairs-6-16-2021.csv`

#### FTE_lunchTag.py

`FTE_lunch_pairs-{date}.csv`
