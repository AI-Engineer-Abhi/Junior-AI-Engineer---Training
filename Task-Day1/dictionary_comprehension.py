# Dictionary Comprehension

# Student marks structure (default score = 0)
students = ["Alice", "Bob"]
subjects = ["Math", "Science"]

marks = {
    student: {subject: 0 for subject in subjects}
    for student in students
}

print(marks)


# Matching numbers to the alphabets

nums = [1, 2, 3, 4, 5]
alphabet = ['a', 'b', 'c', 'd', 'e']

match_dict = {num: letter for num, letter in zip(nums, alphabet)}
print(match_dict)
