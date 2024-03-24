try:
    import time
    import sys
    import os
    from bs4 import BeautifulSoup
    from concurrent.futures import ThreadPoolExecutor
    import concurrent
    import requests
    from sdamgia import SdamGIA
except ModuleNotFoundError:
    sys.exit("Required libraries are missing. Please install them using:\n"
             "pip install -r requirements.txt\n"
             "You can find the requirements.txt file at: https://github.com/zv3zdochka/LAW.git")

subject_url = ''
targets = []


def check_page(page_id: int) -> str:
    """
    Check if the given page contains the target text or JavaScript.

    Args:
    page_id (int): The ID of the page to check.

    Returns:
    str: Result of the page check.
    """
    url = f"{subject_url}/test?id={page_id}"

    if page_id % 1000 == 0:
        print(f"Processing page {page_id}...")

    try:
        with requests.Session() as session:
            response = session.get(url)

            if response.status_code == 200:
                text = BeautifulSoup(response.text, 'html.parser').get_text()

                if len(text) == 118:
                    return f"Page not found: {page_id}"

                for target in targets:
                    if target in text:
                        return f"Target {target} found on page {page_id}"

                if "JavaScript" in text:
                    return "JavaScript detected on the page"

    except Exception as e:
        return f"Error processing page {page_id}: {e}"


def get_current_test_num(subj: str) -> int:
    """
    Get the current test number for the given subject.

    Args:
    subj (str): The subject for which to get the current test number.

    Returns:
    int: The current test number.
    """
    try:
        sdamgia = SdamGIA()
        current_test_num = int(sdamgia.generate_test(subj, {1: 1}))
        del sdamgia
        return current_test_num
    except Exception:
        exit("Switch off your VPN and try again")


def id_generator_up(start_id: int, end_id: int):
    """
    Generate IDs from start_id up to end_id.

    Args:
    start_id (int): The starting ID.
    end_id (int): The ending ID.
    """
    while start_id <= end_id:
        yield start_id
        start_id += 1
    time.sleep(10)
    exit("All variants have been iterated")


def id_generator_down(start_id: int, end_id: int):
    """
    Generate IDs from start_id down to end_id.

    Args:
    start_id (int): The starting ID.
    end_id (int): The ending ID.
    """
    while start_id >= end_id:
        yield start_id
        start_id -= 1
    time.sleep(10)
    exit("All variants have been iterated")


def main(generator, start_id: int, end_id: int):
    """
    Main function for processing pages.

    Args:
    generator (function): The generator function for generating IDs.
    start_id (int): The starting ID.
    end_id (int): The ending ID.
    """
    threads = os.cpu_count() * 3
    with ThreadPoolExecutor(max_workers=threads) as executor:
        ids = generator(start_id, end_id)
        futures = {executor.submit(check_page, next(ids)): id for id in range(100)}

        while futures:
            done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

            for future in done:
                page_id = futures.pop(future)

                try:
                    result = future.result()
                    if result:
                        print(result)

                except Exception as exc:
                    print(f"Exception processing page {page_id}: {exc}")

                new_id = next(ids)
                futures[executor.submit(check_page, new_id)] = new_id


def search_from_to(start: int, end: int):
    """
    Search for targets from start to end.

    Args:
    start (int): The starting ID.
    end (int): The ending ID.
    """
    start_time = time.time()
    main(id_generator_up, start, end)
    elapsed_time = time.time() - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")


def search_from_to_last(start: int):
    """
    Search for targets from start to the current test number.

    Args:
    start (int): The starting ID.
    """
    end = get_current_test_num(subject_name)
    start_time = time.time()
    main(id_generator_up, start, end)
    elapsed_time = time.time() - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")


def search_from_current_to_end(end: int):
    """
    Search for targets from the current test number to end.

    Args:
    end (int): The ending ID.
    """
    start_id = get_current_test_num(subject_name)
    start_time = time.time()
    main(id_generator_down, start_id, end)
    elapsed_time = time.time() - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")


def search_from_current_for_first():
    """
    Search for targets from the current test number endlessly.
    """
    start_id = get_current_test_num(subject_name)
    start_time = time.time()
    main(id_generator_down, start_id, 0)
    elapsed_time = time.time() - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")


def subject_url_by_name(name: str):
    """
    Get the URL of the subject by its name.

    Args:
    name (str): The name of the subject.

    Returns:
    str: The URL of the subject.
    """
    subjects = {
        'math': 'https://math-ege.sdamgia.ru',
        'mathb': 'https://mathb-ege.sdamgia.ru',
        'phys': 'https://phys-ege.sdamgia.ru',
        'inf': 'https://inf-ege.sdamgia.ru',
        'rus': 'https://rus-ege.sdamgia.ru',
        'bio': 'https://bio-ege.sdamgia.ru',
        'en': 'https://en-ege.sdamgia.ru',
        'chem': 'https://chem-ege.sdamgia.ru',
        'geo': 'https://geo-ege.sdamgia.ru',
        'soc': 'https://soc-ege.sdamgia.ru',
        'de': 'https://de-ege.sdamgia.ru',
        'fr': 'https://fr-ege.sdamgia.ru',
        'lit': 'https://lit-ege.sdamgia.ru',
        'sp': 'https://sp-ege.sdamgia.ru',
        'hist': 'https://hist-ege.sdamgia.ru',
    }
    return subjects.get(name)


if __name__ == "__main__":
    # Don't forget to install requirements.txt from https://github.com/zv3zdochka/LAW.git

    targets = ["Щербина", "Смирнова"]
    subject_name = 'math'
    start = 55120100
    end = 7_439_3000
    subject_url = subject_url_by_name(subject_name)
    # search_from_current_for_first() # Views all options from just created to the very first one
    # search_from_current_to_end(end)  # Views all options from just created to end
    search_from_to(start, end)  # Views all options from start to end
    # search_from_to_last(start)  # Views all options from start to just created
    sys.exit(1)
