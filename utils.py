import csv


def csv_handler(filename, csv_content, headers):
    # Open/create a file to append data to
    filepath = f'scraped_tweets_csv/{filename}.csv'
    csv_file = open(filepath, 'w', newline='', encoding='utf8')

    # Use csv writer
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(headers)

    row = []
    for item in csv_content:
        for key in headers:
            row.append(item[key])
        csv_writer.writerow(row)
        row = []

    csv_file.close()
    print(f'Check out scraped_tweets_csv/{filename}.csv')


def get_key_list(my_dict):
    return list(my_dict.keys())
