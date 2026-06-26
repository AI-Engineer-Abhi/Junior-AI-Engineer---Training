# Task 26-06-26

This folder contains simple, student-friendly Python examples for learning list comprehensions, dictionary comprehensions, and generators.

## Files and What They Teach

- `dictionary_comprehension.py`
  - Builds a nested student marks dictionary using a dictionary comprehension.
  - Creates a number-to-letter mapping using `zip()`.
  - Great for learning how to make dictionaries in one line.

- `generator.py`
  - Uses a generator expression to square only even numbers from a nested list.
  - Shows a generator function that yields square values one at a time.
  - Good for understanding lazy evaluation and `yield`.

- `list_comprehension.py`
  - Extracts even numbers from a 2D list using a list comprehension.
  - Flattens a 2D list into a single list in one line.
  - Helps practice compact loops and filtering.

## Example Snippets

### Dictionary comprehension
```python
students = ["Alice", "Bob"]
subjects = ["Math", "Science"]
marks = {student: {subject: 0 for subject in subjects} for student in students}
print(marks)
```

### List comprehension with condition
```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
even_nums = [n for row in matrix for n in row if n % 2 == 0]
print(even_nums)
```

### Generator function
```python
def gen_func():
    for i in range(5):
        yield i ** 2

for value in gen_func():
    print(value)
```

## Tips for Students

- A list comprehension is a short way to write a `for` loop that makes a list.
- A dictionary comprehension works the same but creates a dictionary.
- Generators use `yield` and produce values one by one.
- Practice by changing the lists and seeing how the output changes.
