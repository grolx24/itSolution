file_path = "/etc/ImageMagick-6/policy.xml"
search_string = f"<policy domain=\"path\" rights=\"none\" pattern=\"@*\"/>"
new_string = f"<!-- <policy domain=\"path\" rights=\"none\" pattern=\"@*\"/> -->"

with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
with open(file_path, 'w', encoding='utf-8') as file:
    for line in lines:
        if search_string in line:
            file.write(new_string + '\n')
        else:
            file.write(line)
