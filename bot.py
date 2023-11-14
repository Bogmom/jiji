from openpyxl import load_workbook
import telebot,requests,pyodbc
from telebot import types
bot = telebot.TeleBot("6455603988:AAGq168mY4hFreAxawrnfLxWh_FDe94xwLs")
@bot.message_handler(commands=["start"])
def phone(message):
 x = open('pay.txt').read()
 key = types.InlineKeyboardMarkup()
 key.row_width = 3
 if str(message.from_user.id)== '6424203341':
    hk = types.InlineKeyboardMarkup()
    hk.row_width = 2
    ooi = open("pay.txt", "r")
    o = len(ooi.readlines())
    btn3 = types.InlineKeyboardButton(text=f"- عدد المفعلين {o} .",callback_data='nothing')
    btnn = types.InlineKeyboardButton(text="- تفعيل لشخص .",callback_data='tf')
    btn2 = types.InlineKeyboardButton(text="- ارسل التخزين .",callback_data="t5")
    hk.add(btn3,btn2,btnn)
    bot.reply_to(message,'- اهلا بك ايه المطور .',reply_markup=hk)
    bot.reply_to(message,'- اختر احد المحافظات واتبع التعليمات .',reply_markup=key)  
elif str(message.from_user.id) in x:
    bot.reply_to(message,'- اختر احد المحافظات واتبع التعليمات .',reply_markup=key)
else:
    huks = types.InlineKeyboardMarkup()
    huks.row_width = 1
    huka = types.InlineKeyboardButton(text="- Dev",url="t.me/m_is_m")
    huks.add(huka)
    bot.reply_to(message,'- صديقي انت لم يتم التفعيل لك يرجى مراسلة المطور \n- @m_is_m , @mhtr001',reply_markup=huks)
    imq = bot.forward_message(6424203341, message.chat.id, message.id)
    bot.reply_to(imq,f'- يحاول يبعبص ({message.from_user.id}) .')
@bot.callback_query_handler(func=lambda m:True)
def qu(call):
        x = open('pay.txt').read()
        if str(call.message.chat.id) in x or str(call.message.chat.id) == '6424203341':
         global place
         if call.data == 'tf':
            g= bot.send_message(call.message.chat.id,'- ارسل الايدي الي تريد تفعله .')
            bot.register_next_step_handler(g,hukss)
         if call.data == 't5':
            bot.send_document(call.message.chat.id, open('pay.txt','rb'))
        else:
         bot.answer_callback_query(call.id, f"- لاتبعبص لم يتم التفعيل لك .", show_alert=True)
def hukss(message):
 bot.reply_to(message,'انتظر من فضلك ...')
 open('pay.txt','a').write(f'{message.text}\n')
 bot.send_message(message.chat.id,f'- تم التفعيل بنجاح ل{message.text}')
def start(message):
    x = bot.reply_to(message, f"• مرحبًا بك في بوت قاعدة بيانات الجرائم ..\n• ارسل اسم المجرم الثلاثي .")
    bot.register_next_step_handler(x, search)
def search(message):
	name = message.text
	load = load_workbook("EC.xlsx", read_only=True)
	ws = load.active
	for row in ws.rows:
	   if str(name) in row[1].value:
	   	name = row[1].value
	   	location = row[2].value
	   	info = row[3].value
	   	family = row[4].value
	   	infoo = row[5].value
	   	lo = row[6].value
	   	ph = row[7].value
	   	phone = row[8].value
	   	Message = f"• الاسم : {name}\n• الموقع : {location}\n• معلومات : {info}\n• العائلة : {family}\n• معلومات اخرى : {infoo}\n• الموقع الناشر : {lo}\n• الرقم الاحصائي : {ph}\n• الهاتف : {phone}\n• المبرمج : @m_is_m"
	   	bot.reply_to(message, Message)
bot.infinity_polling()