from src.bot import Bot
import pytest
import sys
sys.path.insert(0, "./src/")


@pytest.fixture
def setup_bot():
    return Bot()  # Create an instance of the Bot class for testing


def test_ping_command(bot):
    # Simulate a message context with content "!ping"
    ctx = bot.get_context("ping")
    # Use the bot to process the message context
    bot.process_commands(ctx)
    print(bot.latency)
    # Perform assertions to check if the bot's response is as expected
    assert "Pong!" in ctx.channel.last_message.content

# Add more test cases as needed
