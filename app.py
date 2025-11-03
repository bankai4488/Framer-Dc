from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

#  Get Discord webhook from environment variable
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route('/framer-webhook', methods=['POST'])
def framer_webhook():
    try:
        data = request.get_json(force=True)

        # Extract fields from Framer form
        name = data.get("Name", "N/A")
        username = data.get("Username", "N/A")
        service = data.get("Service", "N/A")
        message = data.get("Text Area", "N/A")

        # Check webhook URL
        if not DISCORD_WEBHOOK_URL:
            return jsonify({"error": "Missing Discord webhook URL in environment variables"}), 500

        # Format the Discord message
        payload = {
            "content": (
                f"📩 **New Client Submission**\n"
                f"👤 **Name:** {name}\n"
                f"📧 **DcUserName:** {username}\n"
                f"🧰 **Service:** {service}\n"
                f"📝 **Message:** {message}"
            )
        }

        # Send the message to Discord
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

        if response.status_code in [200, 204]:
            return jsonify({"success": True, "message": "Sent to Discord"}), 200
        else:
            return jsonify({
                "success": False,
                "error": f"Discord webhook failed ({response.status_code})",
                "details": response.text
            }), 500

    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "Framer → Discord Webhook Bridge is running!"}), 200


# Vercel looks for "app" variable by default
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
