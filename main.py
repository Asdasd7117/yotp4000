import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from utils import download_youtube_video, download_youtube_audio, transcribe_audio_to_srt, merge_video_with_subtitles

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("أرسل رابط فيديو يوتيوب فقط.")
        return

    await update.message.reply_text("📥 تحميل الفيديو...")
    try:
        video_file = download_youtube_video(url)
        audio_file = download_youtube_audio(url)

        await update.message.reply_text("🔊 تحويل الصوت إلى نص...")
        srt_file = transcribe_audio_to_srt(audio_file)

        await update.message.reply_text("🎬 دمج الترجمة مع الفيديو...")
        output_file = merge_video_with_subtitles(video_file, srt_file)

        await update.message.reply_text("✅ إليك الفيديو المترجم:")
        with open(output_file, "rb") as f:
            await update.message.reply_video(f)
    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء المعالجة: " + str(e))

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()