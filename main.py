import configparser
import json
import regex as re

from telethon.sync import TelegramClient

from datetime import datetime

# for channels
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# for sms
from telethon.tl.functions.messages import GetHistoryRequest


config = configparser.ConfigParser()
config.read("config.ini")

api_id =  #your id
api_hash =  #your hash
username =  # your username

client = TelegramClient(username, api_id, api_hash)

#client.start()

async def dump_all_participants(channel):
	"""Записывает json-файл с информацией о всех участниках канала/чата"""
	queryKey = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
				'v', 'w', 'x', 'y', 'z']
	all_participants = []

	for key in queryKey:
		offset = 0
		limit = 100
		while True:
			#participants = await client(GetParticipantsRequest(channel, ChannelParticipantsSearch(key), offset, limit,hash=0))
			if not participants.users:
				break
			for user in participants.users:
				try:
					if re.findall(r"\b[a-zA-Z]", user.first_name)[0].lower() == key:
						all_participants.append(user)
				except:
					pass

			offset += len(participants.users)
			print(offset)

	all_users_details = []   # parametrs of users

	for participant in all_participants:
		all_users_details.append({"id": participant.id,
			"first_name": participant.first_name,
			"last_name": participant.last_name,
			"user": participant.username,
			"phone": participant.phone,
			"is_bot": participant.bot})

	with open('channel_users.json', 'w', encoding='utf8') as outfile:
		json.dump(all_users_details, outfile, ensure_ascii=False)


async def dump_all_messages(channel):
	"""Записывает json-файл с информацией о всех сообщениях канала/чата"""
	offset_msg = 0
	limit_msg = 100

	all_messages = []
	total_messages = 0
	total_count_limit = 0  # change this var. if you don't need all sms.

	class DateTimeEncoder(json.JSONEncoder):
		'''Класс для сериализации записи дат в JSON'''
		def default(self, o):
			if isinstance(o, datetime):
				return o.isoformat()
			if isinstance(o, bytes):
				return list(o)
			return json.JSONEncoder.default(self, o)

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			all_messages.append(message.to_dict())
		offset_msg = messages[len(messages) - 1].id
		total_messages = len(all_messages)
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break

	with open('channel_messages.json', 'w', encoding='utf8') as outfile:
         json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)


async def main():
  url = input("Введите ссылку на канал или чат: ")
  channel = await client.get_entity(url)
  await dump_all_participants(channel)
  await dump_all_messages(channel)

with client:
  client.loop.run_until_complete(main())

