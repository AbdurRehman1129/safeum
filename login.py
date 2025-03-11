# Open the file and read its content
with open('SafeUM.txt', 'r') as file:
    # Extract usernames from each line
    usernames = [line.split(':')[0].strip() for line in file if ':' in line]

# Join the usernames in the desired format
result = ','.join(usernames)

# Print the formatted usernames
print(result)
