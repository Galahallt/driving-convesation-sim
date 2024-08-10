import logging
from pathlib import Path

# Configure logging with timestamps
logging.basicConfig(filename=Path(__file__).parent / "logs" / "conversation_logs.csv", 
                    level=logging.INFO, 
                    format='%(asctime)s,%(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

# Simulated conversation loop
while True:
    user_input = input("You: ")
    logging.info(f"You,{user_input}")
    
    if user_input.lower() in ["exit", "quit"]:
        break
    
    response = f"Bot,This is a response to '{user_input}'."
    print(response)
    logging.info(response)