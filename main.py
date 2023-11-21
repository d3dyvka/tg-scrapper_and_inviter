from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import sys
import traceback
import random

import time, csv

from telethon.sync import TelegramClient

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.channels import InviteToChannelRequest

#Заходишь на сай разработчика тг https://my.telegram.org/auth?to=apps и регаешься
#После вылезет окно с созданием приложения. Указываешь только полное и краткое имя(просто обязательный пункт) и нажимаешь Create Application
#Откроется страница на которой тебе нужны два нижних параметра: api-id и api-hash. Копируешь их и вставляешь ниже в переменные
#Примечание!!!: id должен быть в виде цифр, а хеш и телефон в виде строки
api_id =
api_hash = ''
phone_number = ''
client = TelegramClient(phone_number, api_id, api_hash, system_version="4.16.30-vxCUSTOM")
#После запуска код попросит ввести номер телефона, вводишь в виде 79000000000 и нажимаешь Enter
#Дальше тебе в тг придет код, вписываешь его и после завершения перезапускаешь код
#Все, код готов парсить

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"
yo="\033[1;33m"

client.start()

chats = []
last_date = None
size_chats = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=size_chats,
    hash=0))

chats.extend(result.chats)


for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print(gr+'[-] Выберите группу для парсинга:'+re)
for i, g in enumerate(groups):
    print(gr+'['+cy+str(i)+']' + ' - ' + g.title)
print('')
g_index = input(gr+"[-] Введите номер: "+re)
target_group=groups[int(g_index)]

print(gr+'[-] Парсим людей ...')
time.sleep(1)
all_participants = []
all_participants = client.iter_participants(target_group)

print(gr+'[-] Сохраняем в файл ...')
time.sleep(1)
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username = user.username or ""
            first_name = user.first_name or ""
            last_name = user.last_name or ""
            name = (first_name + ' ' + last_name).strip()
        else:
            continue
        writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
print(gr+'[-] Процесс выполнен!')

input_file = "members.csv"
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

i = 0
for group in groups:
    print(gr + '[' + cy + str(i) + gr + ']' + cy + ' - ' + group.title)
    i += 1

print(gr + '[+] Выберите группу в которую нужно добавить людей')
g_index = input(gr + "[+] Введите номер: " + re)
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

print(gr + "Введите 1, если нужно добавить людей по никнейму")
mode = int(input(gr + "Input : " + re))
n = 0

for user in users:
        try:
            print("Добавляю пользователя {}".format(user['id']))
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            else:
                sys.exit(re + "[!] Неправильно выбран режим парсинга, попробуйте еще раз.")
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print(gr + "[+] Ждем 5-10 секунд...")
            time.sleep(random.randrange(5, 10))
        except PeerFloodError:
            print(
                re + "[!] Полученно предупреждение флуда от телегармма. \n[!] Скрипт сейчас остановится. \n[!] Попробуйте снова через некоторое время.")
        except UserPrivacyRestrictedError:
            print(re + "[!] Пользовательские настройки приватности пользователя не позволяют это сделать. Пропускаем.")
        except:
            traceback.print_exc()
            print(re + "[!] Неизвестная ошибка")
            continue