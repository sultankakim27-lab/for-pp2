Practice-05 — Python Regular Expressions (RegEx)

This practice focuses on working with **Regular Expressions in Python** using the `re` module.

Main goals:

* learn regex syntax
* use regex functions in Python
* parse receipt data from a text file

📁 Project Structure
Practice5/
├── receipt_parser.py
├── raw.txt
└── README.md

✅ Topics Summary

1. RegEx Basics
   Regular expression patterns
   Metacharacters: . * + ? ^ $ [] () | \
   Character sets and classes

2. Special Sequences
   \d — digits
   \w — word characters
   \s — whitespace
   \D, \W, \S — opposite versions

3. Quantifiers
   {n} — exact number
   {n,} — minimum repetitions
   {n,m} — range of repetitions

4. Python `re` Module
   re.search() — find first match
   re.findall() — find all matches
   re.split() — split string using regex
   re.sub() — replace pattern with another value
   re.match() — match at the beginning of string

5. Receipt Parsing
   Using regex to extract information from `raw.txt`:

* product names
* prices
* total amount
* date and time
* payment method

The parsed data is displayed in a structured format using Python.
