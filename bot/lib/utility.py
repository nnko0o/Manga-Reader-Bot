# Made By @nnko0o in https://github.com/nnko0o/Manga-Reader-Bot

"""
Utility Moulde
"""
import httpx, json
from PIL import Image
from io import BytesIO
import httpx , os , pyrogram
import asyncio,aiofiles,types

async def download_image(url:str):
    """"""
    headers = {
        'Host': '3asq.org',
        'authority': '3asq.org',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image,webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
	
    filename = url.split('/')[-1]
    print(" "+filename)
    if (
    os.path.isfile("../cache/"+filename)or
  os.path.isfile("./cache/"+filename)):
    	print(" .Image in already cache")
    	return f"./cache/{filename}"
    #elif os.path.isfile("./cache/"+filename):print(" 222")
    	
    async with httpx.AsyncClient(http2=True) as client_:
	    print(" File is NOT here,\nWill going to download...")
	    response = await client_.get(url, headers=headers)
	    print(" Image downloaded!, OPENING IMAGE...")
    image = Image.open(BytesIO(response.content)).convert('RGB')
    image.save(await aiofiles.open(f"./cache/{filename}","wb"),"JPEG")
    return f"./cache/{filename}"

async def get_file_id_by_message_id(
	  client:pyrogram.Client
	, chat_id:int
	, Message_id:str or int
	,) -> str:
    Message:pyrogram.types.Message=await client.get_messages(
    chat_id=chat_id,
    message_ids=Message_id
    )
    file_id:str = Message.document.file_id
    return file_id
async def get_user_from_waitList(wait_list:list,chat_id:int):
	for user in wait_list:
		if user==chat_id:
			return True 
	return False
async def add_user(dataBase:dict,chat_id:int):
	users:list=dataBase["users"]
	try:
		for user in users:
			if user==chat_id:pass 
			else:users.append(chat_id)
	except:users.append(chat_id)
	print (dataBase)
	#with open("dataBase.json","w") as file:
#		json.dump(
#		obj=dataBase,fp=file,indent=4
#		)
#	file.close()
	
#asyncio.run(
#download_image(url="https://3asq.org/wp-content/uploads/WP-manga/data/manga_5ca164e635725/0a165af44ab22071274bc133bae1a75e/04.jpg"
#	
#	)
#)
