# lunchTag

A lunch pair generator for the 2021 summer interns at Intuit, used weekly.

## Expected Input

`.csv` file containing 3 columns (based on Google Forms)

Column 1: submission date

Column 2: name

Column 3: email


## Output
`.csv` file containing 3 columns, each in the following format: `name: email`

Column 1: Person 1 (the 'sender.' This person is responsible for setting up the lunch with the other two columns for a given row)

Column 2: Person 2 (the 'recipient.' This is the person who column 1 will reach out to)

Column 3: Person 3 (only if there are an odd # of submissions

## Usage

`python3 lunchTag.py {original document name} {category}`

### Output File Name

Using the category inputted on the command line, the output file name will have the following format:

`{category}-lunch_pairs-{date}.csv`

for example:

`SWE-lunch_pairs-6-16-2021.csv`
