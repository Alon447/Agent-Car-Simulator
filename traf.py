def reverse_dict_value(d, key):
  d[key] = d[key][::-1]

d = {"key1": "value1"}
reverse_dict_value(d, "key1")
print(d)