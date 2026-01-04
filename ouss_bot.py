import logging
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


TOKEN = "YOUR_TOKEN"

# Initialize database
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_text TEXT NOT NULL,
            status TEXT DEFAULT 'progress',
            created_date TEXT NOT NULL,
            completed_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Get user's first name
def get_user_name(update: Update):
    user = update.effective_user
    return user.first_name

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = get_user_name(update)
    keyboard = [
        [InlineKeyboardButton("➕ NEW MISSION", callback_data='add_task')],
        [InlineKeyboardButton("🎯 ACTIVE MISSIONS", callback_data='view_tasks')],
        [InlineKeyboardButton("✅ COMPLETED MISSIONS", callback_data='view_done')],
        [InlineKeyboardButton("📋 ALL MISSIONS", callback_data='view_all')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🚀 **BOSS MODE ACTIVATED**\n\n"
        f"Hey {user_name}! Ready to dominate your day?\n\n"
        f"**YOUR ARSENAL:**\n"
        f"• ➕ Add new missions\n"
        f"• ✅ Mark as completed\n"
        f"• 🗑️ Delete missions\n"
        f"• 📊 Track your productivity\n\n"
        f"Choose your action:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Add a mission
async def add_task_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_name = get_user_name(update)
    await query.edit_message_text(f"🎯 **Hey, {user_name} what's your new project?**\n\nWrite your new mission:")
    return "GET_TASK"

async def get_task_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_text = update.message.text
    user_id = update.effective_user.id
    user_name = get_user_name(update)
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save to database
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (user_id, task_text, status, created_date) VALUES (?, ?, ?, ?)",
        (user_id, task_text, 'progress', created_date)
    )
    conn.commit()
    conn.close()
    
    keyboard = [[InlineKeyboardButton("🎯 VIEW MY MISSIONS", callback_data='view_tasks')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🔥 **NEW MISSION ADDED!**\n\n"
        f"📌 **Mission:** {task_text}\n"
        f"📅 **Started:** {created_date}\n"
        f"⚡ **Status:** IN PROGRESS\n\n"
        f"💪 **Okay {user_name}, make it done soon!**",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return ConversationHandler.END

# View missions
async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE, status_filter=None):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    user_name = get_user_name(update)
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    if status_filter == 'done':
        cursor.execute(
            "SELECT id, task_text, created_date, completed_date FROM tasks WHERE user_id = ? AND status = 'done' ORDER BY completed_date DESC",
            (user_id,)
        )
        title = f"🏆 **{user_name.upper()}'S VICTORIES**"
    elif status_filter == 'all':
        cursor.execute(
            "SELECT id, task_text, status, created_date, completed_date FROM tasks WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        )
        title = f"📊 **{user_name.upper()}'S BATTLEFIELD**"
    else:
        cursor.execute(
            "SELECT id, task_text, created_date FROM tasks WHERE user_id = ? AND status = 'progress' ORDER BY created_date",
            (user_id,)
        )
        title = f"🎯 **{user_name.upper()}'S ACTIVE MISSIONS**"
    
    tasks = cursor.fetchall()
    conn.close()
    
    if not tasks:
        keyboard = [[InlineKeyboardButton("➕ NEW MISSION", callback_data='add_task')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"{title}\n\n🎪 **EMPTY ARENA!**\n\nNo active missions. Create one!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    tasks_text = ""
    keyboard = []
    
    # Motivational message based on mission count
    if status_filter is None and len(tasks) > 0:
        tasks_text += f"💥 **{user_name.upper()} - DO THEM!** 💥\n\n"
    
    for task in tasks:
        if status_filter == 'done':
            task_id, task_text, created_date, completed_date = task
            tasks_text += f"🏅 **MISSION {task_id} - COMPLETED**\n"
            tasks_text += f"📝 {task_text}\n"
            tasks_text += f"📅 Started: {created_date}\n"
            tasks_text += f"🏁 Finished: {completed_date}\n\n"
            
            keyboard.append([
                InlineKeyboardButton(f"🗑️ DELETE {task_id}", callback_data=f'delete_{task_id}')
            ])
            
        elif status_filter == 'all':
            task_id, task_text, status, created_date, completed_date = task
            status_icon = "🏆" if status == 'done' else "🎯"
            tasks_text += f"{status_icon} **MISSION {task_id}**\n"
            tasks_text += f"📝 {task_text}\n"
            tasks_text += f"📅 Started: {created_date}\n"
            if completed_date:
                tasks_text += f"🏁 Finished: {completed_date}\n"
            tasks_text += f"⚡ Status: {'COMPLETED' if status == 'done' else 'IN PROGRESS'}\n\n"
            
            if status == 'progress':
                keyboard.append([
                    InlineKeyboardButton(f"✅ COMPLETE {task_id}", callback_data=f'done_{task_id}'),
                    InlineKeyboardButton(f"🗑️ DELETE {task_id}", callback_data=f'delete_{task_id}')
                ])
            else:
                keyboard.append([
                    InlineKeyboardButton(f"🗑️ DELETE {task_id}", callback_data=f'delete_{task_id}')
                ])
                
        else:
            task_id, task_text, created_date = task
            tasks_text += f"🎯 **MISSION {task_id}**\n"
            tasks_text += f"📝 {task_text}\n"
            tasks_text += f"📅 Started: {created_date}\n\n"
            
            keyboard.append([
                InlineKeyboardButton(f"✅ COMPLETE {task_id}", callback_data=f'done_{task_id}'),
                InlineKeyboardButton(f"🗑️ DELETE {task_id}", callback_data=f'delete_{task_id}')
            ])
    
    # Navigation buttons
    keyboard.append([InlineKeyboardButton("➕ NEW MISSION", callback_data='add_task')])
    keyboard.append([
        InlineKeyboardButton("🎯 ACTIVE", callback_data='view_tasks'),
        InlineKeyboardButton("✅ COMPLETED", callback_data='view_done'),
        InlineKeyboardButton("📋 ALL", callback_data='view_all')
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{title}\n\n{tasks_text}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Mission actions
async def handle_task_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    user_name = get_user_name(update)
    
    if data.startswith('done_'):
        task_id = int(data.split('_')[1])
        completed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get mission text for the message
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT task_text FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )
        task_text = cursor.fetchone()[0]
        
        # Update status
        cursor.execute(
            "UPDATE tasks SET status = 'done', completed_date = ? WHERE id = ? AND user_id = ?",
            (completed_date, task_id, user_id)
        )
        conn.commit()
        conn.close()
        
        await query.answer("🏆 MISSION COMPLETED!")
        
        # Congratulations message
        keyboard = [[InlineKeyboardButton("🎯 NEXT MISSION", callback_data='view_tasks')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            f"🎉 **VICTORY!** 🎉\n\n"
            f"🏆 **{user_name.upper()} YOU DID IT!**\n\n"
            f"✅ Mission completed:\n"
            f"📝 '{task_text}'\n"
            f"🏁 Finished: {completed_date}\n\n"
            f"🚀 **Let's move to the next challenge!**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Refresh view
        await view_tasks(update, context, status_filter=None)
        
    elif data.startswith('delete_'):
        task_id = int(data.split('_')[1])
        
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )
        conn.commit()
        conn.close()
        
        await query.answer("🗑️ Mission deleted!")
        await view_tasks(update, context, status_filter=None)

# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == 'add_task':
        return await add_task_start(update, context)
    elif data == 'view_tasks':
        await view_tasks(update, context, status_filter=None)
    elif data == 'view_done':
        await view_tasks(update, context, status_filter='done')
    elif data == 'view_all':
        await view_tasks(update, context, status_filter='all')
    elif data.startswith('done_') or data.startswith('delete_'):
        await handle_task_action(update, context)
    else:
        await query.answer("Unknown option!")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.")
    return ConversationHandler.END

# Main function
def main():
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_task_start, pattern='^add_task$')],
        states={
            "GET_TASK": [MessageHandler(filters.TEXT & ~filters.COMMAND, get_task_description)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("=" * 50)
    print("🚀 OUSSA MANAGER BOT - BOSS MODE ACTIVATED")
    print("=" * 50)
    print("🔗 Find it on Telegram: @ouss_manager_bot")
    print("📝 Send /start to begin")
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 50)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()