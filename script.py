# pip install pyrogram tgcrypto
import asyncio
import re
import random
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

# ===== Конфигурация =====
API_ID = 23263318
API_HASH = "0ace1a6b260c0458ad8c78a5a8f950c2"
SESSION_NAME = "BADWALK"
TEXT_DEFAULT = "я твою мать ебу же свинорылые твари вы дюблять я же вашу нахуй родословную отберу в щепки вы ебучие свинья которых я отьбеубу просто в 0 просто дяоть буду ебать твою ебпную мать по кд и да слушай короче тут атаое дело случайно твою сестренку отьбепл и ей с лоу кика просто ебал мозг, лоу кик такой мощный что даже нахвй деревья ебалиь, а твой мозг это просто же пиздец я расхуряил с его с 1 удара ты же свин ебаный который йне хуя не может давай же сынок моего хкч иди выптздинт опять очередную рыгоьню я тебе же раз говорю нахуй я твою рыгьнюн в гарьнь втоец матери. засуну а я топором же перебашил ее в горло что там месево ебаное, с костей чисто вам супчик сварил вы это завали как шакалы ебаные, кстати да блять таой отец еще так любит хавать мыш яж потомуто. он же ебаное жаильное которое сосет мне хуй по кд потому что у тебя маи. шлбха, я буду просто нахуй сидеть на балкончике и пить кофе ты скорее сос своей мьаери не знаешь что атоке кофе напомню тебе я же тебе говорил 509 раз нахуй это твкоф напиток богов который ты не когда не попробуешь сынок поеботени ебаной, ты же просто будешь сосать мне хуй по 1 копейки за 109 лет чтобы тебе наупотит на кофе да даже на кружку тебе надо сосать мне хуй вечно б покдуа нахуй наша планета не взарваеться от моего хуя, давай же сынок хцйниубегай с моего хуя потому что же ты сынок пидораса даже нес можешь убежать а как ты убе бишь когда у тебя даже у сынка птдораса ногинаьу, тебе просто гранатой меьом разьебал ноги их асьаи твой отец забрал и кости с этого сделал ты же гидроцефал ебучий пиздаболлв просто кровь у тебя течет сынок выбоядлнчного двильного, че ты. тут сидишь высираешь сто ты дахуя сильный, у тебя же на аве смирительная рубашка твоей матери, нахуя она надо? так да она же не может от моего хуя даже прожить нахуй 2 минуты потому что ты же сынок поебони ебаной я тебе еще раз повторяю на всякий случай еще раз бомже текст я пойду к втоец матери ебало вбду ей вкалачивать просто в стенку чтобы там было ебаное месиво чтоб твой бомже отец наконец-то порадовался ведь он не может терпеть такую хуйню как твоя мать, давай же сынок хуйни высри еще раз хуйгю какую. то же такой дахуя сильный, ты на сильный ты слабак чисто посмел окравить слово своего бога, то есть меня, по этому давай всоси мой хуй уже давалка ебанаяты жавнаьвре сынок бляди ебаной которой я ебало буду бить стдип отец фулл фокус сыно поеботни ты же просто в фарш превратишься от моего великолепного божественного лоу кика, и да твоя мать уже гнилью воняет тад того чтоя. ее нахуй в гробу живую закопал а покуда твоя мать там в гробу я твою сес иенку просто ебу чтоб она шлюха не забывала любимое дело своей матери, а тоый отец просто ебучий бичуган на мусоре сидит на мусорке сосет хуи всем по 10 копеек давай же сынок хуйни медденой высри опять свой слабый текст, я тебе щее раз повторяю уже последний и 3 раз еще раз мне от пиешл смой бомже текст я твою мать пиздопроебину ебанаую просто отьбебу в щепки сынок бомжа ебаного"
MIN_DELAY = 0
MAX_DELAY = 0.09
LOG_FILE = "badwalk_log.txt"

# ========================
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
stop_events = {}
eblo_targets = {}  # {chat_id: set(user_ids)} — кого автоматически удалять

# ===== Утилиты =====
def now_ts():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def parse_text_to_words(text):
    return re.findall(r'\b\w+\b', text, flags=re.UNICODE)


def log_line(line: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now_ts()}] {line}\n")


async def safe_send(chat_id: int, text: str):
    while True:
        try:
            await app.send_message(chat_id, text)
            log_line(f"SENT to {chat_id}: {text}")
            return
        except FloodWait as e:
            log_line(f"FloodWait {e.value}s — sleeping")
            await asyncio.sleep(e.value)
        except Exception as e:
            log_line(f"ERROR sending to {chat_id}: {text} — {e}")
            return


async def send_words(origin_chat_id: int, target_chat_id: int, words_source: str):
    stop_events[origin_chat_id] = asyncio.Event()
    parsed = parse_text_to_words(words_source)

    if not parsed:
        log_line(f"NO_WORDS to send from chat {origin_chat_id}")
        stop_events.pop(origin_chat_id, None)
        return

    for word in parsed:
        if stop_events[origin_chat_id].is_set():
            log_line(f"STOPPED by user during sending to {target_chat_id}")
            break

        await safe_send(target_chat_id, word)
        await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

    stop_events.pop(origin_chat_id, None)
    log_line(f"COMPLETED sending to {target_chat_id}")

# ===== Команды =====

# /sperm
@app.on_message(filters.me & filters.command("sperm", prefixes="/"))
async def on_sperm(client, message):
    origin_chat_id = message.chat.id

    try:
        await message.delete()
        log_line(f"Command /sperm deleted in chat {origin_chat_id}")
    except Exception:
        pass

    if origin_chat_id in stop_events and not stop_events[origin_chat_id].is_set():
        log_line(f"Command ignored, active sending in chat {origin_chat_id}")
        return

    parts = message.text.split(maxsplit=2)
    target_chat_id = origin_chat_id
    supplied_text = None

    if len(parts) == 1:
        supplied_text = TEXT_DEFAULT
    elif len(parts) == 2:
        maybe = parts[1]
        if maybe.startswith("@") or maybe.isdigit():
            try:
                user = await client.get_users(maybe)
                target_chat_id = user.id
            except Exception:
                supplied_text = maybe
        else:
            supplied_text = parts[1]
    else:
        maybe = parts[1]
        rest = parts[2]
        if maybe.startswith("@") or maybe.isdigit():
            try:
                user = await client.get_users(maybe)
                target_chat_id = user.id
                supplied_text = rest
            except Exception:
                supplied_text = " ".join(parts[1:])
        else:
            supplied_text = " ".join(parts[1:])

    if supplied_text is None:
        supplied_text = TEXT_DEFAULT

    log_line(f"START sending from chat {origin_chat_id} to {target_chat_id}: {supplied_text}")
    asyncio.create_task(send_words(origin_chat_id, target_chat_id, supplied_text))


# /stop
@app.on_message(filters.me & filters.command("stop", prefixes="/"))
async def on_stop(client, message):
    origin = message.chat.id
    ev = stop_events.get(origin)
    if ev and not ev.is_set():
        ev.set()
        log_line(f"STOP command received in chat {origin}")

# ===== ANTISTICKER (улучшенный) =====
@app.on_message(filters.me & filters.command("antisticker", prefixes="/"))
async def on_antisticker(client, message):
    chat = message.chat
    chat_id = chat.id
    parts = message.text.split()

    if len(parts) < 3:
        await message.reply("Используй: /antisticker <количество> @user")
        return

    # В приватных чатах удалять чужие сообщения нельзя
    if chat.type == "private":
        await message.reply("В ЛС удалять чужие сообщения нельзя. Используй в группе/супергруппе.")
        log_line(f"ANTISTICKER aborted: chat {chat_id} is private")
        return

    try:
        count = int(parts[1])
        if count <= 0:
            raise ValueError
    except:
        await message.reply("Ошибка: количество должно быть числом > 0")
        return

    user_arg = parts[2]
    try:
        target_user = await client.get_users(user_arg)
        target_id = target_user.id
    except Exception as e:
        await message.reply("Ошибка: не удалось найти пользователя")
        log_line(f"ANTISTICKER find-user error: {e}")
        return

    try:
        await message.delete()
    except:
        pass

    log_line(f"ANTISTICKER start: delete {count} stickers from {target_id} in chat {chat_id}")

    deleted = 0
    scanned = 0
    # проходим историю от новых к старым
    async for msg in app.get_chat_history(chat_id, limit=1500):
        scanned += 1
        if deleted >= count:
            break

        # Только сообщения от нужного юзера
        if not msg.from_user or msg.from_user.id != target_id:
            continue

        # DIAGNOSTIC: попробуем определить, является ли сообщение стикером
        is_sticker_flag = False
        desc_flags = []

        try:
            if getattr(msg, "sticker", None):
                is_sticker_flag = True
                desc_flags.append("sticker")
        except:
            pass

        try:
            if getattr(msg, "media", None) == "sticker":
                is_sticker_flag = True
                desc_flags.append("media==sticker")
        except:
            pass

        try:
            if getattr(msg, "content_type", None) == "sticker":
                is_sticker_flag = True
                desc_flags.append("content_type==sticker")
        except:
            pass

        # иногда стикеры приходят как animation или document (редкие случаи)
        try:
            if getattr(msg, "animation", None):
                # animation может быть стикер (tgs/webm)
                desc_flags.append("animation")
            if getattr(msg, "document", None):
                mime = getattr(msg.document, "mime_type", "") or ""
                desc_flags.append(f"document({mime})")
        except:
            pass

        # если явно не стикер — пропускаем, но логируем некоторые первые/редкие
        if not is_sticker_flag:
            if scanned <= 60 or scanned % 300 == 0:
                log_line(f"ANTISTICKER scan msg_id={msg.id} from {target_id} flags={desc_flags} content_type={getattr(msg,'content_type',None)}")
            continue

        # пытаемся удалить
        try:
            await msg.delete()
            deleted += 1
            log_line(f"ANTISTICKER deleted msg_id={msg.id} ({','.join(desc_flags)})")
        except Exception as e:
            log_line(f"ANTISTICKER failed delete msg_id={msg.id}: {e}")

    log_line(f"ANTISTICKER finished: deleted {deleted}/{count} scanned={scanned}")
    # уведомление о результате (необязательно)
    try:
        await client.send_message(chat_id, f"ANTISTICKER: удалено {deleted}/{count} стикеров от {user_arg}")
    except:
        pass


# ===== EBLO (автоудаление сообщений пользователя) =====
@app.on_message(filters.me & filters.command("eblo", prefixes="/"))
async def on_eblo(client, message):
    chat_id = message.chat.id
    parts = message.text.split()

    if len(parts) < 2:
        await message.reply("Используй: /eblo @user")
        return

    try:
        target = await client.get_users(parts[1])
        user_id = target.id
    except Exception as e:
        await message.reply("Ошибка: не удалось найти пользователя")
        log_line(f"EBLO find-user error: {e}")
        return

    try:
        await message.delete()
    except:
        pass

    eblo_targets.setdefault(chat_id, set()).add(user_id)
    log_line(f"EBLO enabled for user {user_id} in chat {chat_id}")

@app.on_message(filters.me & filters.command("eblooff", prefixes="/"))
async def on_eblo_off(client, message):
    chat_id = message.chat.id
    try:
        await message.delete()
    except:
        pass

    eblo_targets.pop(chat_id, None)
    log_line(f"EBLO disabled in chat {chat_id}")


# ===== AUTO DELETION HOOK =====
@app.on_message()
async def auto_delete_handler(client, message):
    chat_id = message.chat.id
    # Если в этой комнате включён EBLO — удаляем сообщения от отмеченных юзеров
    if chat_id in eblo_targets:
        uid_set = eblo_targets[chat_id]
        if message.from_user and message.from_user.id in uid_set:
            try:
                await message.delete()
                log_line(f"EBLO auto-delete msg from {message.from_user.id} in chat {chat_id}")
            except Exception as e:
                log_line(f"EBLO auto-delete FAILED for msg_id={getattr(message,'id',None)}: {e}")


# ===== Запуск =====
if __name__ == "__main__":
    print("Запуск BADWALK client...")
    print("Команды:")
    print(" /sperm")
    print(" /stop")
    print(" /antisticker количество @user")
    print(" /eblo @user — включить автоудаление")
    print(" /eblooff — выключить автоудаление")
    app.run()
