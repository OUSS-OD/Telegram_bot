🤖 OUSS MANAGER BOT - USER GUIDE
================================

🎯 WHAT IS OUSS MANAGER BOT?
Ouss Manager Bot is your personal mission/task manager on Telegram.
It helps you track your projects, mark them as done, and stay productive!

🔗 BOT LINK: @ouss_manager_bot

🚀 MAIN FEATURES:
=================
1. ➕ ADD NEW MISSIONS - Create tasks with timestamps
2. 🎯 VIEW ACTIVE MISSIONS - See what's in progress
3. ✅ VIEW COMPLETED MISSIONS - See your victories
4. 📋 VIEW ALL MISSIONS - Complete overview
5. ✅ MARK AS COMPLETED - Celebrate your wins
6. 🗑️ DELETE MISSIONS - Remove unwanted tasks

📝 HOW TO USE THE BOT:
======================
1. START THE BOT:
   - Type: /start
   - Or click: "Start" button

2. ADD A NEW MISSION:
   - Click "➕ NEW MISSION"
   - Type your mission/task
   - Bot will save it with current date/time

3. VIEW YOUR MISSIONS:
   - "🎯 ACTIVE MISSIONS" - Tasks in progress
   - "✅ COMPLETED MISSIONS" - Finished tasks
   - "📋 ALL MISSIONS" - Everything

4. MANAGE MISSIONS:
   - For active missions: "✅ COMPLETE" or "🗑️ DELETE"
   - For completed missions: "🗑️ DELETE" only

🌟 SPECIAL MOTIVATIONAL MESSAGES:
==================================
• When adding: "Hey [Name] what's your new project?"
• After adding: "Okay [Name], make it done soon!"
• When viewing active: "[Name] - DO THEM!"
• When completing: "[Name] YOU DID IT! Let's move to the next challenge!"

💾 DATA STORAGE:
================
• All missions saved in SQLite database (tasks.db)
• Each mission stores:
  - Mission text
  - Creation date/time
  - Completion date/time (if done)
  - Status (progress/done)
• Data persists even if bot restarts

🖥️ HOW TO RUN THE BOT LOCALLY:
==============================
1. Install Python 3.7+
2. Install required library:
   pip install python-telegram-bot

3. Run the bot:
   python ouss_bot.py

4. Keep CMD window open while using bot

⚠️ IMPORTANT NOTES:
===================
• Bot only works when CMD window is open
• Close CMD = Bot stops working
• Token must be kept SECRET (never share)
• Each user sees only their own missions

🔧 TROUBLESHOOTING:
===================
1. Bot not responding?
   - Check CMD window is open
   - Check internet connection

2. "Module not found" error?
   - Run: pip install python-telegram-bot

3. Token not working?
   - Get new token from @BotFather
   - Update TOKEN in ouss_bot.py

🔄 RESTARTING THE BOT:
======================
1. In CMD, press Ctrl+C to stop
2. Run again: python ouss_bot.py

📊 DATABASE LOCATION:
=====================
• File: tasks.db (in same folder as bot)
• Can be opened with SQLite browser
• Back up this file to save your data

🎨 CUSTOMIZATION:
=================
You can modify:
• Messages in the code
• Button texts
• Emojis
• Date format

📱 TELEGRAM FEATURES USED:
==========================
• Inline keyboards
• Callback queries
• Conversation handlers
• Markdown formatting
• User data storage

🔒 SECURITY:
============
• Each user ID is tracked separately
• No personal data shared
• Token protected in code
• Database local to your machine

📞 SUPPORT:
===========
If you need help with the bot, contact the developer!

🎯 PRO TIPS:
============
• Use clear mission descriptions
• Complete missions daily
• Review completed missions for motivation
• Delete old/unnecessary missions

⭐ ENJOY STAYING PRODUCTIVE WITH OUSS MANAGER BOT!
==================================================