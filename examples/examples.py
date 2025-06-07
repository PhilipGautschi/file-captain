""" Usage examples for the file-utils package.

Demonstrates saving and loading data with automatic format detection
including overwrite protection.

Copyright (c) 2025 Philip Gautschi
SPDX-License-Identifier: MIT
"""

from file_utils import load_file, save_file

# Save data to a file
text_data = "Hello, world and some unicode characters! 🧠 字 Ω"
save_file("text.txt", text_data)

serializable_object = {"key1": "text-key", 2: "number-key"}
save_file("object.pickle", serializable_object)

dict_data = {"host": "localhost", "port": 8080}
save_file("dict.json", dict_data)

# Save with overwrite protection disabled
dict_data_new = {"host": "localhost", "port": 8080, "user": "admin"}
save_file("dict.json", dict_data_new, overwrite_protection=False)


# Load data from a file
loaded_text = load_file("text.txt")
print(loaded_text)
loaded_dict = load_file("dict.json")
print(loaded_dict)
my_object = load_file("object.pickle")
print(my_object)
