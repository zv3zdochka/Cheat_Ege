
url = f"{subject_url}/test?id={page_id}"

    if page_id % 1000 == 0:
        print(f"Processing page {page_id}...")

    try:
        with requests.Session() as session:
            response = session.get(url)

            if response.status_code == 200:
                text = BeautifulSoup(response.text, 'html.parser').get_text()