# Made By @nnko0o in https://github.com/nnko0o/Manga-Reader-Bot

import httpx , aiohttp , aiofiles,os
from typing import List
from bs4 import BeautifulSoup
async def get_file_url_size(url:str):
	async with httpx.AsyncClient() as Client:
		haad = await Client.head(url=url)
		size = haad.headers["content-length"]
	return size

async def download_image(url:str,path:str,name:str):
	async with aiohttp.ClientSession() as session:
	    url = f"{url}"
	    print(f" {url}")
	    async with session.get(url) as resp:
	        if resp.status == 200:
	            #fi=open(f"{path}/{name}","w+");fi.close()
	            f = await aiofiles.open(path+"/"+name, mode='wb')
	            await f.write(await resp.read())
	            await f.close()
	return f"{path}/{name}"

async def download_images(images:List,path:str):
	for image in images: await download_image(image,path,image.split("/")[-1])

class Manga3asq:
    
    """A class for scrap 3asq.org"""
    
    BaseURL= "https://3asq.org/"
        
    async def _request(self,url:str,parms:dict={}):
        """Return response"""
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url,params=parms,)
        return response 
	
    async def searchManga(self,searchQeury:str):
        searchQeury = searchQeury.replace(" ",'+')
        url = self.BaseURL+'wp-admin/admin-ajax.php';
        data_ = f"action=wp-manga-search-manga&title={searchQeury}"
        async with httpx.AsyncClient() as Client:
            r= await Client.post(url=url,data=data_,headers={
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://3asq.org',
        'referer': 'https://3asq.org/?s=Hero&post_type=wp-manga',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        })
        print(r)
        data = [url['url'] for url in r.json()['data']]
        data_title = [url['title'] for url in r.json()['data']]
        data_link = ['https://3asq.deta.dev/api/fetch?link='+link for link in data ]
        data_manga = [{'title': a,'url': b,} for a ,b in zip(data_title,data_link)]
        return data_manga

    async def getChapters(self,url:str):
	    manga_name = url.split('/')[4]
	    new_link = 'https://3asq.org/manga/'+manga_name+'/ajax/chapters/'
	    async with httpx.AsyncClient() as requests:
	    	r = await requests.post(new_link,headers={
	        'accept': '*/*',
	        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	        'origin': 'https://3asq.org',
	        'referer': 'https://3asq.org/manga/'+manga_name+'/',
	        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
	    })
	    tree = BeautifulSoup(r.text, 'html.parser')
	    data_link = [child for child in tree.findAll("li", {"class":"wp-manga-chapter"})]
	    data_date = [child for child in tree.findAll("span", {"class":"chapter-release-date"})]
	    links_data = [link.find('a')['href'] for link in data_link]
	    date_release = [link.find('i').text for link in data_date]
	    links = ['https://3asq.deta.dev/api/dl?link='+link for link in links_data]
	    all_link = dict(enumerate(links, start=1))
	    return all_link

    async def getPagesFromChapter(self,link:str):
        async with httpx.AsyncClient() as requests: 
            page = await requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        image_data = [child['src'] for child in soup.findAll("img", {"class":"wp-manga-chapter-img"})]
        image_links = [link.strip() for link in image_data]
        result = []
        for page in image_links:
        	size_=await get_file_url_size(url=page)
        	result.append([page,size_])
        return result
    async def get_ch(self,
    manga_name:str,
    chapter_number:int,
    ) -> List:
    	"""enter manga chapter return pages
Arguments:
manga_name String -> just the name (not in link name)
chapter_number Int -> the chapter number
Return:
List of pages link <List class <str class>> 
"""
    	search = await self.searchManga(searchQeury=manga_name.lower());
    	link = search[0]['url'].split('=')[1];
    	chapters = await self.getChapters(url=link);
    	print("chapters\n",chapters)
    	print(chapter_number)
    	chapter = chapters[9];
    	chapter_link = chapter.split("=")[1]
    	print(chapter_link)
    	Pages = await self.getPagesFromChapter(link=chapter_link)
    	
    	return Pages #list of string "link of pages"
