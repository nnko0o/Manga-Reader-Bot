# Made By @nnko0o in https://github.com/nnko0o/Manga-Reader-Bot
# BUI -> Button user interface
# A module for the BUI of the bot

from .utility import *
from .Manga3asq import *

from pyrogram.types import *
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from pykeyboard import InlineButton,InlineKeyboard


async def download(page,m:Message,c:pyrogram.Client):
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
		#os.remove(image) -> Delete the file from your storage /// that will make a bug,
		# TODO : make the returned data is the image no the path and delete the file ;
		return image
	else:print(" False");return 0

async def get_chapter(manga:str, chapter:any,db:dict) -> list :
	data_name=f"{manga}:{chapter}"
	print(data_name)
	

	try:
		if db[data_name]:return db[data_name]
		print(" .Use old chapter")

	except:
		print (" .Use New chapter")
		_3asq=Manga3asq()
		#search manga
		search = await _3asq.searchManga(manga)
		if search[0]=="not found":
			return("not found")
		chs = await _3asq.getChapters(url=search[0]['url'].split("=")[1])
		name = search[0]['url'].split("=")[1].split("/")[-2]
		url=search[0]['url'].split("=")[1]
		ch = await _3asq.getPagesFromChapter(f"{url}{chapter}/")

		db[data_name]=ch
		result=db[data_name]
		#async with aiofiles.open("dataBase.json",'w') as file:
		#	await file.write(f"{json.dumps(obj=dataBase,)}")
		#file.close()
		return result

async def button_message(query:dict,c:pyrogram.Client):
	manga_name=query["manga"]
	chapter=query["chapter_number"]
	page_ = query["current_page"]
	message: Message=query["message"]
	db: dict = query["database"]
	try:q:CallbackQuery=query["Q"]
	except:pass
	chapter_:list = []
	PageImage='https://img.freepik.com/free-vector/404-error-with-landscape-concept-illustration_114360-7888.jpg?w=2000'
	if page_!=0: page_-=1
	
	try:
		if db[f"{manga_name}:{chapter}"][page_][2]:
			PageImage = db[f"{manga_name}:{chapter}"][page_][2]
			chapter_ = db[f"{manga_name}:{chapter}"]
			print("  .Used File_id")
	except:
		print (" .Used New Without File_id")
		chapter_=await get_chapter(manga_name,chapter,db)
		print(chapter_,len(chapter))
		if chapter_=="not found":
			return(await message.reply_text(
			text="عذراً، المانجا التي تريدها غير موجودة."
			))
		if chapter_=="Index Error":return(
		await message.reply_text("عذراً، هذا الفصل غير متوفر.")
		)
		print(chapter_);print(f"\n**{chapter_}**\n")
		print (type(page_))
		PageImage=chapter_[page_][0]
		print(f" {chapter_[page_]}\n ")
		PageImage_=await download(m=message,page=chapter_[page_],c=c)
		if PageImage_!=0:PageImage=PageImage_
		print(PageImage_)
		
	print (f" * {len(chapter_)}\n * {page_+1}")
	#text= "رد على الصفحه بكلمة ملف سيرجع لك الصفحه بصيغة ملف"
	keyboard = InlineKeyboard()
	keyboard.paginate(
	  count_pages=len(chapter_)
	, current_page=page_+1
	, callback_pattern=f"PageChange@{manga_name}:{chapter}"+'#{number}'
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
	
	Page_FileId = await get_file_id_by_message_id(client=c,chat_id=msg.chat.id,Message_id=msg.id)
	if len(db[f"{manga_name}:{chapter}"][page_])==2:
		db[f"{manga_name}:{chapter}"][page_].append(Page_FileId)

async def searchManga(
	query:dict,
	client:pyrogram.client
):
	# Get argemnts from query
	MangaName:str = query['manga-name']
	message:Message = query['message']
	Type:str = query["type"]
	# Search the manga
	if Type=='send':
		_3asq = Manga3asq()
		SearchData:list = await _3asq.searchManga(searchQeury=MangaName)
		print(MangaName,SearchData)
		if SearchData[0]=="not found":
			return(await message.reply_text('عذراً, لا توجد مانجا بهذا الأسم'))
		loop_time:int = 5
		if len(SearchData)<=5:
			loop_time = len(SearchData)
		result_keyboard = InlineKeyboard(row_width=2)
		i = 0
		for index in SearchData:
			print(index)
			if i==loop_time:break
			i += 1
			result_keyboard.row(InlineButton(
				text=index["title"],
				callback_data=f"SearchResult@{index['url'].split('=')[1].split('/')[-2]}"
				# https://3asq.org/manga/Name/
#				            12              3            4           5
#				            -4,5           -3            -2           -1
			))
			
		print(' SSSSSSSS')
		return await message.reply_text('results:',reply_markup=result_keyboard)
async def showManga(
	client:pyrogram.Client,
	query:dict
	):
	MangaData = await getMangaDetiles(
		MangaURL="https://3asq.org/manga/"+query ["manga-name"]+'/'
	)
	KeyBoard = InlineKeyboard(row_width=1)
	KeyBoard.add(
	
	    InlineButton( 
		"Link", url="https://3asq.org/manga/"+query ["manga-name"]+'/' ),
		InlineButton(
	"Select Chapter", 
	callback_data=f'selectMangaChapter@'+query ["manga-name"]))
	print(query["manga-name"])
	return (await client.send_photo(
  	chat_id = query ["chat_id"]
    , photo=MangaData["cover"]
	, caption=f"""
Manga Name: {MangaData['title']}
auther: {MangaData['auther']}
artis: {MangaData['artis']}
Story: / {MangaData['story']}
	"""
	, reply_markup= KeyBoard
	
	))