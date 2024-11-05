# Yeh hai simple Ding-Dong Bot jo humne satyachat library ke saath banaya hai

import asyncio
from satyachat import Satyachat, Message  # Updated import

async def on_message(msg: Message):
    """Aaye hue message ko handle karega"""
    if msg.text() == 'ding':  # Agar 'ding' message aaya toh 'dong' reply karega
        await msg.say('dong')  
    
async def main():
    bot = Satyachat()  # Custom Satyachat bot class ka use kar rahe hain
    bot.on('message', on_message)  # Message event listener set kar rahe hain
    await bot.start()  # Bot start ho raha hai

asyncio.run(main())

# Credits: Satyam Dubey
# simple-bot.py
# Copyright (c) 2024 satyamtkd
# All rights reserved.
