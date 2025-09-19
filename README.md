# Zoom License Manager

Automated license management system for Zoom that assigns and unassigns licenses based on a predefined schedule.

## ✨ Features

- **Automated License Management**: Automatically assigns and unassigns Zoom licenses
- **License Usage Tracking**: Monitors and reports total, used, and available licenses
- **Low License Alerts**: Automatically warns when available licenses are running low
- **Schedule-Based**: Uses a database schedule to determine license assignments
- **Exception Handling**: Supports an exempt list of users who should never lose their licenses
- **Notifications**: Sends detailed Telegram notifications about license operations
- **Error Reporting**: Provides comprehensive error logging and reporting

## ⏰ Scheduling with Cron

To automatically run the license manager at 1 AM from Monday to Friday, set up a cron job as follows:

1. Open your crontab configuration:
   ```bash
   crontab -e
   ```

2. Add this line to run the script at 1 AM on weekdays (Monday-Friday):
   ```
   0 1 * * 1-5 cd /path/to/zoom-license-manager && /path/to/venv/bin/python app.py >> /var/log/zoom_license_manager.log 2>&1
   ```

   Replace:
   - `/path/to/zoom-license-manager` with the actual path to your project directory
   - `/path/to/venv/bin/python` with the path to your virtual environment's Python executable

3. Save and exit. The cron job will now run automatically.

4. (Optional) To monitor the logs:
   ```bash
   tail -f /var/log/zoom_license_manager.log
   ```

### Log Rotation (Recommended)

To prevent log files from growing too large, set up log rotation by creating a new file at `/etc/logrotate.d/zoom-license-manager` with:

```
/var/log/zoom_license_manager.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
}
```

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

### Running the License Manager

```bash
python app.py
```

### Telegram Notification Format

The system sends detailed notifications to Telegram with the following format:

```
📊 License Management Summary
==========================
📅 Date: 2023-09-20
⏰ Time: 00:40:03 EAT

🔴 Unassigned: 5/5
🟢 Assigned: 3/3

📊 License Usage:
• Total Licenses: 100
• Used Licenses: 85
• Available Licenses: 15

⚠️ Warning: Running low on available licenses!

🛡️ Exempt Users (Never Unassigned):
• admin@example.com
• manager@example.com

🛡️ Exempted in This Run:
• user1@example.com
• user2@example.com

❌ Failed Unassignments:
• user3@example.com: User not found

❌ Failed Assignments:
• user4@example.com: No available licenses

✅ Completed Successfully
```

### License Usage Report

The system includes a comprehensive license usage report showing:
- Total number of available licenses
- Number of currently used licenses
- Number of available licenses
- Automatic warning when available licenses are running low (less than 10% remaining)

You can also check license usage programmatically:
```python
from assign import get_license_usage

usage = get_license_usage()
if usage:
    print(f"Total Licenses: {usage['total_licenses']}")
    print(f"Used Licenses: {usage['used_licenses']}")
    print(f"Available Licenses: {usage['available_licenses']}")
```

### Expected Output

```
🚀 Starting license management...
==================================================
📅 Today is: Friday
📅 Yesterday was: Thursday

📋 Fetching schedule...
✅ Successfully connected to the database.

📊 License Usage:
• Total Licenses: 100
• Used Licenses: 85
• Available Licenses: 15

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
