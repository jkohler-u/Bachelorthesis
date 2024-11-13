import csv

# Function to extract numbers from a string
def extract_numbers(sentence):
    numbers = []
    for word in sentence.split():
        try:
            numbers.append(float(word))
        except ValueError:
            pass
    return numbers

# Open the CSV file
with open('responses.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    lines = list(reader)

# Iterate through each line and update if necessary
for i, line in enumerate(lines):
    numbers = extract_numbers(line[0])
    if len(numbers) == 1:
        lines[i][0] = numbers[0]

# Write the updated lines back to the CSV file
with open('responsesnr.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(lines)
