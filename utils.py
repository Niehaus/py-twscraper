import csv
import os

def csv_handler(filename, csv_content, headers):
    # Open/create a file to append data to
    filepath = f'{filename}.csv'
    csv_file = open(filepath, 'w+', newline='', encoding='utf8')

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


def write_gephi_files(graph, filename):
    # Get headers for Gephi csv files
    nodes_headers = get_key_list(graph.nodes[-1])
    edges_headers = get_key_list(graph.edges[-1])

    # Write node file
    file = f'{filename}_nodes'
    csv_handler(
        file,
        graph.nodes,
        nodes_headers
    )

    # Write edges file
    file = f'{filename}_edges'
    csv_handler(
        file,
        graph.edges,
        edges_headers
    )


def write_rts(tweet):
    filepath = f'rt_content_dir/rt_content.csv'

    if not os.path.isfile(filepath):
        csv_file = open(filepath, 'a', newline='', encoding='utf8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['rt_id',
                             'who_was_rt',
                             'content_of_rt']
                            )
    else:
        csv_file = open(filepath, 'a', newline='', encoding='utf8')
        csv_writer = csv.writer(csv_file)

    row = [tweet['rt_id'], tweet['who_was_rt'], tweet['content_of_rt']]
    csv_writer.writerow(row)
    csv_file.close()
    # print(f'Retweet written to {filepath}')


def get_key_list(my_dict):
    return list(my_dict.keys())
