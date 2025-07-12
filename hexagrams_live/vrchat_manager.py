import datetime
from pythonosc import udp_client
import constants

class VRChatManager:
	def __init__(self):
		self.client = udp_client.SimpleUDPClient(constants.VRCHAT_IP, constants.VRCHAT_PORT)

	def send_message(self, message):
		if not constants.SEND_TO_VRCHAT_ENABLED or constants.EXIT_FLAG:
			return
		try:
			self.client.send_message("/chatbox/input", [message, True, False])
			print("Message sent to VRChat")
		except Exception as e:
			if not constants.EXIT_FLAG:
				print(f"[VRChatManager] Error sending message to VRChat: {e}")
			pass

	def format_message_page1(self, hexagrams, time_to_zero, level6_days=None, level6_moving_line=None):
		current_date = datetime.datetime.now().date()
		days_to_zero = round(time_to_zero.total_seconds() / 86400)
		hours_to_zero = int((time_to_zero.total_seconds() % 86400) // 3600)
		
		message = f"Date: {current_date}\nDays_to_0: {days_to_zero}d{hours_to_zero}h\n"
		
		# Find level 3 for the Change line
		for level, cycle_length, cycle_name, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
			if level == 3:
				time_to_next_change = datetime.timedelta(seconds=time_since_last_change) - cycle_length
				time_time = (cycle_length - abs(time_to_next_change))
				hours = int(abs(time_time.seconds // 3600))
				minutes = int(abs((time_time.seconds % 3600) // 60))
				seconds = int(abs(time_time.seconds % 60))
				message += f"Change: {hours:02d}:{minutes:02d}:{seconds:02d}\n"
				break

		# Add levels 4 and 5 as before
		for level in [4, 5]:
			for l, cycle_length, cycle_name, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
				if l == level:
					hexagram_first_name = hexagram_name.split(" - ")[0]
					moving_line = (time_since_last_change // (cycle_length.total_seconds() / 6)) + 1
					days = cycle_length.total_seconds() / 86400
					message += f"L {level}: {days:.0f} d, {hexagram_number}-{hexagram_first_name} - {moving_line}\n"
					break

		# Add level 6 using the exact values from the GUI for days and moving line
		if level6_days is not None and level6_moving_line is not None:
			# Find the level 6 hexagram name and number
			for l, cycle_length, cycle_name, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
				if l == 6:
					hexagram_first_name = hexagram_name.split(" - ")[0]
					message += f"L 6: {level6_days} d, {hexagram_number}-{hexagram_first_name} - {level6_moving_line}\n"
					break
		else:
			for l, cycle_length, cycle_name, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
				if l == 6:
					line_change_interval = cycle_length.total_seconds() / 6
					time_until_next_line_change = line_change_interval - (time_since_last_change % line_change_interval)
					days = int(time_until_next_line_change // 86400)
					moving_line = int((time_since_last_change // line_change_interval) + 1)
					hexagram_first_name = hexagram_name.split(" - ")[0]
					message += f"L 6: {days} d, {hexagram_number}-{hexagram_first_name} - {moving_line}\n"
					break

		return message

	def format_message_page2(self, hexagrams, time_to_zero):
		message = ""
		for level, cycle_length, _cycle_name, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
			if level > 3:
				continue
				
			hexagram_first_name = hexagram_name.split(" - ")[0]
			moving_line = (time_since_last_change // (cycle_length.total_seconds() / 6)) + 1

			if level == 1:
				cycle_length_str = f"{cycle_length.total_seconds():.2f}"
				message += f"L {level}: {cycle_length_str} s, {hexagram_number} - {hexagram_first_name}\n"
			elif level == 2:
				minutes = int(abs(time_since_last_change // 60))
				seconds = int(abs(time_since_last_change % 60))
				message += f"L 2: change {minutes:02d}:{seconds:02d}\n"
				message += f"L {level}: {cycle_length.total_seconds():.2f} s, {hexagram_number} - {hexagram_first_name} - {moving_line}\n"
			elif level == 3:
				hours = int(abs(time_since_last_change // 3600))
				minutes = int(abs((time_since_last_change % 3600) // 60))
				seconds = int(abs(time_since_last_change % 60))
				message += f"L 3 change {hours:02d}:{minutes:02d}:{seconds:02d}\n"
				cycle_length_str = f"{cycle_length.total_seconds() / 3600:.2f}"
				message += f"L {level}: {cycle_length_str} h, {hexagram_number} - {hexagram_first_name} - {moving_line}\n"

		return message