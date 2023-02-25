# Made By @nnko0o in https://github.com/nnko0o/Manga-Reader-Bot

#pylint:disable=C0103
from pyrogram import Client,filters,idle
from pyrogram.types import Message,CallbackQuery
from pyrogram.enums import ParseMode
import pyromod
from asyncio import get_event_loop
from lib.Manga3asq import Manga3asq
from lib.utility import *
from lib.TelegramBUI import *
import os,json,threading,re,aiofiles
#Things:-
# list.remove() # delete item from value


api_id=11619572
api_key="f9dd1efc1781f1476c53afa04d76b234"
OLD_bot_token="6114851678:AAHV7HbEcS7LpoL3dELA0qesY4nSlTaoV_U"
bot_token =	"6114851678:AAFYFbRv7ORfji2Sp7Y-4CNoTAoLIDyR1Z8"
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
	dataBase={
		"users":[],
		"manga-cach":{}
	}
	users=dataBase["users"]
	db = dataBase["manga-cach"]
else:
	with open('dataBase.json','r')as r:
		dataBase=json.load(r)
		users=dataBase["users"]
		db = dataBase["manga-cach"]


	
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
	#await add_user(dataBase,m.chat.id)
	mmsg = await m.reply("Wait for Getting your chapter...")
	
	
	if (len(m.text)==6 and len(m.text.split(' '))!=3):
		return await m.reply("/manga <رقم الفصل> <اسم المانجا>")
		log(f'Manga Command; data: Null: User:{m.from_user.id}')
	elif len(re.findall(r"\d",m.text.split(" ")[2]))==0:
		return await m.reply("/manga <رقم الفصل> <اسم المانجا>\n                                   ^^^^^^^^^^^\nيجب ان يكون رقم، مثل: 13")
	log(f"Manga Command; data:{m.text.split(' ')[1]}\\{m.text.split(' ')[1]};User:{m.from_user.id}")
	await button_message(c=c,query={
		"manga":m.text.lower().split(" ")[1],
		"chapter_number":m.text.split(" ")[2],
		"current_page":1,
		"message":m,
		"type":"send",
		"database":db
	})
	await mmsg.delete()

@c.on_callback_query()
async def inlineeQuery(cl:Client,q:CallbackQuery):
	print (f"  {q.data}")
	if q.data=="start:policy":
		await q.answer("كل الحقوق تابعة لمانجا العاشق™",show_alert=False)
	if q.data.startswith('PageChange@') :
		print(q.data) # PageChange@berserk:13#2
		q.data=q.data.replace("PageChange@",'')
		data_=q.data.lower().split('#')
		data=data_[0].split(":")
		log(f"Page Change; data:{data[0]}\\{data[1]}\\{data_[1]}; User:{q.from_user.id}")
		await button_message(c=c,query={
			"manga":data[0],
			"chapter_number":data[1],
			"current_page":int(data_[1]),
			"message":q.message,
			"type":'edit',
			"Q":q,
			"database":db
		})
	if q.data.startswith("SearchResult@"):
		print(q.data)
		await showManga(client=c, query={
		"chat_id": q.message.chat.id,
		"manga-name": q.data.split("@")[1].replace("-"," ")
		})
	if q.data.startswith("selectMangaChapter@"):
		print(q.data)
		#await q.message.delete()
		msg=await q.message.chat.ask("Send Chapter Number:",filters=filters.text)
	# button_message(query:dict,c:pyrogram.Client)
		await msg.request.edit_text( "SetUp the chapter..." )
		await button_message(c=c,query={
"manga":q.data.split("@")[1],
"chapter_number":msg.text,
"current_page":1,
"type":"send",
"message":q.message,
"database": db,
"Q":q
}
	   )
		await msg.request.delete()
	

@c.on_message(filters.command(
	commands='search' , prefixes=''
))
async def SearchHandler(cl:c,m:Message):
	if m.text=='search':return(
		await m.reply_text('ضع قيمة للبحث')
	)
	await searchManga(
		query={
			'manga-name':m.text.lower().replace('search',''),
			'message':m,
			'type':'send'
		}, client=c
	)

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
	log("Bot is Runnig!")
	await idle()

if __name__=='__main__':
	loop = get_event_loop()
	threading.Thread(target=loop.run_until_complete(main()))
	with open("dataBase.json",'w') as datadumper:
		json.dump(dataBase,datadumper,indent=4)
	datadumper.close()
	log("bot has STOPED!")
