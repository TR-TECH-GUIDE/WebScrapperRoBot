# © SLBotsOfficial ™
# © TR-TECH-GUIDE
# 2021

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bs4 import BeautifulSoup
import requests
from telegraph.api import Telegraph
from script import script

SLBotsOfficial = Client(
    "WebScrapperBot",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)
telegraph = Telegraph(
    access_token=os.environ.get("TELEGRAPH_TOKEN", "dbc6169e9c7b4871fd681d87c80f5f5371fd59bff01dc95eca546cdb41a1")
)


@SLBotsOfficial.on_message(filters.command(["start"]))
async def start(_, message: Message):
    await message.reply_text("I can Scrape a website within seconds. Send me A website link and Get Your results now Want To Know More About Web Scraping? Read Help")  # Edit Your Start string here
                        reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("HELP", callback_data="help_data"),
                        InlineKeyboardButton("ABOUT", callback_data="about_data"),
                    ],
                    [
                        InlineKeyboardButton(
                            "⭕️ JOIN OUR CHANNEL ⭕️", url="https://t.me/SLBotsOfficial")
                    ]
                ]
            )
        
@SLBotsOfficial.on_message(filters.command(["help"]))
async def help(_, message: Message):
    await message.reply_text("Web scraping, web harvesting, or web data extraction is data scraping used for extracting data from websites. The web scraping software may directly access the World Wide Web using the Hypertext Transfer Protocol or a web browser.")

@SLBotsOfficial.on_message(filters.command(["about"]))
async def about(_, message):
    await message.reply_text(
            text=script.ABOUT_TEXT.format(message.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("BACK", callback_data="help_data"),
                        InlineKeyboardButton("START", callback_data="start_data"),
                    ],
                    [
                        InlineKeyboardButton(
                            "⭕️ JOIN OUR CHANNEL ⭕️", url="https://t.me/SLBotsOfficial")
                    ]
                ]
            )
    
@SLBotsOfficial.on_message((filters.regex("https") | filters.regex("http") | filters.regex("www")) & (filters.forwarded | filters.reply | filters.private))

async def scrapping(_, message: Message):
    txt = await message.reply_text("Validating Link", quote=True)
    try:  # Extracting Raw Data From Webpage ( Unstructured format)
        url = str(message.text)
        request = requests.get(url)
        await txt.edit(text=f"Getting Raw Data from {url}", disable_web_page_preview=True)
        file_write = open(f'RawData-{message.chat.username}.txt', 'a+')
        file_write.write(f"{request.content}")  # Writing Raw Content to Txt file
        file_write.close()
        await message.reply_document(f"RawData-{message.chat.username}.txt", caption="©@SLBotsOfficial", quote=True)
        os.remove(f"RawData-{message.chat.username}.txt")
        await txt.delete()
    except Exception as error:
        print(error)
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return
    try:
        txt = await message.reply_text(text=f"Getting HTML code from {url}", disable_web_page_preview=True, quote=True)
        soup = BeautifulSoup(request.content, 'html5lib')  # Extracting Html code in Tree Format
        file_write = open(f'HtmlData-{message.chat.username}.txt', 'a+')
        soup.data = soup.prettify()  # parsing HTML
        file_write.write(f"{soup.data}")  # writing data to txt
        file_write.close()
        await message.reply_document(f"HtmlData-{message.chat.username}.txt", caption="©@SLBotsOfficial", quote=True)
        os.remove(f"HtmlData-{message.chat.username}.txt")
        await txt.delete()
    except Exception as error:
        await message.reply_text(text=f"{error}", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return
    try:
        txt = await message.reply_text(f"Getting all Links from {url}", disable_web_page_preview=True, quote=True)
        file_write = open(f'AllLinks-{message.chat.username}.txt', 'a+')
        for link in soup.find_all('a'):  # getting all <a> tags in Html
            links = link.get('href')  # Extracting Href value of <a>
            file_write.write(f"{links}\n\n")  # writing links to txt file
        file_write.close()
        with open(f'AllLinks-{message.chat.username}.txt', "r") as file_text:
            telegraph_resp = telegraph.create_page(
                title="WebScrapperBot Data",
                author_name="WebScrapperBot",
                author_url="https://github.com/TR-TECH-GUIDE/WebScrapperRoBot",
                html_content=file_text.read()
            )
        await message.reply_document(
            f"AllLinks-{message.chat.username}.txt",
            caption="©@SLBotsOfficial",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Open in Telegraph", url=f"https://telegra.ph/{telegraph_resp['url']}")
            ]])
        )
        os.remove(f"AllLinks-{message.chat.username}.txt")
        await txt.delete()
    except Exception:
        await message.reply_text(text=f"No Links Found !!", disable_web_page_preview=True, quote=True)
        await txt.delete()

    try:
        txt = await message.reply_text(
            f"Getting all Paragraph from {url} ...",
            disable_web_page_preview=True,
            quote=True
        )
        file_write = open(f'AllParagraph-{message.chat.username}.txt', 'a+')
        paragraph = ""
        for para in soup.find_all('p'):  # Extracting all <p> tags
            paragraph = para.get_text()  # Getting Text from Paragraphs
            file_write.write(f"{paragraph}\n\n")  # writing to a file
        file_write.close()
        with open(f'AllLinks-{message.chat.username}.txt', "r") as file_text:
            telegraph_resp = telegraph.create_page(
                title="WebScrapperBot Data",
                author_name="WebScrapperBot",
                author_url="https://github.com/TR-TECH-GUIDE/WebScrapperRoBot",
                html_content=file_text.read()
            )
        await txt.delete()
        await message.reply_document(
            f"AllParagraph-{message.chat.username}.txt",
            caption="©@SLBotsOfficial",
            quote=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Open in Telegraph", url=f"https://telegra.ph/{telegraph_resp['url']}")
            ]])
        )
        os.remove(f"AllParagraph-{message.chat.username}.txt")
    except Exception:
        await message.reply_text(text="No Paragraphs Found !!", disable_web_page_preview=True, quote=True)
        await txt.delete()
        return
async def scrapping(bot,message):
 try:  # Extracting Raw Data From Webpage ( Unstructured format)
    txt = await message.reply_text("Validating Link")
    url=str(message.text)
    request = requests.get(url)
    await txt.edit(text=f"Getting Raw Data from {url}",disable_web_page_preview=True)
    with open(f'RawData-{message.chat.username}.txt', 'a+') as text_path:  
         file_write = open(f'RawData-{message.chat.username}.txt','a+')
         file_write.write(f"{request.content}") # Writing Raw Content to Txt file
         file_write.close
         await message.reply_document(f"RawData-{message.chat.username}.txt",caption="©@SLBotsOfficial")
         os.remove(f"RawData-{message.chat.username}.txt")
    await txt.delete()
 except Exception as error:
          print (error)
          await message.reply_text(text=f"{error}",disable_web_page_preview=True)            
          await txt.delete()
          return
 try:
    txt = await message.reply_text(text=f"Getting HTML code from {url}",disable_web_page_preview=True)
    soup = BeautifulSoup(request.content, 'html5lib') # Extracting Html code in Tree Format
    with open(f'HtmlData-{message.chat.username}.txt', 'a+') as text_path:
          file_write = open(f'HtmlData-{message.chat.username}.txt','a+')
          soup.data=soup.prettify()  # parsing HTML
          file_write.write(f"{soup.data}") # writing data to txt
          file_write.close
          await message.reply_document(f"HtmlData-{message.chat.username}.txt",caption="©@SLBotsOfficial")
          os.remove(f"HtmlData-{message.chat.username}.txt")
    await txt.delete()
 except Exception as error:
          await message.reply_text(text=f"{error}",disable_web_page_preview=True)            
          await txt.delete()
          return
 try:
    txt = await message.reply_text(f"Getting all Links from {url}",disable_web_page_preview=True)
    with open(f'AllLinks-{message.chat.username}.txt', 'a+') as text_path:
          file_write = open(f'AllLinks-{message.chat.username}.txt','a+')
          for link in soup.find_all('a'): # getting all <a> tags in Html
              links=link.get('href') # Extracting Href value of <a>
              file_write.write(f"{links}\n\n") # writing links to txt file
              file_write.close
          await message.reply_document(f"AllLinks-{message.chat.username}.txt",caption="©@SLBotsOfficial")
          os.remove(f"AllLinks-{message.chat.username}.txt")
    await txt.delete()
 except Exception as error:
          await message.reply_text(text="No Links Found !!",disable_web_page_preview=True)            
          await txt.delete()
          
 try:
    txt = await message.reply_text(f"Getting all Paragraph from {url}",disable_web_page_preview=True)
    with open(f'AllParagraph-{message.chat.username}.txt', 'a+') as text_path:
          file_write = open(f'AllParagraph-{message.chat.username}.txt','a+')
          paragraph=''
          for para in soup.find_all('p'): # Extracting all <p> tags
              paragraph=para.get_text() # Getting Text from Paragraphs
              file_write.write(f"{paragraph}\n\n") # writing to a file
              file_write.close
          await txt.delete()
          await message.reply_document(f"AllParagraph-{message.chat.username}.txt",caption="©@SLBotsOfficial")
          os.remove(f"AllParagraph-{message.chat.username}.txt")
          
          
 except Exception as error:
          await message.reply_text(text="No Paragraphs Found !!",disable_web_page_preview=True)            
          await txt.delete()
          return


# Use soup.find_all('tag_name') to Extract Specific Tag Details
"""
soup.title
# <title>The Dormouse's story</title>

soup.title.name
# u'title'

soup.title.string
# u'The Dormouse's story'

soup.title.parent.name
# u'head'
"""

SLBotsOfficial.run()
