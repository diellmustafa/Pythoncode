# words = ("spam", "eggs", "ham")
# print(words[0])

# empty_tuple = ()

# words[1] = "cheese"

# person = ("Rubik", 15, "Finland")
#
# name, age, birthplace = person
# print(name, age, birthplace)

#
# my_dictionary = {
#     "key1": "value1",
#     "key2": "value2",
#     "key3": "value3",
# }

# contact_info = {
#     "Diell":"049200908",
#     "Drit":"049180807"
# }

# drit_phone = contact_info["Drit"]
#
# print(drit_phone)
#
# contact_info["Dielli2.0"] = "049700503"
#
# print(contact_info)

# del contact_info["Diell"]
# print(contact_info)

# keyes = contact_info.keys()
# print(keyes)

# values = contact_info.values()
# print(values)

# items = contact_info.items()
# print(items)

contact_info2 = {
    "Diell": {
        "email": "diell@gmail.com",
        "number": "049202020",
        "password": "diell123!"
    },
    "Drit": {
        "email": "drit@gmail.com",
        "number": "0473002030",
        "password": "driti123!"
    },
    "Dion": {
        "email": "dion@gmail.com",
        "number": "045325453",
        "password": "dion1234!"
    }
}

diell_contact = contact_info2["Diell"]
print(diell_contact)

grades = {
    ("Diell", "Math") : 5,
    ("Drit", "Math") : 2,
}

diell_math = grades[("Diell", "Math")]
print(diell_math)