# Made By @nnko0o in https://github.com/nnko0o/Manga-Reader-Bot

#pylint:disable=C0103
from pyrogram import Client,filters,idle
from pyrogram.types import Message,CallbackQuery,InputMediaDocument
from pyrogram.enums import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified, MediaEmpty
from pykeyboard import InlineKeyboard, InlineButton
from asyncio import get_event_loop
from lib.Manga3asq import Manga3asq
from lib.utility import *
import os,json,sched,time,threading,re,aiofiles
from io import BytesIO
global msg01
#Things:-
# list.remove() # delete item from value


db = {
	# name:chabter_number :- pages <List of string have link>
	"berserk:num"    : [0,1,2,3,4,5,6,7,000]
}
# List of int   <chat_id>
wait_time:list = [1229755]

api_id=0 # put your api id
api_key="put your api hash"
bot_token="put your token here"
c: Client = Client(
	"telegramClient"
	, api_id=api_id
	, api_hash=api_key
	, bot_token=bot_token
	,)
users=[]
if not os.path.isfile(path="dataBase.json"):
	with open("dataBase.json","w") as file:
		file.write("{\n")
		file.write("""
 "users":[01234]
 "manga-cach":{
  "berser:num":[["$url str","$size int"],["https://example/g.jpg",26667]]
 }
		""")
		file.write("\n}")
	file.close()
else:
	with open('dataBase.json','r')as r:
		dataBase=json.load(r)
		users=dataBase["users"]
		db = dataBase["manga-cach"]


async def download(page,m:Message):
	print(" download -> ",page)
	if int(page[1]) > 5242880 :
		
		print(" True")
		print(page)
		msg01:Message= await c.send_message(
		   chat_id=m.chat.id
		 , text="يتم تحميل الصفحة..."
		 , )
		image = await download_image(
		url=f"{page[0]}",)
		await msg01.edit_text(
		text="يتم رفع الصفحة..."
		)
		await msg01.delete()
		#os.remove(image)
		return image
	else:print(" False");return 0

async def get_chapter(manga:str, chapter:any) -> list :
	data_name=f"{manga}:{chapter}"

	try:
		if db[data_name]:return db[data_name]
		print(" .Use old chapter")

	except:
		print (" .Use New chapter")
		_3asq=Manga3asq()
		#search manga
		search = await _3asq.searchManga(manga)
		chs = await _3asq.getChapters(url=search[0]['url'].split("=")[1])
		name = search[0]['url'].split("=")[1].split("/")[-2]
		url=search[0]['url'].split("=")[1]
		ch = await _3asq.getPagesFromChapter(f"{url}{chapter}/")

		dataBase["manga-cach"][data_name]=ch
		result=dataBase["manga-cach"][data_name]
		print(f"\n***{result}***\n")
		async with aiofiles.open("dataBase.json",'w') as file:
			await file.write(f"{json.dumps(obj=dataBase,)}")
		file.close()
		#json.dump(
#	obj=dataBase,
#	fp=await aiofiles.open("dataBase.json","w"), indent=4
#	)
		return result

async def button_message(query:dict):
	manga_name=query["manga"]
	chapter=query["chapter_number"]
	page_ = query["current_page"]
	message=query["message"]
	try:q:CallbackQuery=query["Q"]
	except:pass
	chapter_:list = []
	print (page_)
	if page_!=0: page_-=1
	print (page_)
	
	try:
		if db[f"{manga_name}:{chapter}"][page_][2]:
			PageImage = db[f"{manga_name}:{chapter}"][page_][2]
			chapter_ = db[f"{manga_name}:{chapter}"]
			print("  .Used File_id")
	except:
		print (" .Used New Without File_id")
		chapter_=await get_chapter(manga_name,chapter)
		print(chapter_);print(f"\n**{chapter_}**\n")
		print (type(page_))
		PageImage=chapter_[page_][0]
		print(f" {chapter_[page_]}\n ")
		PageImage_=await download(m=message,page=chapter_[page_])
		if PageImage_!=0:PageImage=PageImage_
		print(PageImage_)
	
		
	print (f" * {len(chapter_)}\n * {page_+1}")
	#text= "رد على الصفحه بكلمة ملف سيرجع لك الصفحه بصيغة ملف"
	keyboard = InlineKeyboard()
	keyboard.paginate(
	  count_pages=len(chapter_)
	, current_page=page_+1
	, callback_pattern=f"{manga_name}:{chapter}"+'#{number}'
	)
	print(len(chapter_))
	try:
		if query["type"]=="send" or not query["type"]:
			msg = await c.send_document(
		message.chat.id,
		document=PageImage,
		reply_markup=keyboard,
		)
		elif query["type"]=="edit":
			msg = await c.edit_message_media(
			
			chat_id=message.chat.id,
			message_id=message.id,
			reply_markup=keyboard,
	        media=InputMediaDocument(
	          media=PageImage, 
	          caption=f"chapter {chapter} of {manga_name}"
	          )
			)
	except MessageNotModified:
		await q.answer(text="حبيبي هي نفسها",show_alert=True)
		#PageImage=chapter_[page_+1][0]
#		PageImage_=await download(m=message,page=chapter_[page_ + 1])
#		if PageImage_!=0:PageImage=PageImage_

#		keyboard = InlineKeyboard()
#		keyboard.paginate(
#	  count_pages=len(chapter_)
#	, current_page=page_+1
#	, callback_pattern=f"{manga_name}:{chapter}"+'#{number}'
#	)
#		if query["type"]=="send" or not query["type"]:
#			msg = await c.send_document(
#		message.chat.id,
#		document=PageImage,
#		reply_markup=keyboard,
#		)
#		elif query["type"]=="edit":
#			msg = await c.edit_message_media(
#			chat_id=message.chat.id,
#			message_id=message.id,
#			reply_markup=keyboard,
#	        media=InputMediaDocument(
#	          media=PageImage, caption="."
#	          )
#			)
	
	Page_FileId = await get_file_id_by_message_id(client=c,chat_id=msg.chat.id,Message_id=msg.id)
	if len(db[f"{manga_name}:{chapter}"][page_])==3:
		db[f"{manga_name}:{chapter}"][page_]=Page_FileId
	print(db[f"{manga_name}:{chapter}"][page_])

@c.on_message(filters.command("start"))
async def start_command(cl:Client,m:Message):
	await add_user(chat_id=m.chat.id,dataBase=dataBase)
	keyboard = InlineKeyboard(row_width=2)
	keyboard.add(
	 InlineButton("DEV",url="https://t.me/nnk0o/"),
	 InlineButton("Channel",url="https://t.me/anime_eclipse")
	,InlineButton(text="الحقوق",callback_data="start:policy"))
	#text = f"مرحباً بك **{m.from_user.first_name}** في بوت بوك،\nيقدم هذا البوت قارء مانجا بسيط وأيضاً يقدم لك مكتبة موقع الـ[العاشق](https://3asq.org) مع ميزة البحث على المانجا واختيار الفصول\nميزات مستقبلية ستضاف مثل قائمة المفضلات وحفظ الصفحات__(إرسالها كملف)__\nالمطور ——> @nnk0o"
	text =f"""
مرحبا **{m.from_user.first_name}** انا بوك،
من انا؟ انا بوت قارء مانجا بسيط وسريع، ولدي مكتبة رائعة من [مانجا العاشق](https://3asq.org) .
انا حالياً لستُ كاملاً، أي هناك ميزات وتحسينات قادمة، واحتمال وجود اخطاء هنا وهناك
اذا وجدت خطأ او تريد اي استفسار او اضافة راسل مطوري

المطور —>> @nnk0o
"""
	await m.reply_photo(photo="https://i.imgur.io/8X57wJ0_d.webp?maxwidth=640&shape=thumb&fidelity=medium"
	, caption=text
	, parse_mode=ParseMode.MARKDOWN
#	, disable_web_page_preview=True
	, reply_markup=keyboard
	,)

@c.on_message(filters.command("manga"))
async def t(cl:Client,m:Message):
	await add_user(dataBase,m.chat.id)
		
	if (len(m.text)==6 and len(m.text.split(' '))!=3):
		return await m.reply("/manga <رقم الفصل> <اسم المانجا>")
	elif len(re.findall(r"\d",m.text.split(" ")[2]))==0:
		return await m.reply("/manga <رقم الفصل> <اسم المانجا>\n                                   ^^^^^^^^^^^\nيجب ان يكون رقم، مثل: 13")
	await button_message(query={
		"manga":m.text.lower().split(" ")[1],
		"chapter_number":m.text.split(" ")[2],
		"current_page":1,
		"message":m,
		"type":"send"
	})

@c.on_callback_query()
async def inlineeQuery(cl:Client,q:CallbackQuery):
	if q.data=="start:policy":
		await q.answer("كل الحقوق تابعة لمانجا العاشق™",show_alert=True)
	elif q.data.split("#"):
		print(q.data) # berserk:13#2
		data_=q.data.lower().split('#')
		data=data_[0].split(":")
		await button_message(query={
			"manga":data[0],
			"chapter_number":data[1],
			"current_page":int(data_[1]),
			"message":q.message,
			"type":'edit',
			"Q":q
		})

@c.on_message(filters.command("bc"))
async def bc (cl:Client,m:Message):
	if m.text.lower()=="/bc":return await m.reply_text("Uasge: /bc <Text>")
	text=m.text.replace("/bc","")
	for user in users:
		await cl.send_message(
		chat_id=user,
		text=text,
		parse_mode=ParseMode.MARKDOWN,
		disable_web_page_preview=True
		,)
		await m.reply_text(text=f"sended To {user} .")
	await m.reply_text(f"Complite /bc for {len(users)}")

@c.on_message(filters.command("file_id"))
async def get_file_id(cl:Client,m:Message):
	if m.reply_to_message.photo :
		file_id=m.reply_to_message.photo.file_id
	elif m.reply_to_message.document:
		file_id=m.reply_to_message.document.file_id
	await m.reply(f"`{file_id}`",parse_mode=ParseMode.MARKDOWN)

async def main() :
	print("Starting...")
	await c.start()
	print("Runnig!")
	await idle()
async def dumpy():
	json.dump(obj=dataBase,
	fp=await aiofiles.open("dataBase.json",'w'),indent=4)
if __name__=='__main__':
	loop = get_event_loop()
	threading.Thread(target=loop.run_until_complete(main()))
	#loop.run_until_complete(dumpy())
	print("STOPED")
