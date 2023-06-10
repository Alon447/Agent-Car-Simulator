import pandas as pd
import json

#JSON format: {source_road:{target_road:{optional_road:time}}}
content = {
  12:
    {
      13: {
        14:1,
        15:2
      },
      14:{
        15:1,
        16:2
      },
    13: {
      13: {
          14:1,
          15:2
        },
        14:{
          15:1,
          16:2
        }
    }
  }
}
# # write to JSON
# with open('test_write_q.json', 'w') as f:
#     json.dump(content, f)

#read from JSON to pandas
with open('test_write_q.json') as file:
  newdata = json.load(file)
print(newdata)
print(type(newdata))
