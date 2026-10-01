"""Troca as figuras SVG do artigo 05 pelas imagens dos slides (PDF enviado pelo autor).

Uso (uma vez): python build/pmbok_figuras.py
Atua sobre src/orig/pmbok-dialetica/index.html; as imagens ficam em src/orig/pmbok-dialetica/img/.
"""
import re

F = 'src/orig/pmbok-dialetica/index.html'
h = open(F, encoding='utf8').read()
assert 'class="shot' not in h, 'figuras já trocadas'


def shot(n, slide, cap, src, alt):
    return ('<figure class="shot reveal" id="slide-%d">\n<figcaption class="cap">Figura %d. %s</figcaption>\n'
            '<a href="../assets/img/pmbok-slide-%02d.jpg" target="_blank" rel="noopener" title="Abrir a imagem em tamanho original">'
            '<img src="../assets/img/pmbok-slide-%02d.jpg" width="1376" height="768" loading="lazy" alt="%s"></a>\n'
            '<figcaption class="src">%s</figcaption>\n</figure>\n') % (n, n, cap, slide, slide, alt, src)


def block(fid):
    return re.search(r'<figure class="fig" id="%s">.*?</figure>\n' % fid, h, re.S).group(0)


MO = 'Fonte: elaborado pelo autor, com base em March (1991) e O’Reilly e Tushman (2013).'
F1 = shot(1, 2, 'O dilema executivo contemporâneo: governança e rastreabilidade contra inovação e velocidade', MO,
          'Dois lados em tensão: à esquerda uma coluna de concreto representando exploitation, governança e rastreabilidade; à direita fitas orgânicas representando exploration, inovação e velocidade; abaixo, a síntese de que a evolução do PMBOK busca reconciliar essa tensão.')
F2 = shot(2, 1, 'A dialética como lente: da estrutura rígida à arquitetura adaptativa', 'Fonte: elaborado pelo autor, com base em Hegel (1977) e Seo e Creed (2002).',
          'Ilustração em que uma estrutura geométrica rígida, à esquerda, se dissolve em uma rede orgânica laranja e se recompõe em uma estrutura em módulos, à direita, representando a trajetória das edições 6, 7 e 8 do PMBOK.')
F3 = (shot(3, 4, 'A tese (6ª edição): a predominância processual, código T', 'Fonte: elaborado pelo autor, com base em PMI (2017).',
           'Estrutura cúbica de vigas azuis e cinza representando a 6ª edição, com 10 áreas de conhecimento, 5 grupos de processos e 49 processos descritos por entradas, ferramentas e técnicas e saídas.')
      + shot(4, 5, 'A antítese (7ª edição): o deslocamento para princípios, código A', 'Fonte: elaborado pelo autor, com base em PMI (2021a, 2021b).',
             'Rede de nós e linhas em tons de laranja representando a 7ª edição, com 12 princípios, 8 domínios de desempenho e tailoring no centro da arquitetura; os grupos de processos passam a ser um dos modelos possíveis.')
      + shot(5, 6, 'A síntese (8ª edição): a recomposição arquitetural, código S', 'Fonte: elaborado pelo autor, com base em PMI (2025).',
             'Rede verde-azulada sobre uma estrutura translúcida representando a 8ª edição, com 6 princípios, 7 domínios de desempenho e reintrodução da orientação de processos ao lado de tailoring.')
      + shot(6, 9, 'Matriz de evolução estrutural do PMBOK® Guide (6ª a 8ª edição)', 'Fonte: elaborado pelo autor, com base em PMI (2017, 2021a, 2025).',
             'Matriz comparando as três edições em arquitetura central, estatuto dos processos e abordagens de entrega, concluindo que o padrão é de recomposição em camadas e não de substituição linear.'))
F4 = (shot(7, 8, 'Ambidestria metodológica: o núcleo teórico da nova arquitetura', MO,
           'Quadrante com os eixos padronização (exploitation) e adaptação (exploration), com a ambidestria metodológica da 8ª edição destacada; ao lado, a distinção entre pluralismo e hibridismo, no nível do projeto, e ambidestria metodológica, no nível da arquitetura do standard.')
      + shot(8, 10, 'Tailoring como a regra de decisão', 'Fonte: elaborado pelo autor, com base em PMI (2025).',
             'Esquema em que os princípios (o porquê) passam por um mecanismo chamado tailoring, a regra de decisão conforme o contexto do projeto, e resultam em orientações práticas e processos (o como).'))
F6 = shot(9, 7, 'A refutação da leitura pendular', 'Fonte: elaborado pelo autor, com base em PMI (2025).',
          'Pêndulo entre processos e agilidade riscado por um X, ao lado de uma hélice que combina estrutura e rede; a conclusão é que a 8ª edição não é um retorno pendular, e sim uma recomposição dialética.')
F8 = shot(11, 11, 'Sustentabilidade como princípio arquitetural', 'Fonte: elaborado pelo autor, com base em Elkington (1997), Silvius e Schipper (2014) e PMI (2025).',
          'Pilar de concreto destacado em verde-azulado, rotulado sustentabilidade, sustentando uma estrutura; ao lado, três blocos de texto sobre o novo status normativo, a evolução do conceito e o alinhamento estratégico.')

for k, v in [('figura-1', F1), ('figura-2', F2), ('figura-3', F3), ('figura-4', F4), ('figura-5', ''), ('figura-6', F6), ('figura-8', F8)]:
    h = h.replace(block(k), v)

# a figura 7 (isomorfismo institucional) não tem slide correspondente: fica como SVG e só muda o número
h = h.replace('Figura 7. Isomorfismo institucional', 'Figura 10. Isomorfismo institucional')

h = h.replace('<div class="tablewrap"><table>\n<thead><tr><th>Proposição</th>',
              shot(12, 3, 'O rigor metodológico da análise: corpus, delineamento e códigos T, A e S',
                   'Fonte: elaborado pelo autor, com base em Bowen (2009), Gioia, Corley e Hamilton (2013) e Whetten (1989).',
                   'Fluxo em que o corpus principal (guias PMBOK, Agile Practice Guide e Scrum Guide) passa por análise documental qualitativa e é classificado em três códigos: T, predominância da prescrição; A, deslocamento para princípios; S, recomposição.')
              + '<div class="tablewrap"><table>\n<thead><tr><th>Proposição</th>', 1)
h = h.replace('<h2>Considerações finais</h2>\n',
              '<h2>Considerações finais</h2>\n'
              + shot(13, 12, 'Implicações práticas: da conformidade rígida à governança contextual', 'Fonte: elaborado pelo autor.',
                     'À esquerda, uma grade uniforme representando o isomorfismo engessado; à direita, um conjunto de formas diversas em um mesmo recipiente representando a governança contextual; abaixo, implicações para diretores de PMO, competências de liderança e o fim da oposição entre métodos.'), 1)
h = h.replace('</div>\n</section>\n\n<section class="sec">\n<h2>Referências</h2>',
              '</div>\n' + shot(14, 13, 'Conclusão: da prescrição à habilitação', 'Fonte: elaborado pelo autor.',
                               'Torre em estrutura de treliça que muda de azul-acinzentado na base para laranja e verde-azulado no topo, ao lado do texto de conclusão sobre a trajetória dialética do PMBOK.')
              + '</section>\n\n<section class="sec">\n<h2>Referências</h2>', 1)

h = h.replace('figure.fig{margin:22px 0 26px', 'figure.fig,figure.shot{margin:22px 0 26px')
h = h.replace('figcaption.cap{', 'figure.shot img{display:block;width:100%;height:auto;border-radius:8px}\nfigure.shot>a{display:block;overflow:hidden;border-radius:8px}\nfigcaption.cap{', 1)
h = h.replace('</style>\n</head>', '</style>\n<link rel="stylesheet" href="../assets/anim.css">\n<script>document.documentElement.classList.add("js")</script>\n</head>', 1)
h = h.replace('</script>\n<noscript>', '</script>\n<script src="../assets/anim.js"></script>\n<noscript>', 1)
h = h.replace('@media print{.nav,.replay,.btn{display:none}', '@media print{.nav,.replay,.btn{display:none}.js .reveal{opacity:1!important;transform:none!important}', 1)
open(F, 'w', encoding='utf8').write(h)
print('figuras com imagem:', h.count('class="shot'), '| figuras SVG restantes:', h.count('<figure class="fig"'))
