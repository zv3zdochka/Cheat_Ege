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

1. **Local_Search.py**: The main file of the project.

2. **Local_Search_async.py**: This file contains asynchronous versions of functions for searching test variants created by teachers. It is intended for running on local machines.

3. **Bot.py**: This file contains the code for the bot component of the project.

4. **Search.py**: This file contains functions for server-side usage, allowing for searching test variants created by teachers.

5. **Local_Search.py**: This file contains functions for searching test variants created by teachers. It supports two search modes: bottom-up and top-down. You can use the functions to search for the test variants on your pc. 

## Using the Files

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

- Make sure you have access to the sdamgia.ru website.
- Before using, ensure that your IP is not being blocked on the sdamgia.ru website.

## Usage Local_Search_async.py

1. Create a JSON file (`data.json`) containing the information about the subjects you want to search. The JSON file should have the following format:

```json
{
  "subject_name1": [["target","target"], 123],
  "subject_name2": [["target","target"], 234],
  ...
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
- Make sure you have access to the sdamgia.ru website.
- Before using, ensure that your IP is not being blocked on the sdamgia.ru website.

