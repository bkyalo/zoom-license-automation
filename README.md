# Zoom License Manager

Automated license management system for Zoom that assigns and unassigns licenses based on a predefined schedule.

## ✨ Features

- **Automated License Management**: Automatically assigns and unassigns Zoom licenses
- **Schedule-Based**: Uses a database schedule to determine license assignments
- **Exception Handling**: Supports an exempt list of users who should never lose their licenses
- **Notifications**: Sends detailed Telegram notifications about license operations
- **Error Reporting**: Provides comprehensive error logging and reporting

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Zoom account with admin privileges
- Zoom OAuth app credentials
- Telegram bot (for notifications)
- MySQL/MariaDB database

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/zoom-license-manager.git
   cd zoom-license-manager
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file and update with your credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

## ⚙️ Configuration

Edit the `.env` file with your configuration:

```ini
# Zoom API Configuration
ZOOM_ACCOUNT_ID=your_account_id
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret

# Database Configuration
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Exempt Users (never unassigned)
EXEMPT_USERS=admin@example.com,user@example.com
```

## 🛠️ Usage

Run the license manager:

```bash
python app.py
```

### Expected Output

```
🚀 Starting license management...
==================================================
📅 Today is: Friday
📅 Yesterday was: Thursday

📋 Fetching schedule...
✅ Successfully connected to the database.

📊 Summary:
- Found 5 users to unassign
- Found 3 users to assign

🔴 Unassigning licenses for 5 users...
1. Unassigning from user1@example.com... ✅ Done
...

🟢 Assigning licenses to 3 users...
1. Assigning to newuser@example.com... ✅ Done
...

==================================================
✅ License management completed!
📱 Notification sent to Telegram
```

## 📋 License Management Rules

1. Users are assigned licenses based on the schedule in the database
2. Users who had licenses yesterday but not today will have them unassigned
3. Users in the `EXEMPT_USERS` list will never have their licenses unassigned
4. Detailed logs are sent to Telegram after each run

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python
- Uses the Zoom API for license management
- Telegram for notifications
