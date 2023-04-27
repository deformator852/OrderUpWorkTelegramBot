from pyrogram import Client
from create_bot import API_ID,API_HASH

async def all_download():
    id = ""
    #chat_id
    client = Client('sesion', API_ID, API_HASH)
    await client.start()
    messages = client.get_chat_history(chat_id=id)
    async for mess in messages:
        print(mess.text)
        with open("messages.txt", "a") as file:
          if mess != None:
            file.write(str(mess.text) + "\n")
    await client.stop()

