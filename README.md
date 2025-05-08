# Discord Codeforces Verification Bot

A Discord bot that verifies users by linking their Discord accounts with their Codeforces handles.

## Features

- Verify users by linking Discord accounts with Codeforces handles
- Check verification status
- Rate-limited API calls to Codeforces
- Proper error handling and logging
- Scalable and maintainable codebase

## Project Structure

```
src/
├── bot/
│   ├── api/            # API clients
│   ├── cogs/           # Discord cogs
│   ├── config/         # Configuration
│   ├── models/         # Database models
│   └── utils/          # Utility functions
├── tests/              # Test files
└── docs/              # Documentation
```

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:

```
BOT_TOKEN=your_discord_bot_token
```

5. Run the bot:

```bash
python -m src.bot.bot
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Write tests if applicable
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

### Adding New Features

1. Create a new cog in `src/bot/cogs/`
2. Add any new API clients in `src/bot/api/`
3. Add database models in `src/bot/models/`
4. Add utility functions in `src/bot/utils/`
5. Update configuration in `src/bot/config/`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
