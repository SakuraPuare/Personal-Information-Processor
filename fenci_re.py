import re
import json


with open("info.txt", "r",encoding="utf-8") as f:
    txt = f.read()

txt_split = txt.split("\n\n")

black_list = ['陈文:', '手机', '身份证', '到新街', '一吨', '姓名', '电话']

license_pattern = r"[\u4e00-\u9fa5][a-z|A-Z|0-9]{6}"
tel_pattern = r"\d{3}-\d{8}|\d{4}-\{7,8}"
name_pattern = r"([\u4e00-\u9fa5]{2,3})(?![\u4e00-\u9fa5])"

cant_process = []
result = []
for i in txt_split:
    origin_i = i
    for t in black_list:
        i = i.replace(t, "")
    licences = re.findall(license_pattern, i)
    tels = re.findall(tel_pattern, i)
    names = re.findall(name_pattern, i)
    if len(licences) > 1:
        cant_process.append(origin_i)
        continue
    if len(licences) == 0:
        cant_process.append(origin_i)
        continue
    name = None
    if len(names) != 0:
        name = names[0]
    tel = None
    if len(tels) != 0:
        tel = tels[0]
    entry = {"license": licences[0], "name": name, 'tel': tel}
    result.append(entry)

print(len(cant_process))
print(len(result))

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False)

with open("error.json", "w", encoding="utf-8") as f:
    json.dump(cant_process, f, ensure_ascii=False)
