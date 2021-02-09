import pandas as pd
import re

df = pd.read_csv('rt_content_dir/rt_content.csv')
most_retweeted = df['rt_id'].value_counts()[:25].sort_values(ascending=False)

# who_was_rt = []
variables = ['rts']
iramuteq_file = open(
    f'./rt_content_dir/mais_rts.txt',
    "w", encoding="utf-8")

inicia_comando = "*" * 4
for i in range(0, 25):
    rows = df.loc[df['rt_id'] == most_retweeted.index[i]]
    conteudo = rows['content_of_rt'].iloc[0]
    # who_was_rt.append(rows['who_was_rt'].iloc[0])

    p = re.compile('\w+')  # retira todos os simbolos não alfa-numericos
    description = p.findall(conteudo)
    description = ' '.join(description)
    line = f'{inicia_comando} '
    for variable in variables:
        line += f'*{variable} '
    line += f'\n{description}\n\n'
    iramuteq_file.write(line)
