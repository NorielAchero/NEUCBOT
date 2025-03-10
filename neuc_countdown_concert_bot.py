import asyncio
from telegram import Bot
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+

# Replace with your bot token
BOT_TOKEN = "8157328271:AAEhbpQgPEdlsWcLZv1MPTQurkpu0BicMCU"
# Replace with your channel ID (e.g., -100XXXXXXXXX) NEU CHOIR CHANNEL
CHANNEL_ID = "-1001219010958"

bot = Bot(token=BOT_TOKEN)

# Set the timezone for PHT
pht = ZoneInfo("Asia/Manila")

# Target date: May 31, 2025 (set as timezone-aware)
target_date = datetime(2025, 5, 31, tzinfo=pht)

# List of image URLs to rotate through
IMAGE_URLS = [
    "https://scontent.fmnl4-3.fna.fbcdn.net/v/t1.15752-9/482088757_521901337234170_1012017785195558247_n.png?_nc_cat=110&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeFkiOB3QeiNLRRx4_c31FqbzjRgvOkoXefONGC86Shd55kL3EA9-xpFY9OrPsolHlwiGdonWOuKdBIKuxz7W-P0&_nc_ohc=T0aeHJt5SdwQ7kNvgEOGozS&_nc_oc=AdixE0KBLf_F5-QbbG4DYV5QYL35X6edlDZ6g-fnpptme8DQVuPpl6d1bWvDBzMbiiPYc7tWnpiJWxlL_ZBqmYTk&_nc_zt=23&_nc_ht=scontent.fmnl4-3.fna&oh=03_Q7cD1wGXHgVXccmbf3JE_6IwJ0QoqGhiIT5Ahvn1ETANMXDuxQ&oe=67F28E77",
    "https://scontent.fmnl4-7.fna.fbcdn.net/v/t1.15752-9/481855395_9264961806957801_3476448116590271344_n.png?_nc_cat=108&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeGLRgrJObdwOzk267ATquYd2D-YjqfUbc3YP5iOp9RtzYzSB5B-8ky5NxGjBFijYRia_7u3dauXYSgpnU-EEpZm&_nc_ohc=NgihrPAfQ-QQ7kNvgEfZzZv&_nc_oc=AdjM-kR3ceVwCz-shdL00TmNjrgjV_NWM0dk-fRbAjVT4gvtLKHVBwSWL-ShG5uBOrDEtM7xFuNAZl2od_vIhXhX&_nc_zt=23&_nc_ht=scontent.fmnl4-7.fna&oh=03_Q7cD1wHcNqv1UkVTswozW6b0hO1NcJJ25qUo0KYBb7g-DD9p5g&oe=67F28C93",
    "https://scontent.fmnl4-7.fna.fbcdn.net/v/t1.15752-9/482517946_980480137380271_4824337153112852363_n.png?_nc_cat=104&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeEP6TuOLVR5_sdm1xOprytO8tez6KJQGkDy17PoolAaQEN9PyiM7XnFjCEz2skXH8TNP9L_SABLSrtUxqrhLdey&_nc_ohc=-mbdNwznTCkQ7kNvgHjHhUk&_nc_oc=AdjnjR87Nc7NhfYzXG0v4ZTN_UB0McrJ4Uq9sBL2GNB4FYBx6zNIWGneyH9BrnXoZzPqD-FZBUv-1m5SnvFpdabo&_nc_zt=23&_nc_ht=scontent.fmnl4-7.fna&oh=03_Q7cD1wFZS8VwQ0_u3HIut-0vwXdcf2fCY2s8l_-oBa9ruJZcRA&oe=67F27EE8",
    "https://scontent.fmnl4-7.fna.fbcdn.net/v/t1.15752-9/482620123_1324189031953960_9133658927109165720_n.png?_nc_cat=104&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeHwxKcCJKzMg5Wegp4ldoN6vzVNFbF5gxS_NU0VsXmDFGY7LZ1CplPaPkc41K6YWilg8KwI7xjgcFTfgmNtLLy-&_nc_ohc=Vv94mwWL6IMQ7kNvgGvNwRm&_nc_oc=AdiVDDNzUEv0o6HPO7kfMftxKkYLJP2bvK-r9KrryPKX1_6dSLHmhLKqz4Pf8Yd_053DLOllEDXgDmZB0h8PwkSg&_nc_zt=23&_nc_ht=scontent.fmnl4-7.fna&oh=03_Q7cD1wHHbDR-AC_2JqBN-S-NGNgmrnli057xm5-VChI49Qt1Tw&oe=67F29FB3",
]

async def send_telegram_message():
    """Sends an image with the countdown caption to the Telegram channel at 1:00 AM (PHT)."""
    while True:
        now = datetime.now(pht)
        # Define the target time (7:30 AM)
        target_time = time(7, 30)  # 7:30 AM in 24-hour format
        next_message_time = datetime.combine(now.date(), target_time).replace(tzinfo=pht)

        # If the target time already passed today, schedule for tomorrow
        if now > next_message_time:
            next_message_time = datetime.combine(now.date() + timedelta(days=1), target_time).replace(tzinfo=pht)

        seconds_until_target = (next_message_time - now).total_seconds()

        print(f"Waiting {seconds_until_target:.2f} seconds until next 7:30 AM (PHT)...")

        # Wait until the target time
        await asyncio.sleep(seconds_until_target)

        # Calculate days remaining (ensuring the operation is done in PHT)
        today = datetime.now(pht)
        days_remaining = (target_date - today).days + 1  # +1 to include today

        # Select the image for the day using rotation
        image_index = today.toordinal() % len(IMAGE_URLS)
        image_url = IMAGE_URLS[image_index]

        message_text = f"📅 NEUChoirConcert: {days_remaining} days until May 31, 2025! 🩵"

        # Send only the image with the caption
        await bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=message_text)
        print(f"🖼️ Image sent to Telegram with caption: {message_text}")

async def print_console_message():
    """Prints a status update to the console every 30 seconds."""
    while True:
        now = datetime.now(pht).strftime("%Y-%m-%d %H:%M:%S")
        print(f"🕒 Bot is running (PHT)... Current time: {now}")
        await asyncio.sleep(30)  # Wait for 30 seconds

async def main():
    """Runs both tasks concurrently."""
    await asyncio.gather(send_telegram_message(), print_console_message())

# Run the async function
asyncio.run(main())
