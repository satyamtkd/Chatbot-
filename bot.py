# Zaroori libraries import kar rahe hain
from typing import List, Optional, Union
import asyncio
from datetime import datetime
from satyachat_puppet import get_logger  # satyachat_puppet ka use
from satyachat import (  # satyachat ka use
    MessageType,
    FileBox,
    RoomMemberQueryFilter,
    Satyachat,  # Main class ka naam change kiya
    Contact,
    Room,
    Message,
    Image,
    MiniProgram,
    Friendship,
    FriendshipType,
    EventReadyPayload
)

logger = get_logger(__name__)

class MyBot(Satyachat):  # Ab hum Satyachat class ka use karenge
    """
    Satyachat functions ko inherit karke event listen karenge
    """

    def __init__(self) -> None:
        """Initialize karne ka function"""
        self.login_user: Optional[Contact] = None
        super().__init__()

    async def on_ready(self, payload: EventReadyPayload) -> None:
        """Bot ready hone par ye function chalega"""
        logger.info('Bot ready with payload %s...', payload)

    async def on_message(self, msg: Message) -> None:
        """Aaye hue messages ko handle karega"""
        from_contact: Contact = msg.talker()
        text: str = msg.text()  # Message ka text le raha hai
        room: Optional[Room] = msg.room()  # Agar ye group message hai toh room object le raha hai
        msg_type: MessageType = msg.type()
        file_box: Optional[FileBox] = None
        if text == 'ding':  # Agar 'ding' message hai toh reply 'dong' se karega
            conversation: Union[Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('dong')
            file_box = FileBox.from_url(
                'https://example.com/ding-dong.jpg',  # Updated URL
                name='ding-dong.jpg')
            await conversation.say(file_box)
        elif msg_type == MessageType.MESSAGE_TYPE_IMAGE:
            logger.info('Image file receive ho rahi hai')
            image: Image = msg.to_image()
            hd_file_box: FileBox = await image.hd()  # High-quality image ko file mein save karega
            await hd_file_box.to_file('./hd-image.jpg', overwrite=True)
            thumbnail_file_box: FileBox = await image.thumbnail()
            await thumbnail_file_box.to_file('./thumbnail-image.jpg', overwrite=True)
            artwork_file_box: FileBox = await image.artwork()
            await artwork_file_box.to_file('./artwork-image.jpg', overwrite=True)
            await msg.say(hd_file_box)  # Message mein image send karega
        elif msg_type in [MessageType.MESSAGE_TYPE_AUDIO, MessageType.MESSAGE_TYPE_ATTACHMENT, MessageType.MESSAGE_TYPE_VIDEO]:
            logger.info('File receive ho rahi hai...')
            file_box = await msg.to_file_box()
            if file_box:
                await file_box.to_file(file_box.name)  # File ko save karega
        # Yahan aur bhi event handlers add kar sakte hain...

    async def on_login(self, contact: Contact) -> None:
        """Login event"""
        logger.info('User <%s> logged in...', contact)
        self.login_user = contact

    # Friendship aur room join ke liye aur bhi functions yahan add kar sakte hain

async def main() -> None:
    """Bot start karne ka function"""
    bot = MyBot()
    await bot.start()

asyncio.run(main())

# Credits: Satyam Dubey