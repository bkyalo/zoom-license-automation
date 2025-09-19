import requests
from getschedule import get_email_schedule
from day_utils import get_day_info, get_day_schedule
from assign import assign_license
from unassign import unassign_license
from config import Config
import time

def send_telegram_message(message):
    """Send a message to the configured Telegram chat."""
    try:
        payload = {
            'chat_id': Config.TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(Config.TELEGRAM_API_URL, json=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Failed to send Telegram notification: {str(e)}")
        return False

def manage_licenses():
    from datetime import datetime
    print("🚀 Starting license management...")
    print("=" * 50)
    
    # Get day information
    day_info = get_day_info()
    today = day_info['today']
    yesterday = day_info['yesterday']
    
    print(f"📅 Today is: {today}")
    print(f"📅 Yesterday was: {yesterday}")
    
    # Initialize tracking for failed operations
    failed_unassign = []
    failed_assign = []
    
    # Get the full schedule
    print("\n📋 Fetching schedule...")
    schedule = get_email_schedule()
    if not schedule:
        print("❌ Failed to fetch schedule. Exiting.")
        return
    
    # Get today's and yesterday's emails
    today_emails = set(get_day_schedule(schedule, day_info['today']))
    yesterday_emails = set(get_day_schedule(schedule, day_info['yesterday']))
    
    # Find emails that are only in yesterday (need to unassign)
    # But exclude exempt users from being unassigned
    emails_to_unassign = [email for email in (yesterday_emails - today_emails) 
                         if email not in Config.EXEMPT_USERS]
    
    # Track any exempt users that would have been unassigned
    exempted_users = [email for email in (yesterday_emails - today_emails) 
                     if email in Config.EXEMPT_USERS]
    
    if exempted_users:
        print("\n🛡️  The following users are exempt from unassignment:")
        for email in exempted_users:
            print(f"  • {email}")
        print()
    
    # Find emails that are only in today (need to assign)
    emails_to_assign = today_emails - yesterday_emails
    
    print(f"\n📊 Summary:")
    print(f"- Found {len(emails_to_unassign)} users to unassign")
    print(f"- Found {len(emails_to_assign)} users to assign")
    
    # Unassign licenses from yesterday's users
    if emails_to_unassign:
        print(f"\n🔴 Unassigning licenses for {len(emails_to_unassign)} users...")
        for i, email in enumerate(emails_to_unassign, 1):
            print(f"{i}. Unassigning from {email}...", end=" ")
            try:
                if unassign_license(email):
                    print("✅ Done")
                else:
                    print("❌ Failed")
                    failed_unassign.append((email, "Failed to unassign license"))
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Error: {error_msg}")
                failed_unassign.append((email, error_msg))
            # Add a small delay to avoid hitting rate limits
            # time.sleep(1)
    else:
        print("\nℹ️ No users to unassign from yesterday.")
    
    # Assign licenses to today's users
    if emails_to_assign:
        print(f"\n🟢 Assigning licenses to {len(emails_to_assign)} users...")
        for i, email in enumerate(emails_to_assign, 1):
            print(f"{i}. Assigning to {email}...", end=" ")
            try:
                if assign_license(email):
                    print("✅ Done")
                else:
                    print("❌ Failed")
                    failed_assign.append((email, "Failed to assign license"))
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Error: {error_msg}")
                failed_assign.append((email, error_msg))
            # Add a small delay to avoid hitting rate limits
            # time.sleep(1)
    else:
        print("\nℹ️ No new users to assign licenses to today.")
    
    # Prepare summary message
    total_unassigned = len(emails_to_unassign)
    total_assigned = len(emails_to_assign)
    success_unassign = total_unassigned - len(failed_unassign)
    success_assign = total_assigned - len(failed_assign)
    
    # Format failed operations for the message
    def format_failed_operations(failed_list, operation_type):
        if not failed_list:
            return "• No failures"
        return "\n".join([f"• {email}: {error}" for email, error in failed_list])
    
    # Format the error messages
    unassign_errors = format_failed_operations(failed_unassign, "unassign")
    assign_errors = format_failed_operations(failed_assign, "assign")
    
    # Format exempt users list
    exempt_users_list = "\n".join([f"• {email}" for email in Config.EXEMPT_USERS]) or "• None"
    
    # Format exempted users in this run
    exempted_in_run = "\n".join([f"• {email}" for email in exempted_users]) if 'exempted_users' in locals() and exempted_users else "• None"
    
    current_time = datetime.now()
    summary = f"""
<b>📊 License Management Summary</b>
==========================
📅 <b>Date:</b> {current_time.strftime('%Y-%m-%d')}
⏰ <b>Time:</b> {current_time.strftime('%H:%M:%S %Z')}

<b>🔴 Unassigned:</b> {success_unassign}/{total_unassigned}
<b>🟢 Assigned:</b> {success_assign}/{total_assigned}

<b>🛡️ Exempt Users (Never Unassigned):</b>
{exempt_users_list}

<b>🛡️ Exempted in This Run:</b>
{exempted_in_run}

<b>❌ Failed Unassignments:</b>
{unassign_errors}

<b>❌ Failed Assignments:</b>
{assign_errors}

✅ <b>Completed Successfully</b>
"""
    
    # Send summary via Telegram
    send_telegram_message(summary)
    
    print("\n" + "=" * 50)
    print("✅ License management completed!")
    print("📱 Notification sent to Telegram")

if __name__ == "__main__":
    manage_licenses()
