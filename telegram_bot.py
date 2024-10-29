from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess
import time
import threading
import requests
import random

GROUP_CHAT_ID = <YOUR_GROUP_CHAT_ID>
BOT_TOKEN = "<YOUR_BOT_TOKEN>"
START_COMMAND = "screen -S minecraft -d -m java -Xmx1024M -jar paper-1.21.1-128.jar nogui"

def auto_save():
    while True:
        if subprocess.run("screen -list | grep -q 'minecraft'", shell=True).returncode == 0:
            print("[+] Guardando mundo...")
            subprocess.run("screen -S minecraft -p 0 -X stuff 'say Mundo Guardado!\\n'", shell=True)
            time.sleep(5)
            subprocess.run("screen -S minecraft -p 0 -X stuff 'save-all\\n'", shell=True)
            time.sleep(500)
        else:
            print("[+] El servidor ha sido detenido, finalizando el autoguardado.")
            break

async def start_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == GROUP_CHAT_ID:
        check_command = "screen -list | grep -q 'minecraft'"
        check_result = subprocess.run(check_command, shell=True)

        if check_result.returncode == 0:
            await update.message.reply_text("⚠️ El servidor ya está ejecutado.")
        else:
            subprocess.Popen(START_COMMAND, shell=True)
            await update.message.reply_text("🟢 Servidor de Minecraft iniciado!")
            
            threading.Thread(target=auto_save, daemon=True).start()

async def stop_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == GROUP_CHAT_ID:
        subprocess.run("screen -S minecraft -p 0 -X stuff 'stop\\n'", shell=True, check=True)
        await update.message.reply_text("🔴 Servidor de Minecraft detenido.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_command = "screen -list | grep -q 'minecraft'"
    check_result = subprocess.run(check_command, shell=True)

    if check_result.returncode == 0:
        await update.message.reply_text("🟢 El servidor de Minecraft está actualmente en ejecución.")
    else:
        await update.message.reply_text("🔴 El servidor de Minecraft está actualmente detenido.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📜 *Comandos Disponibles*:\n\n"
        "/start o /iniciar - Inicia el servidor de Minecraft.\n"
        "/stop o /detener - Detiene el servidor de Minecraft.\n"
        "/status o /estado - Muestra el estado del servidor.\n"
        "/help o /ayuda - Muestra esta ayuda."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_server))
    app.add_handler(CommandHandler("iniciar", start_server))
    app.add_handler(CommandHandler("stop", stop_server))
    app.add_handler(CommandHandler("detener", stop_server))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ayuda", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("estado", status))
    app.run_polling()
