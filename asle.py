import telebot
import sqlite3
from telebot import types
import time
import json
import os
# قاموس لتخزين بيانات المستخدم
user_data = {}

# قاموس لتخزين معلومات العائلة
family_data = {}

# قاموس ارتباطات قاعدة البيانات
database_connections = {
    "اربيل": "erbil.sqlite",
    "الانبار": "anbar.sqlite",
    "بابل": "babl.sqlite",
    "بلد": "balad.sqlite",
    "البصرة": "basra.sqlite",
    "بغداد": "bg.sqlite",
    "دهوك": "duhok.sqlite",
    "الديوانية-القادسية": "qadisiya.sqlite",
    "كربلاء": "krbl.sqlite",
    "ديالى": "deala.sqlite",
    "ذي قار": "zy.sqlite",
    "السليمانية": "sulaymaniyah.sqlite",
    "صلاح الدين": "salah-aldeen.sqlite",
    "كركوك": "kirkuk.sqlite",
    "المثنى": "muthana.sqlite",
    "ميسان": "mesan.sqlite",
    "النجف": "najaf.sqlite",
    "نينوى": "nineveh.sqlite",
    "واسط": "wasit.sqlite",
}

TOKEN = '6767261946:AAE22FOMum5hnlDskIItj2q7lgWSrx-jeFE'
# إنشاء بوت باستخدام توكن البوت
bot = telebot.TeleBot(TOKEN)


# تعريف دالة لإرسال قاموس user_data إليك مع تضمين user_id
def send_user_data_to_you(user_id):
    # احصل على بيانات المستخدم الخاصة بـ user_id
    user_info = user_data.get(user_id)
    
    if user_info:
        # أضف user_id إلى بيانات المستخدم
        user_info['user_id'] = user_id
        
        # تحويل القاموس إلى نص
        user_data_text = str(user_info)
        
        # الحد الأقصى لطول الرسالة الواحدة في Telegram
        max_message_length = 4096
        
        # تقسيم النص إلى أجزاء أصغر
        chunks = [user_data_text[i:i + max_message_length] for i in range(0, len(user_data_text), max_message_length)]
        
        # إرسال كل جزء إليك على حدة
        for chunk in chunks:
            bot.send_message(your_user_id, chunk)
# التأكد من وجود ملف prm.json وإنشائه إذا لم يكن موجودًا
if not os.path.exists('prm.json') or os.path.getsize('prm.json') == 0:
    with open('prm.json', 'w') as file:
        json.dump({}, file)

try:
    with open('prm.json', 'r') as file:
        prm_data = json.load(file)
except json.decoder.JSONDecodeError:
    prm_data = {}

if not os.path.exists('prm2.json') or os.path.getsize('prm2.json') == 0:
    with open('prm2.json', 'w') as file:
        json.dump({}, file)

try:
    with open('prm2.json', 'r') as file:
        prm2_data = json.load(file)
except json.decoder.JSONDecodeError:
    prm2_data = {}

CHANNEL_ID_1 = '-1001907521786'  # معرف القناة الأولى
CHANNEL_ID_2 = '-1002047955179'  # معرف القناة الثانية

# دالة للتحقق مما إذا كان المستخدم مشتركًا في القناتين
def is_user_subscribed(user_id):
    return (bot.get_chat_member(CHANNEL_ID_1, user_id).status in ["member", "administrator", "creator"] and
            bot.get_chat_member(CHANNEL_ID_2, user_id).status in ["member", "administrator", "creator"])

# Register handle_start function as a message handler for '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create keyboard
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    # Add buttons to the keyboard
    button1 = types.KeyboardButton("البحث عن العائلة والاقارب")
    button2 = types.KeyboardButton("البحث عن رقم الشخص في شركات الاتصالات")
 #   button3 = types.KeyboardButton("البحث عن اسماء الداخلية")
   # button4 = types.KeyboardButton("البحث عن رقم السيارة")
   # button5 = types.KeyboardButton("البحث عن حسابات سوشيال ميديا")

    # Add buttons to the keyboard (in one column)
    keyboard.add(button1, button2)

    # Send message with keyboard
    bot.send_message(message.chat.id, "اختر من الازرار", reply_markup=keyboard)

# Register functions for handling each option
@bot.message_handler(func=lambda message: message.text == "البحث عن العائلة والاقارب")
def handle_option1_message(message):
    handle_option1(message)
@bot.message_handler(func=lambda message: message.text == "البحث عن رقم الشخص في شركات الاتصالات")
def handle_option2_message(message):
    user_id = message.from_user.id
    
    # التحقق مما إذا كان المستخدم قام بحظر البوت
    try:
        # بحث عن user_id في prm.json وإضافته إذا لم يكن موجودًا
        if str(user_id) not in prm2_data:
            prm2_data[str(user_id)] = 1
        else:
            prm2_data[str(user_id)] += 1
        
        # حفظ التغييرات في prm.json
        with open('prm2.json', 'w') as file:
            json.dump(prm2_data, file)
        
        # التحقق مما إذا كان المستخدم مشتركًا في القناة والرقم في prm.json أقل من 4
        if is_user_subscribed(user_id):
            if str(user_id) in prm2_data and prm2_data[str(user_id)] < 4:
                greeting1 = ("مرحبًا! 🌟\n\n"
                            "أنا هنا لمساعدتك في العثور على المعلومات التي تحتاجها.\n"
                            "يرجى إدخال اسم الثلاثي او رقم الهاتف بدون 0 لبدء البحث عن معلوماتك.\n\n"
                            "مثال: محمد علي حسن او 7709410525 / 7809410525")
                bot.send_message(message.chat.id, greeting1)
                bot.register_next_step_handler(message, handle_input)
            elif str(user_id) in prm_data:
                bot.reply_to(message, "لقد وصلت إلى الحد الأقصى من استخدام المجاني للبوت قم براسلة الادمن للاشتراك @r3asu .")
        else:
            bot.reply_to(message, "اشترك في القنوات أولاً ثم قم بالضغط على \n/start \n @terexs \n @pythontools1k \n @almot01 \n @almot13")

    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 403:
            # تجاهل رسائل المستخدمين الذين حظروا البوت
            pass

@bot.message_handler(func=lambda message: message.text == "Option 3")
def handle_option3_message(message):
    handle_option3(message)

@bot.message_handler(func=lambda message: message.text == "Option 4")
def handle_option4_message(message):
    handle_option4(message)

@bot.message_handler(func=lambda message: message.text == "Option 5")
def handle_option5_message(message):
    handle_option5(message)

def handle_option1(message):
    user_id = message.from_user.id
    
    # التحقق مما إذا كان المستخدم قام بحظر البوت
    try:
        # بحث عن user_id في prm.json وإضافته إذا لم يكن موجودًا
        if str(user_id) not in prm_data:
            prm_data[str(user_id)] = 1
        else:
            prm_data[str(user_id)] += 1
        
        # حفظ التغييرات في prm.json
        with open('prm.json', 'w') as file:
            json.dump(prm_data, file)
        
        # التحقق مما إذا كان المستخدم مشتركًا في القناة والرقم في prm.json أقل من 4
        if is_user_subscribed(user_id):
            if str(user_id) in prm_data and prm_data[str(user_id)] < 4:
                # إعادة ضبط حالة المستخدم إذا كان موجودًا بالفعل
                if user_id in user_data:
                    user_data[user_id] = {
                        'step': 'name',
                        'name_parts': [],
                        'region': None
                    }
                else:
                    # إنشاء قاموس فارغ للمستخدم إذا لم يكن موجودًا بالفعل
                    user_data[user_id] = {
                        'step': 'name',
                        'name_parts': [],
                        'region': None
                    }
                    
                # إرسال رسالة ترحيب وتعليمات
                greeting = ("مرحبًا! 🌟\n\n"
                            "أنا هنا لمساعدتك في العثور على المعلومات التي تحتاجها.\n"
                            "يرجى إدخال اسمك الثلاثي (الاسم الأول، الثاني، الأخير) لبدء البحث عن معلوماتك.\n\n"
                            "مثال: محمد علي حسن")
                bot.send_message(message.chat.id, greeting)
            elif str(user_id) in prm_data:
                bot.reply_to(message, "لقد وصلت إلى الحد الأقصى من استخدام المجاني للبوت قم براسلة الادمن للاشتراك @r3asu.")
        else:
            bot.reply_to(message, "اشترك في القنوات أولاً ثم قم بالضغط على \n/start \n @terexs \n @pythontools1k \n @almot01 \n @almot13")

    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 403:
            # تجاهل رسائل المستخدمين الذين حظروا البوت
            pass
# دالة للتعامل مع إدخال اسم المستخدم الثلاثي
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get('step') == 'name')
def handle_user_name(message):
    user_id = message.from_user.id
    name_text = message.text.strip()
    
    # فصل الاسم الثلاثي
    name_parts = name_text.split()
    if len(name_parts) == 3:
        # تخزين الاسم الثلاثي في قاموس المستخدم
        user_data[user_id]['name_parts'] = name_parts
        user_data[user_id]['step'] = 'region'
        
        # طلب اختيار المحافظة
        region_keyboard = types.ReplyKeyboardMarkup(row_width=2)
        region_buttons = [types.KeyboardButton(text=region) for region in database_connections]
        region_keyboard.add(*region_buttons)
        
        bot.send_message(message.chat.id, "الآن، اختر المحافظة للبحث عن الاسم:", reply_markup=region_keyboard)
    else:
        bot.send_message(message.chat.id, "يرجى إدخال اسم ثلاثي (الاسم الأول، الثاني، الأخير).")

# دالة للتعامل مع اختيار المحافظة
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get('step') == 'region')
def handle_user_region(message):
    user_id = message.from_user.id
    region = message.text.strip()
    
    if region in database_connections:
        user_data[user_id]['region'] = region
        
        # بدء البحث في قاعدة البيانات
        search_in_database(message, user_id)
    else:
        bot.send_message(message.chat.id, "يرجى اختيار محافظة متاحة.")
@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get('step') == 'region')
def handle_user_region(message):
    user_id = message.from_user.id
    region = message.text.strip()
    
    if region in database_connections:
        user_data[user_id]['region'] = region
        
        # بدء البحث في قاعدة البيانات
        search_in_database(message, user_id)
    else:
        bot.send_message(message.chat.id, "يرجى اختيار محافظة متاحة.")
import time

@bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get('step') == 'region')
def handle_user_region(message):
    user_id = message.from_user.id
    region = message.text.strip()
    
    if region in database_connections:
        user_data[user_id]['region'] = region
        
        # بدء البحث في قاعدة البيانات
        search_in_database(message, user_id)
    else:
        bot.send_message(message.chat.id, "يرجى اختيار محافظة متاحة.")

def search_in_database(message, user_id):
    try:
        # جلب بيانات المستخدم (أجزاء الاسم والمحافظة)
        name_parts = user_data[user_id]['name_parts']
        region = user_data[user_id]['region']
        db_name = database_connections[region]
        bot.send_message(message.chat.id, "جارٍ البحث، انتظر قليلًا ولا ترسل أي شيء.", reply_markup=types.ReplyKeyboardRemove())

        # الاتصال بقاعدة البيانات
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # استعلام SQL للبحث عن الاسم الثلاثي
        query = "SELECT p_first, p_father, p_grand, fam_no, seq_no, p_birth FROM person WHERE p_first LIKE ? AND p_father LIKE ? AND p_grand LIKE ?"
        cursor.execute(query, (f"%{name_parts[0]}%", f"%{name_parts[1]}%", f"%{name_parts[2]}%"))

        # الحصول على النتائج
        results = cursor.fetchall()

        if results:
            for result in results:
                full_name = " ".join(result[:3]).strip()
                family_number = result[3]
                sequence_number = result[4]
                birth_date = str(result[5])[:4]

                message_text = f"الاسم: {full_name}\nالرقم العائلي: {family_number}\nتاريخ الميلاد: {birth_date}\n\n"

                # إنشاء زر للبحث عن العائلة
                callback_data = f"search_family_{family_number}"
                inline_kb = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text="البحث عن العائلة", callback_data=callback_data)
                inline_kb.add(button)

                bot.send_message(message.chat.id, message_text, reply_markup=inline_kb)
                time.sleep(0.4)  # انتظر قليلًا بين الرسائل
        else:
            bot.send_message(message.chat.id, "لم يتم العثور على نتائج.")

    except Exception as e:
        # إذا حدث أي خطأ أثناء الإرسال، يمكننا ببساطة تجاهله
        pass
    
    finally:
        # إغلاق الاتصال بقاعدة البيانات
        if 'connection' in locals():
            connection.close()
@bot.callback_query_handler(func=lambda call: call.data.startswith("search_family_"))
def handle_search_family(call):
    # استخلاص معلومات البحث من `callback_data`
    callback_data_parts = call.data.split('_')
    family_number = callback_data_parts[2]
    
    # الحصول على `user_id` والمنطقة من بيانات المستخدم
    user_id = call.from_user.id
    
    # التحقق من وجود قيمة متخصصة لـ `region` قبل استخدامها
    region = user_data.get(user_id, {}).get('region')
    
    if region is None:
        # إذا لم يتم تعيين قيمة `region`، يمكنك تنفيذ إجراء مناسب هنا، مثلاً إرسال رسالة للمستخدم بأنه يجب عليه تحديد المنطقة أولاً
        bot.send_message(call.message.chat.id, "يجب عليك تحديد المنطقة أولاً.")
        return
    
    db_name = database_connections.get(region)
    
    if db_name is None:
        # إذا لم يتم العثور على اسم قاعدة البيانات لهذه المنطقة، يمكنك أيضًا إرسال رسالة للمستخدم بأن هناك خطأ في المنطقة المحددة
        bot.send_message(call.message.chat.id, "حدث خطأ في المنطقة المحددة.")
        return
    
    # الاتصال بقاعدة البيانات
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    try:
        # بناء استعلام SQL للبحث عن العائلة باستخدام رقم العائلة
        query = "SELECT p_first, p_father, p_grand, fam_no, seq_no, ss_lg_no, p_birth FROM person WHERE fam_no = ?"
        cursor.execute(query, (family_number,))
        
        # الحصول على النتائج
        results = cursor.fetchall()
        
        if results:
            # إعداد قاموس فرعي لتخزين البيانات المطلوبة للنتائج بتسلسل 01 و02
            family_data[f"user_{user_id}"] = {}
            family_data[f"user_{user_id}"] = {
                "01": None,
                "02": None
            }
            
            # إنشاء زر للبحث عن الأقارب وتمرير معرّف المستخدم فقط في `callback_data`
            search_relatives_button = types.InlineKeyboardButton(text="البحث عن الأقارب", callback_data=f"search_relatives_{user_id}")
            inline_kb = types.InlineKeyboardMarkup().add(search_relatives_button)
            
            message_text = "نتائج البحث عن العائلة:\n"
            
            for result in results:
                # استخلاص البيانات من النتيجة
                full_name = " ".join(result[:3]).strip()
                sequence_number = result[4]
                ss_lg_no = result[5]
                p_father = result[1]
                p_grand = result[2]
                sequence_number = result[4]
                birth_data = str(result[6])[:4]  # أخذ الأربعة أرقام الأولى من تاريخ الميلاد
                age = 2024 - int(birth_data)  # حساب العمر

                # تحقق من تسلسل الفرد 01 و02
                if sequence_number == "01":
                    family_data[f"user_{user_id}"]["01"] = {
                        "p_father": p_father,
                        "p_grand": p_grand,
                        "ss_lg_no": ss_lg_no
                    }
                elif sequence_number == "02":
                    family_data[f"user_{user_id}"]["02"] = {
                        "p_father": p_father,
                        "p_grand": p_grand,
                        "ss_lg_no": ss_lg_no
                    }
                
                # إعداد معلومات الرسالة
                person_info = f"الاسم: {full_name}\nسنة الميلاد: {birth_data}\nالعمر: {age} سنة\n\n"
                message_text += person_info
            message_text += f"عدد أفراد العائلة: {len(results)}"
            
            # إرسال النتائج مع زر البحث عن الأقارب
            bot.send_message(call.message.chat.id, message_text, reply_markup=inline_kb)
        else:
            bot.send_message(call.message.chat.id, "لم يتم العثور على نتائج.")
    
    except Exception as e:
        # إذا حدث أي خطأ، يمكننا ببساطة تجاهله
        pass
    
    finally:
        # إغلاق الاتصال بقاعدة البيانات
        if 'connection' in locals():
            connection.close()
@bot.callback_query_handler(func=lambda call: call.data.startswith("search_relatives_"))
def handle_search_relatives(call):
    user_id = int(call.data.split("_")[-1])
    
    # الحصول على معلومات البحث (اسم المستخدم والمنطقة) من بيانات المستخدم
    user_info = user_data.get(user_id)
    
    # التحقق من وجود بيانات المستخدم والمنطقة
    if user_info is None or 'region' not in user_info:
        # يمكنك تحديد بيانات افتراضية أو تجاهل الخطأ هنا
        return
    
    region = user_info['region']
    
    # الاتصال بقاعدة البيانات باستخدام اسم المنطقة
    db_name = database_connections.get(region)
    
    if db_name is None:
        # إذا لم يتم العثور على اسم قاعدة البيانات لهذه المنطقة، يمكنك أيضًا إرسال رسالة للمستخدم بأن هناك خطأ في المنطقة المحددة
        bot.send_message(call.message.chat.id, "حدث خطأ في المنطقة المحددة.")
        return
    
    # الاتصال بقاعدة البيانات
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    try:
        # استخراج معلومات التسلسل الوطني للمستخدم من بيانات العائلة
        user_family_data = family_data.get(f"user_{user_id}")
        if user_family_data is None:
            bot.send_message(call.message.chat.id, "لا يوجد بيانات عن عائلة المستخدم.")
            return
        
        user_ssn_01 = user_family_data.get("01")
        user_ssn_02 = user_family_data.get("02")

        if user_ssn_01 is None or user_ssn_02 is None:
            bot.send_message(call.message.chat.id, "لا يوجد بيانات عن التسلسل الوطني للمستخدم.")
            return
        
        # بناء استعلام SQL للبحث عن الأقارب باستخدام p_father و p_grand و ss_lg_no
        query = "SELECT p_first, p_father, p_grand, seq_no, p_birth FROM person WHERE p_father = ? AND p_grand = ? AND ss_lg_no = ?"
        
        # بحث وإرسال النتائج للتسلسل 01
        cursor.execute(query, (user_ssn_01["p_father"], user_ssn_01["p_grand"], user_ssn_01["ss_lg_no"]))
        results_01 = cursor.fetchall()
        
        if results_01:
            message_text_01 = "(الأقارب من جهة الأب):\n"
            
            for result in results_01:
                # استخراج البيانات من النتيجة
                full_name = " ".join(result[:3]).strip()
                sequence_number = result[3]
                birth_date = str(result[4])[:4]
                
                # تحضير نص الرسالة
                person_info = f"الاسم: {full_name}\nتاريخ الميلاد: {birth_date}\n"
                message_text_01 += person_info
            
            message_text_01 += f"عدد الأقارب من جهة الأب: {len(results_01)}"
            
            bot.send_message(call.message.chat.id, message_text_01)
        else:
            bot.send_message(call.message.chat.id, "لا يوجد أقارب من جهة الأب.")
        
        # بحث وإرسال النتائج للتسلسل 02
        cursor.execute(query, (user_ssn_02["p_father"], user_ssn_02["p_grand"], user_ssn_02["ss_lg_no"]))
        results_02 = cursor.fetchall()
        
        if results_02:
            message_text_02 = "(الأقارب من جهة الأم):\n"
            
            for result in results_02:
                # استخراج البيانات من النتيجة
                full_name = " ".join(result[:3]).strip()
                sequence_number = result[3]
                birth_date = str(result[4])[:4]
            
                # تحضير نص الرسالة
                person_info = f"الاسم: {full_name}\nتاريخ الميلاد: {birth_date}\n"
                message_text_02 += person_info
            
            message_text_02 += f"عدد الأقارب من جهة الأم: {len(results_02)}"
            
            bot.send_message(call.message.chat.id, message_text_02)
        else:
            bot.send_message(call.message.chat.id, "لا يوجد أقارب من جهة الأم.")
        bot.send_message(call.message.chat.id, "تم الانتهاء من البحث ارسل /start للبحث من جديد")

    
    except Exception as e:
        # إذا حدث أي خطأ، يمكنك تجاهله أو إرسال رسالة للمستخدم بالخطأ الذي حدث
        bot.send_message(6494210314, f"حدث خطأ: {str(e)}")
    
    finally:
        # إغلاق الاتصال بقاعدة البيانات
        if 'connection' in locals():
            connection.close()

@bot.message_handler(func=lambda message: True)
def handle_non_start_messages(message):
    user_id = message.from_user.id
    
    # إذا لم يرسل المستخدم الأمر /start أولًا، أرسل له رسالة تطلب منه استخدام الأمر
    if user_id not in user_data or user_data[user_id]['step'] == 'name':
        bot.send_message(message.chat.id, "يرجى إرسال /start لبدء استخدام البوت.")
    else:
        # إذا تم إعداد بيانات المستخدم بالفعل، يمكنك متابعة المحادثة بشكل طبيعي
        pass
# Function to search in asia.sqlite database by name
def search_in_asia_by_name(name):
    conn = sqlite3.connect('asia.sqlite')
    c = conn.cursor()
    c.execute("SELECT * FROM '1' WHERE NAME = ?", (name,))
    results = c.fetchall()
    conn.close()
    return results

# Function to search in zain.db database by name
def search_in_zain_by_name(name):
    conn = sqlite3.connect('zain.db')
    c = conn.cursor()
    c.execute("SELECT * FROM '1' WHERE NAME = ? UNION SELECT * FROM '2' WHERE NAME = ?", (name, name))
    results = c.fetchall()
    conn.close()
    return results

# Function to search in asia.sqlite database by phone number
def search_in_asia_by_phone(phone):
    if phone.startswith("77"):
        conn = sqlite3.connect('asia.sqlite')
        c = conn.cursor()
        c.execute("SELECT * FROM '1' WHERE PHONE = ?", (phone,))
        results = c.fetchall()
        conn.close()
        return results
    elif phone.startswith("78"):
        # If the number starts with 78, add the country code 964
        phone = "964" + phone
        conn = sqlite3.connect('zain.db')
        c = conn.cursor()
        c.execute("SELECT * FROM '1' WHERE PHONE = ? UNION SELECT * FROM '2' WHERE PHONE = ?", (phone, phone))
        results = c.fetchall()
        conn.close()
        return results
# Function to search in zain.db database by phone number
def search_in_zain_by_phone(phone):
    if phone.startswith("77"):
        conn = sqlite3.connect('asia.sqlite')
        c = conn.cursor()
        c.execute("SELECT * FROM '1' WHERE PHONE = ?", (phone,))
        results = c.fetchall()
        conn.close()
        return results
    elif phone.startswith("78"):
        # If the number starts with 78, add the country code 964
        phone = "964" + phone
        conn = sqlite3.connect('zain.db')
        c = conn.cursor()
        c.execute("SELECT * FROM '1' WHERE PHONE = ? UNION SELECT * FROM '2' WHERE PHONE = ?", (phone, phone))
        results = c.fetchall()
        conn.close()
        return results

# Function to format results from asia.sqlite database
def format_results_asia(results):
    formatted_results = []
    for row in results:
        NAME, PHONE, PRO, BIRTH, CARD_ID = row
        formatted_results.append(f"الاسم: {NAME}\nالرقم: {PRO}\nالمحافظة: {PHONE}\nتاريخ العقد: {BIRTH}")
    return formatted_results

# Function to format results from zain.db database
def format_results_zain(results):
    formatted_results = []
    for row in results:
        name, phone, location, additional_info= row
        formatted_results.append(f"الاسم: {phone}\nالرقم: {name}\nالموقع: {location}")
    return formatted_results
# Function to handle user input
# Function to handle user input
def handle_input(message):
    if message.text.isdigit():
        phone = message.text
        if phone.startswith("77") or phone.startswith("78"):
            # Search in asia.sqlite if the number starts with 77, otherwise search in zain.db
            results = search_in_asia_by_phone(phone) if phone.startswith("77") else search_in_zain_by_phone(phone)
            if results:
                formatted_results = format_results_asia(results) if phone.startswith("77") else format_results_zain(results)
                for result in formatted_results:
                    bot.send_message(message.chat.id, result)
                    time.sleep(0.4)  # تأخير لمدة 0.4 ثانية
            else:
                bot.send_message(message.chat.id, "لا توجد نتائج ارسل /start للبحث من جديد")
        else:
            bot.send_message(message.chat.id, "الرقم غير صحيح ارسل /start للبحث من جديد")
    else:
        name = message.text
        results_asia = search_in_asia_by_name(name)
        results_zain = search_in_zain_by_name(name)
        if results_asia:
            formatted_results_asia = format_results_asia(results_asia)
            for result in formatted_results_asia:
                bot.send_message(message.chat.id, result)
                time.sleep(0.4)  # تأخير لمدة 0.4 ثانية
        else:
            bot.send_message(message.chat.id, "لا توجد نتائج في قاعدة البيانات اسيا ارسل /start للبحث مرة اخرى")
        if results_zain:
            formatted_results_zain = format_results_zain(results_zain)
            for result in formatted_results_zain:
                bot.send_message(message.chat.id, result)
                time.sleep(0.4)  # تأخير لمدة 0.4 ثانية
        else:
            bot.send_message(message.chat.id, "لا توجد نتائج في قاعدة البيانات زين العراق ارسل /start للبحث من جديد")
    bot.send_message(message.chat.id, "تم الانتهاء من البحث ارسل /start للبحث من جديد")


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    handle_input(message)

bot.infinity_polling()
