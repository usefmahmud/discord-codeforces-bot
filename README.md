# Discord Codeforces Challenge Bot
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/usefmahmud/discord-codeforces-bot)

A Discord bot that integrates with Codeforces to create coding challenges between users, track progress, and foster competitive programming growth.

## Features

### Current Implementation

- **User Verification System**

  - Link Discord account to Codeforces handle
  - Verification via Codeforces organization field
  - Automatic role assignment based on Codeforces rank

- **Information Commands**

  - `/info` - View user profile information
  - `/status` - Check verification status
  - `/reset` - Reset account verification

- **Leaderboard System**

  - `/leaderboard` command with different scopes
  - Ranking based on Codeforces ratings
  - Visual indicators for different ranks

- **Codeforces API Integration**
  - User data retrieval
  - Rating and rank tracking
  - Rate-limited API requests

## Project Roadmap

### Sprint 1: Challenge System Implementation

- Create `/challenge` command for random problems
- Implement challenge acceptance system
- Build solution verification via Codeforces submissions API
- Track challenge statistics

### Sprint 2: Solo Mode Implementation

- Add `/solo` command for personal practice
- Allow filtering by rating, difficulty, and tags
- Implement progress tracking
- Provide personalized problem recommendations

### Sprint 3: Enhanced User Experience

- Improve command responses with rich embeds
- Create user statistics dashboard
- Enhance error handling and feedback
- Add visual progress indicators

### Sprint 4: Community Features

- Implement server-wide challenges
- Add group competitions
- Create event scheduling for contests
- Build reward system

## Future Enhancements

- Contest notification system
- Achievements and badges
- Educational resources and learning paths

## Technical Requirements

- Python 3.8+
- discord.py
- SQLite database
- Codeforces API access

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your Discord bot token:
   ```
   BOT_TOKEN=your_discord_bot_token
   ```
4. Run the bot: `python -m src.bot`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
