# -*- coding: utf-8 -*-
"""
list prompt example
"""
from __future__ import print_function, unicode_literals
from PyInquirer import prompt, Separator, style_from_dict, Token

from pyfiglet import Figlet, figlet_format
from rich import print

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def action_choices(answers):
    choices = ['Nenhuma opção encontrada ):']
    if answers['action'] == 'Realizar Busca de Tweets':
        choices = [
            Separator('= Algoritmos ='),
            'Buscar por termo',
            'Buscar por hashtag'
        ]
        return choices
    elif answers['action'] == 'Buscar Usuário':
        choices = [
            # Separator('= Isso irá abrir seu navegador ='),
            # 'Link: ...'
            Separator('= EM BREVE =')
        ]
        return choices
    elif answers['action'] == 'Dicas para Gráficos e Análises':
        message = ''
        choices = [
            Separator('= Links e tutoriais que podem ajudar ='),
            'Link1: ...',
            'Link2: ...'
        ]
        return choices
    elif answers['action'] == 'Sair':
        raise SystemExit
    return choices


question = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'O que deseja fazer?',
        'choices': [
            'Realizar Busca de Tweets',
            Separator('= Extras ='),
            'Algoritmo Genetico Interativo',
            'Dicas para Gráficos e Análises',
            'Sair'
        ]
    },
    {
        'type': 'list',
        'name': 'which',
        'message': 'Escolha uma opção..',
        'choices': action_choices,
    },
]

main_title = figlet_format('Scraper CLI', font='slant')
print(f'[bold blue]'
      f'{main_title}'
      f'[/bold blue]')
try:
    while True:
        answers = prompt(question, style=style)
except KeyError:
    print('Ocorreu algum problema...tente executar novamente!')

