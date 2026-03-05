import re

# 1. 'a' followed by zero or more 'b'
text1 = "a ab abb abbb ac"
pattern1 = r"ab*"
print("1:", re.findall(pattern1, text1))


# 2. 'a' followed by two to three 'b'
text2 = "ab abb abbb abbbb"
pattern2 = r"ab{2,3}"
print("2:", re.findall(pattern2,text2))


# 3. lowercase letters joined with underscore
text3 = "hello_world test_case python_code notValid"
pattern3 = r"[a-z]+_[a-z]+"
print("3:", re.findall(pattern3, text3))


# 4. one uppercase letter followed by lowercase letters
text4 = "Hello World Python regex Test"
pattern4 = r"[A-Z][a-z]+"
print("4:", re.findall(pattern4, text4))


# 5. 'a' followed by anything ending in 'b'
text5 = "aab axxb a123b ac"
pattern5 = r"a.*b"
print("5:", re.findall(pattern5, text5))


# 6. replace space, comma, or dot with colon
text6 = "Hello, world. Python regex is fun"
result6 = re.sub(r"[ ,\.]", ":", text6)
print("6:", result6)


# 7. convert snake_case to camelCase
def snake_to_camel(text):
    parts = text.split("_")
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

text7 = "snake_case_string"
print("7:", snake_to_camel(text7))


# 8. split string at uppercase letters
text8 = "HelloWorldPython"
result8 = re.split(r"(?=[A-Z])", text8)
print("8:", result8)


# 9. insert spaces between words starting with capital letters
text9 = "HelloWorldPython"
result9 = re.sub(r"([A-Z])", r" \1", text9).strip()
print("9:", result9)


# 10. convert camel Case to snake_case
text10 = "helloWorldPython"
result10 = re.sub(r"([A-Z])", r"_\1", text10).lower()
print("10:", result10)