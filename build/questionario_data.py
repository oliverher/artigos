# -*- coding: utf-8 -*-
"""Fonte única do questionário (v0.4, revisado para aplicação). Usada pela página do site e pelos documentos Word."""

TITLE = 'Questionário para Diagnóstico do uso da IA por Servidores Públicos do Estado de GO'
SHORT = 'Diagnóstico do uso da IA por Servidores Públicos do Estado de GO'
STATUS = ('Versão preliminar. O instrumento ainda não passou por pré-teste, por leitura de especialistas nem por apreciação de comitê de ética, '
          'e não deve ser aplicado antes dessas etapas.')

SCALE = ['Discordo totalmente', 'Discordo', 'Nem concordo nem discordo', 'Concordo', 'Concordo totalmente']

DEFINITIONS = [
    "Neste questionário, 'inteligência artificial' (IA) inclui assistentes de texto (como ChatGPT, Copilot e Gemini), tradução e resumo automáticos e sistemas que classificam ou analisam documentos e dados.",
    "'IA generativa' é a IA que produz texto, imagens ou resumos a partir de uma instrução, como os assistentes de texto. 'Usar IA no trabalho' significa usar essas ferramentas em tarefas da sua função. 'Meu órgão' é o órgão ou entidade em que você trabalha hoje.",
]

CONSENT = [
    "Você está sendo convidado(a) a responder um questionário sobre a aprendizagem e o uso de inteligência artificial (IA) no serviço público do Estado de Goiás. A participação é voluntária e anônima: não pedimos seu nome, e-mail, matrícula, órgão nem qualquer dado que permita identificá-lo(a), e as respostas serão analisadas apenas em conjunto. Não há respostas certas ou erradas, e as respostas não serão usadas para avaliar você ou seu órgão. Você pode desistir a qualquer momento fechando a página. O tempo médio é de cerca de 13 minutos. Ao clicar em 'Continuar', você declara ter 18 anos ou mais e concordar em participar.",
    "Dúvidas sobre o estudo: [e-mail do pesquisador responsável]. Parecer do comitê de ética: [número, quando houver].",
]

# (código, enunciado, opções, observação de fluxo)
FILTER = [('F1', 'Você atua hoje no Poder Executivo do Estado de Goiás?', ['Sim', 'Não'], "Se a resposta for 'Não', o questionário se encerra com agradecimento.")]
PROFILE = [
    ('P1', 'Qual é o seu tipo de vínculo atual?',
     ['Servidor(a) efetivo(a), sem função ou cargo comissionado', 'Servidor(a) efetivo(a), com função ou cargo comissionado',
      'Comissionado(a) sem vínculo efetivo com o Estado', 'Temporário(a) ou contratado(a) por tempo determinado', 'Outro vínculo'],
     "Se a resposta for 'Outro vínculo', o questionário se encerra com agradecimento."),
    ('P2', 'Há quanto tempo você trabalha no serviço público estadual?', ['Menos de 2 anos', 'De 2 a 5 anos', 'De 6 a 10 anos', 'De 11 a 20 anos', 'Mais de 20 anos'], ''),
    ('P3', 'Faixa etária', ['Até 29 anos', '30 a 39 anos', '40 a 49 anos', '50 a 59 anos', '60 anos ou mais', 'Prefiro não informar'], ''),
    ('P4', 'Maior nível de escolaridade concluído', ['Ensino médio', 'Ensino superior', 'Pós-graduação', 'Prefiro não informar'], ''),
    ('P5', 'Sua atividade principal é mais próxima de:', ['Atendimento ou entrega direta de serviços ao público', 'Atividades administrativas e de suporte', 'Tecnologia da informação e dados', 'Outra'], ''),
    ('P6', 'Você coordena ou supervisiona outras pessoas?', ['Sim', 'Não', 'Prefiro não informar'], ''),
]
_FREQ = ['Nunca usei', 'Já testei, mas não uso', 'Algumas vezes por mês', 'Algumas vezes por semana', 'Todos os dias']
EXPERIENCE = [
    ('E1', 'Com que frequência você usa IA generativa em tarefas do trabalho?', _FREQ, ''),
    ('E2', 'Com que frequência você usa IA generativa na vida pessoal?', _FREQ, ''),
    ('E3', 'Nos últimos 12 meses, você fez algum curso ou capacitação sobre IA?',
     ['Não', 'Sim, por iniciativa própria', 'Sim, oferecido pelo meu órgão ou pela Escola de Governo', 'Sim, dos dois tipos'], ''),
    ('E4', 'Seu órgão disponibiliza alguma ferramenta de IA aprovada para uso no trabalho?', ['Sim', 'Não', 'Não sei'], ''),
]

# dimensão: (chave, título, instrução, itens[(código, enunciado, invertido, origem)])
V, W, A, AS, P = 'validada', 'wolfe', 'abbad', 'adaptada', 'propria'
ORIG = {
    'validada': 'Escala validada em português',
    'wolfe': 'Traduzida e adaptada de Wolfe et al. (2025), sem validação nesta forma',
    'abbad': 'Adaptada de Abbad e Sallorenzo (2001), sem validação nesta forma',
    'propria': 'Redação própria, sem validação',
}
DIMS = [
    ('iap', 'Intenção de aprender IA', 'Pense no seu trabalho atual.', [
        ('IAP1', 'Pretendo buscar cursos ou materiais para aprender a usar IA nos próximos 6 meses.', False, P),
        ('IAP2', 'Estou disposto(a) a dedicar tempo para aprender a usar IA no meu trabalho.', False, P),
        ('IAP3', 'Pretendo aprender a usar IA por iniciativa própria, mesmo sem curso oferecido pelo meu órgão.', False, P),
        ('IAP4', 'Quero entender como a IA funciona, seus limites e seus riscos, e não apenas saber usá-la.', False, P)]),
    ('iu', 'Intenção de usar IA', 'Pense no seu trabalho atual.', [
        ('IU1', 'Pretendo usar IA no meu trabalho no próximo mês.', False, W),
        ('IU2', 'Pretendo usar IA no meu trabalho nos próximos seis meses.', False, W)]),
    ('ac', 'Apoio da chefia imediata e dos colegas', "Pense no seu local de trabalho atual. Nos itens sobre a chefia, inclua a opção 'Não tenho chefia imediata'.", [
        ('AC1', 'Minha chefia imediata me encoraja a usar IA no meu trabalho.', False, A),
        ('AC2', 'Minha chefia imediata ajuda a remover obstáculos para eu usar IA no trabalho.', False, A),
        ('AC3', 'Quando tenho dificuldade em usar IA no trabalho, recebo orientação sobre como fazê-lo.', False, A),
        ('AC4', 'Recebo reconhecimento quando uso IA de forma adequada no trabalho.', False, A),
        ('AC5', 'Meus colegas mais experientes apoiam minhas tentativas de usar IA no trabalho.', False, A)]),
    ('te', 'Tempo para aprender', 'Pense no seu local de trabalho atual.', [
        ('TE1', 'Tenho tempo dentro da minha jornada para estudar novas ferramentas.', False, P),
        ('TE2', 'Posso participar de cursos durante o horário de trabalho.', False, P),
        ('TE3', 'Minha carga de trabalho deixa espaço para eu experimentar novas formas de trabalhar.', False, P),
        ('TE4', 'Meu volume de trabalho me impede de dedicar tempo a aprender coisas novas.', True, P)]),
    ('af', 'Acesso a ferramentas e cursos', 'Pense no seu local de trabalho atual.', [
        ('AF1', 'Tenho os recursos necessários para usar IA no meu trabalho.', False, W),
        ('AF2', 'Tenho acesso a ferramentas de IA aprovadas pelo meu órgão.', False, P),
        ('ATN', "Para esta linha, marque 'Discordo'.", False, 'controle'),
        ('AF3', 'Meu órgão oferece cursos sobre IA ligados às minhas tarefas.', False, P)]),
    ('se', 'Segurança para experimentar', 'Pense na sua equipe de trabalho direta.', [
        ('SE1', 'Nessa equipe, quando alguém comete um erro, é comum que isso seja usado contra ela no futuro.', True, V),
        ('SE2', 'É fácil discutir problemas ou questões difíceis nessa equipe.', False, V),
        ('SE3', 'Nessa equipe, as pessoas são rejeitadas por serem diferentes.', True, V),
        ('SE4', 'Assumir riscos é completamente seguro nessa equipe.', False, V),
        ('SE5', 'É difícil pedir ajuda a outros membros dessa equipe.', True, V),
        ('SE6', 'Membros dessa equipe respeitam e valorizam as contribuições uns dos outros.', False, V),
        ('SE7', 'Meu órgão não me responsabilizaria injustamente por um erro cometido de boa-fé ao usar IA.', False, P)]),
    ('cr', 'Clareza das regras de uso', 'Pense no seu órgão atual.', [
        ('CR1', 'As regras sobre o que posso e não posso fazer com IA no meu órgão são claras.', False, P),
        ('CR2', 'Há uma pessoa ou equipe a quem posso recorrer no meu órgão para resolver dificuldades com IA.', False, W),
        ('CR3', 'As orientações do meu órgão sobre proteção de dados ao usar IA foram comunicadas de forma clara.', False, P)]),
    ('up', 'Utilidade percebida', 'Pense no seu trabalho atual.', [
        ('UP1', 'Acho a IA útil no meu trabalho.', False, W),
        ('UP2', 'Usar IA me permite concluir tarefas com mais rapidez.', False, W),
        ('UP3', 'Usar IA aumenta minha produtividade.', False, W),
        ('UP4', 'Aprender novas ferramentas me ajudaria a atender melhor a população.', False, P)]),
    ('cf', 'Confiança para usar IA com segurança', 'Pense no seu trabalho atual.', [
        ('CF1', 'Tenho o conhecimento necessário para usar IA no meu trabalho.', False, W),
        ('CF2', 'Sei como proteger dados pessoais e sigilosos ao usar IA.', False, P),
        ('CF3', 'Sei em que situações uma decisão exige revisão humana, mesmo com apoio de IA.', False, P)]),
    ('pp', 'Propósito e contribuição social', 'Indique o quanto você concorda com cada afirmação.', [
        ('PP1', 'Gerar impacto para a sociedade é mais importante do que minhas conquistas individuais.', False, V),
        ('PP2', 'Os acontecimentos do dia a dia sempre me lembram de como somos dependentes uns dos outros.', False, V),
        ('PP3', 'A boa prestação do serviço público é algo muito importante para mim.', False, V),
        ('PP4', 'Eu correria risco de perdas ou danos pessoais para ajudar alguém.', False, V),
        ('PP5', 'Eu estou disposto(a) a fazer sacrifícios pessoais em prol do bem-estar coletivo.', False, V),
        ('CP1', 'Meu trabalho contribui para melhorar a vida da população.', False, P)]),
    ('rc', 'Receios', 'Pense no seu trabalho atual.', [
        ('RC1', 'Tenho receio de que a IA reduza a necessidade do meu cargo ou da minha função.', False, P),
        ('RC2', 'Tenho receio de expor dados sigilosos ao usar ferramentas de IA.', False, P),
        ('RC3', 'Tenho receio de ser responsabilizado(a) por um erro cometido com apoio de IA.', False, P)]),
]
OPEN = [('Q1', 'O que mais ajudaria você a aprender a usar IA no trabalho?'), ('Q2', 'O que mais dificulta o seu aprendizado ou o uso de IA hoje?')]
OPEN_NOTE = 'Não escreva nomes de pessoas, setores ou órgãos.'

N_SCALE = sum(len(d[3]) for d in DIMS)
N_OTHER = len(FILTER) + len(PROFILE) + len(EXPERIENCE)
N_TOTAL = N_SCALE + N_OTHER + len(OPEN)
