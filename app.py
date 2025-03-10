from flask import Flask, request, jsonify
from flask_cors import CORS
import telegram
import asyncio
import os

app = Flask(__name__)
CORS(app)

BOT_TOKEN = "7685931936:AAGPko-E1FrWZItSSKVFNHcp4nYk5_5SnHU"
CHANNEL_ID = "-1002260718745"

bot = telegram.Bot(token=BOT_TOKEN)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/send', methods=['POST'])
def send_message():
    caption = request.form.get("caption", "")
    image = request.files.get("image")

    if not image and not caption:
        return jsonify({"error": "Either an image or a text message is required"}), 400

    try:
        if image:
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_path)

            with open(image_path, "rb") as img_file:
                # Create a new event loop for this call
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(bot.send_photo(chat_id=CHANNEL_ID, photo=img_file, caption=caption))
                loop.close()
            
            os.remove(image_path)  # Clean up after sending

        elif caption:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(bot.send_message(chat_id=CHANNEL_ID, text=caption))
            loop.close()

        return jsonify({"success": True, "message": "✅ Message sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Disable the reloader to avoid event loop issues during debugging
    app.run(debug=True, use_reloader=False)