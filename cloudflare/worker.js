import { handleGroupsCommand } from './groups.js';
import { handleNewSongs } from './handleNewSongs.js';



async function sendMessage(chatId, text, env) {
  const BOT_TOKEN = env.BOT_TOKEN || '';
  const TELEGRAM_API = `https://api.telegram.org/bot${BOT_TOKEN}`;
  await fetch(`${TELEGRAM_API}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text }),
  });
}

export default {
  async fetch(request, env) {
    
    if (request.method !== "POST") {
      return new Response("Invalid request method", { status: 405 });
    }

    let update;
    try {
      update = await request.json();
    } catch {
      return new Response("Invalid JSON", { status: 400 });
    }

    const message = update.message;
    if (!message || !message.text) {
      return new Response("No message text found", { status: 400 });
    }

    const chatId = message.chat.id;
    const userName = message.from.username || "Unknown User";
    const userId = message.from.id;
    const text = message.text.trim();

    const lowerText = text.toLowerCase();

    // Handle group commands
    const groupCmds = ['/makegroup', '/addartist', '/removeartist', '/removegroup'];
    if (groupCmds.some(cmd => lowerText.startsWith(cmd))) {
      const reply = await handleGroupsCommand(env, userId, text);
      await sendMessage(chatId, reply, env);
      return new Response("OK", { status: 200 });
    }

    // Handle /newsongs command
    if (lowerText.startsWith('/newsongs')) {
      const artistName = text.slice(9).trim();
      if (!artistName) {
        await sendMessage(chatId, "Please provide an artist name. Usage: /NewSongs Selena Gomez", env);
        return new Response("OK", { status: 200 });
      }
      const reply = await handleNewSongs(artistName);
      await sendMessage(chatId, reply, env);
      return new Response("OK", { status: 200 });
    }

    // Default fallback
    await sendMessage(chatId, `Hello, ${userName} (ID: ${userId})!\nTry /NewSongs artist_name or group commands like /MakeGroup, /AddArtist.`,env);
    return new Response("OK", { status: 200 });
  }
};
