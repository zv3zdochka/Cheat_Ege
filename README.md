# Project EGE

Project EGE is aimed at finding test variants created by teachers immediately after their creation.

## Installation

1. Ensure you have Python 3.12 or higher installed.
2. Clone the project repository using the following command:
    ```
    git clone https://github.com/zv3zdochka/Cheat_Ege.git
    ```
3. Navigate to the project directory:
    ```
    cd Cheat_Ege
    ```
4. Install the necessary dependencies using the `requirements.txt` file:
    ```
    pip install -r requirements.txt
    ```

## Files in the Project


1. **Local_Search_async.py**: This file contains asynchronous versions of functions for searching test variants created by teachers. It is intended for running on local machines.

2. **Bot.py**: This file contains the code for the bot components of the project.

3. **Search.py**: This is an optimized server version of a bot designed for educational purposes. It is specifically tailored to monitor web pages for certain content and notify users accordingly.

4. **Local_Search.py**: This file contains functions for searching test variants created by teachers. It supports two search modes: bottom-up and top-down. You can use the functions to search for the test variants on your pc. 

# Using the Files

1. If you want to run the bot locally, you likely need to use either `Local_Search.py` or `Local_Search_async.py`. Choose the appropriate script based on your requirements and run it using Python.

2. If you want to run Search.py on Yandex cloud virtual machine visit VM.md.

## Search.py

## How to Run:

1. **Requirements Installation:**

    Make sure you have Python installed. Then, install the required libraries using pip:

    ```
    pip install -r requirements.txt
    ```


2. **Execution:**

    Run the script using Python:

    ```
    python Search.py
    ```

    Make sure you're in the directory where `Search.py` is located.

3. **Docker:**

    Alternatively, you can run the bot using Docker. Ensure you have Docker installed and the Docker daemon is running. Then, build the Docker image:

    ```
    docker build -t search-bot .
    ```

    Once the image is built, you can run a container from it:

    ```
    docker run -d --name search-bot-container search-bot
    ```

    This will run the bot in a Docker container named `search-bot-container`.

## Optimizations:

- The code is optimized for performance, utilizing asynchronous programming with asyncio to handle multiple tasks concurrently.
- It employs aiohttp for asynchronous HTTP requests, which improves efficiency when fetching web pages.
- The code is designed to minimize downtime and maximize responsiveness, ensuring timely updates and notifications.

## Commands:

- `/allow <user_id>`: Authorize a user to access the bot.
- `/deny <user_id>`: Deny authorization for a user.
- `/help`: Display help information.
- `/admin <user_id>`: Upgrade a user to admin status.
- `/text <message>`: Send a message to all users.
- `/textto <user_id> <message>`: Send a message to a specific user.
- `/users`: Get a list of authorized users.
- `/all`: Get a list of all users.
- `/banned`: Get a list of banned users.
- `/save`: Save bot data to files.
- `/ban <user_id>`: Ban a user from accessing the bot.
- `/free <user_id>`: Release a user from ban.
- `/delete <user_id>`: Delete a user from the bot's records.


## Usage Local_Search.py

1. Edit the variables `targets`, `subject_name`, `start`, and `end` according to your needs:

   - `targets`: List of target texts to search for on web pages.
   - `subject_name`: The name of the EGE subject for which you want to perform the search. Possible values: `'math'`, `'mathb'`, `'phys'`, `'inf'`, `'rus'`, `'bio'`, `'en'`, `'chem'`, `'geo'`, `'soc'`, `'de'`, `'fr'`, `'lit'`, `'sp'`, `'hist'`.
   - `start`: The starting page ID from which the search will begin.
   - `end`: The ending page ID on which the search will end.

2. Run the script. Depending on your needs, uncomment one of the functions in the `if __name__ == "__main__":` block:

   - `search_from_current_for_first()`: View all options from just created to the very first one.
   - `search_from_current_to_end(end)`: View all options from just created to the end.
   - `search_from_to(start, end)`: View all options from start to end.
   - `search_from_to_last(start)`: View all options from start to just created.

3. Upon completion of the script execution, the execution time will be displayed, and the code will exit with code `1`.

## Important

- Make sure you have access to the sdamgia.ru website, you have to use russian ip.
- Before using, ensure that your IP is not being blocked on the sdamgia.ru website.

## Usage Local_Search_async.py

1. Create a JSON file (`data.json`) containing the information about the subjects you want to search. The JSON file should have the following format:

```json
{
  "subject_name1": [["target","target"], 123],
  "subject_name2": [["target","target"], 234]
}
```

Replace `"subject_name"` with the name of the EGE subject, `"targets"` with a list of target texts to search for on web pages, and `"start_id"` with the starting page ID from which the search will begin.

2. Run the script with the following command:

```bash
python Local_Search_async.py data.json
```

Ensure that you pass the correct filename (`data.json`) as an argument.

3. The script will continuously search for the specified targets on the web pages asynchronously. When targets are found, they will be logged in the `found.txt` file along with the subject name and the current time.

4. The script will update the JSON file with the latest information about the last processed page ID for each subject.

5. The script adjusts its sleep time dynamically based on the time taken for each cycle. If a cycle completes too quickly, the sleep time increases slightly, and if it takes too long, the sleep time decreases slightly to optimize performance.

## Important

- Ensure that the JSON file (`data.json`) exists and contains the required information in the correct format.
- Make sure you have access to the sdamgia.ru website, you have to use russian ip.
- Before using, ensure that your IP is not being blocked on the sdamgia.ru website.

# Bot.py

This file is a Telegram bot script designed to manage user authorization and interactions. It includes features such as authorization requests, user banning, message broadcasting, and more.

## Bot Setup

1. **Token**: Replace the `TOKEN` variable with your Telegram bot token obtained from BotFather.

2. **Admin Authorization**: Replace `creator` variable value with your Telegram user id. This user will have admin privileges.

3. **Running the Bot**: Run the script to start the bot.

## Usage

### User Authorization

- When a user sends a message to the bot, they will be prompted for authorization.
- Admins can authorize users using the `/allow` command followed by the user's ID.
- Admins can deny authorization using the `/deny` command followed by the user's ID.

### Commands

- `/help`: Displays help message.
- `/admin <user_id>`: Grants admin privileges to the specified user ID.
- `/text <message>`: Sends the specified message to all users.
- `/textto <user_id> <message>`: Sends the specified message to a specific user.
- `/users`: Displays a list of authorized users.
- `/all`: Displays a dictionary of user IDs and their corresponding usernames.
- `/banned`: Displays a list of banned users.
- `/save`: Sends the bot's data files to the invoking admin.
- `/ban <user_id>`: Bans the specified user.
- `/free <user_id>`: Unbans the specified user.
- `/delete <user_id>`: Deletes the specified user from the list of authorized users.

### Broadcasting

- The bot periodically sends random messages to all authorized users.

## Data Management

- User authorization data is stored in `users.json`.
- Logs are stored in `log.txt`.
- Messages sent by the bot are logged in `found.txt`.

## Important

- Ensure that the bot is authorized to interact with users and has the necessary permissions.
- Use admin commands with caution, especially commands that grant admin privileges or ban users.

