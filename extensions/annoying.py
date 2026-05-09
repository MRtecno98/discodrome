
import asyncio
import os, random, logging
from typing import Final

from discord import FFmpegPCMAudio

from discodrome import DiscodromeClient

ANNOYING_ENABLE: Final[bool] = os.getenv("ANNOYING_DELAY", "true").lower() == "true"
ANNOYING_DELAY: Final[int] = int(os.getenv("ANNOYING_DELAY", str(20*60))) # Default to 20 minutes
ANNOYING_CHANCE: Final[int] = int(os.getenv("ANNOYING_CHANCE", str(5))) # Default to 1 in 5 chance

async def annoying_task(bot: DiscodromeClient):
	''' A task that sends a message to the test guild every 10 minutes. '''

	await bot.wait_until_ready()

	while not bot.is_closed():
		logging.info(f"Running annoying task (delay is {ANNOYING_DELAY} seconds, chance is 1 in {ANNOYING_CHANCE})")

		for guild in bot.guilds:
			if guild.voice_client is not None:
				break

			for voice in guild.voice_channels:
				if len(voice.members) >= 2:
					if (rnd := random.randint(1, ANNOYING_CHANCE)) == 1:
						logging.info(f"Annoying task triggered in guild '{guild.name}' (chance was {rnd})")

						client = await voice.connect()

						audio = FFmpegPCMAudio(source='resources/tacobell.mp3')

						await asyncio.sleep(0.5)
						client.play(audio)

						while client.is_playing():
							await asyncio.sleep(0.5)

						await client.disconnect()
						
						break
					else:
						logging.info(f"Annoying task skipped in guild '{guild.name}' (chance was {rnd})")

		await asyncio.sleep(ANNOYING_DELAY) # Sleep for the specified delay

async def setup(bot: DiscodromeClient):
	if ANNOYING_ENABLE:
		asyncio.create_task(annoying_task(bot))
