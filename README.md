# Discord Codeforces Verification Bot

A Discord bot to verify users with their Codeforces handle and display their rating and rank.

## Features

- **/verify**: Start the verification process with your Codeforces handle.
- **/status**: Check your current verification status.
- **/reset**: Reset your verification and remove your data.
- **/info**: Get information about a user's Codeforces status.

## Setup

### Requirements

- Python 3.8+
- The following Python packages (see `requirements.txt`):

### Environment Variables

Create a `.env` file in the root or `src/config/` directory with:

```
BOT_TOKEN=your_discord_bot_token
```

### Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set up your `.env` file as described above.

### Running the Bot

Start the bot with:

```
python run.py
```

## Usage

### Verification Process

1. Use `/verify <your_codeforces_handle>` to start.
2. The bot will give you a verification code.
3. Go to your Codeforces profile settings and set your **organization** to the provided code.
4. Run `/verify <your_codeforces_handle>` again to complete verification.

### Other Commands

- `/status`: Shows your verification status and Codeforces info.
- `/reset`: Removes your verification and data (confirmation required).
- `/info <user>`: Shows Codeforces info for a user (if registered).

## Conditions & Notes

- You must have a valid Codeforces handle.
- The bot requires permission to manage roles in your Discord server.
- The database is created automatically in `src/data/bot.db`.
- The bot uses the Codeforces API and may be subject to rate limits.
