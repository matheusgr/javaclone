import re

pattern_comment = re.compile("/\*.*?\*/", re.DOTALL)
pattern_one_line_comment = re.compile("//.*?\n")
pattern_string = re.compile('".*?"', re.DOTALL)
pattern_spaces = re.compile('\s',re.DOTALL)
pattern_digits = re.compile('\d',re.DOTALL)

# https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
def remove_comments(string):
    for p in [pattern_comment, pattern_one_line_comment, pattern_string]:
        string = re.sub(p,"" ,string)
    return string
