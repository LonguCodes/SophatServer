from message import data

#data.create_new_chat(0,[0])
#data.save_chat(0)

data.load_chat(0,2)
for i in data.load_messages(0):
   print(i)