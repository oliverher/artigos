import re, shutil, html

S = 'docs'
SLUG = 'passaporte-pessoa-idosa'

CHEV = ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down mt-0.5 h-5 w-5 shrink-0 '
        'text-muted-foreground transition-transform duration-300" aria-hidden="true"><path d="m6 9 6 6 6-6"></path></svg>')
BOOK = re.search(r'<svg[^>]*lucide-book-open.*?</svg>',
                 open(S + '/proposito-de-vida/index.html', encoding='utf8').read(), re.S).group(0)

e = html.escape


def acc(title, paras, quote=None):
    body = ''.join('<p class="text-[15px] leading-relaxed text-muted-foreground">%s</p>' % e(p, quote=False) for p in paras)
    if quote:
        body += ('<p class="rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] italic leading-relaxed '
                 'text-accent-foreground">%s</p>' % e(quote, quote=False))
    return ('<div class="overflow-hidden rounded-xl border bg-card transition-shadow shadow-[var(--shadow-soft)]">'
            '<button type="button" aria-expanded="false" class="flex w-full items-start gap-4 px-5 py-4 text-left transition-colors '
            'hover:bg-secondary/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">'
            '<span class="mt-1 h-2 w-2 shrink-0 rounded-full transition-colors bg-sage"></span>'
            '<span class="flex-1 font-medium leading-snug text-foreground">%s</span>%s</button>'
            '<div class="grid transition-all duration-300 ease-out grid-rows-[0fr] opacity-0"><div class="overflow-hidden">'
            '<div class="space-y-4 border-t border-border/70 px-5 py-5 pl-11">%s</div></div></div></div>') % (e(title, quote=False), CHEV, body)


def fig(img, alt, cap, fit=False):
    style = ' style="object-fit:contain;background:#fff"' if fit else ''
    return ('<figure class="mt-6 overflow-hidden rounded-xl border bg-card shadow-[var(--shadow-soft)]">'
            '<a href="../assets/img/%s" target="_blank" rel="noopener" title="Abrir a imagem em tamanho original">'
            '<img src="../assets/img/%s" alt="%s" loading="lazy" class="aspect-video w-full object-cover"%s/></a>'
            '<figcaption class="border-t px-5 py-4 text-sm leading-relaxed text-muted-foreground">%s'
            '<span class="mt-1 block text-xs text-muted-foreground/80">%s</span></figcaption></figure>'
            % (img, img, e(alt), style, e(cap[0], quote=False), e(cap[1], quote=False)))


def section(num, sid, title, sub, figs, accs):
    return ('<section id="%s" aria-labelledby="%s-titulo"><div class="flex items-baseline gap-4">'
            '<span class="font-display text-3xl text-ochre">%s</span><div><h2 id="%s-titulo" class="text-2xl font-semibold">%s</h2>'
            '<p class="mt-1 text-sm text-muted-foreground">%s</p></div></div>%s<div class="mt-6 space-y-3">%s</div></section>'
            % (sid, sid, num, sid, e(title, quote=False), e(sub, quote=False), ''.join(figs), ''.join(accs)))


FONTE_SLIDE = 'Figura extraída da apresentação do artigo.'

sections = [
    section('01', 'jornada', 'A Jornada de Transformação e o serviço em foco',
            'Uma metodologia de Design Thinking e Design de Serviços aplicada a um benefício voltado a pessoas com 60 anos ou mais.',
            [fig('passaporte-jornada.png', 'Jornada de Transformação dos Serviços Públicos do TransformaLAB, com 24 etapas em sete fases: definição e pré-requisitos, ponto de partida, jornada do usuário, transformação de processos, digitalização, testes e capacitação e disponibilização.',
                 ('As 24 etapas da Jornada de Transformação, organizadas em sete fases, da identificação do serviço à sua disponibilização nos canais digitais.', 'TransformaLAB | Jornada de Transformação dos Serviços Públicos. Clique na imagem para ampliar.'), fit=True)],
            [acc('O que é a Jornada de Transformação',
                 ['Metodologia desenvolvida pela Superintendência Central de Transformação Pública (SCTP) da Secretaria de Estado da Administração de Goiás (Sead), com apoio do TransformaLAB.',
                  'Ela combina Design Thinking e Design de Serviços e foi aplicada ao redesenho do serviço Emitir Passaporte da Pessoa Idosa. É esse percurso, e não uma tecnologia isolada, o artefato investigado no estudo.'],
                 'Digitalizar processos não basta para gerar valor público quando o público-alvo enfrenta barreiras de letramento digital.'),
             acc('O serviço analisado: Passaporte da Pessoa Idosa',
                 ['Instituído pela Lei estadual nº 14.765/2004, o passaporte garante gratuidade no transporte intermunicipal a pessoas com 60 anos ou mais, residentes em Goiás, com renda familiar mensal de até três salários mínimos.',
                  'A investigação ocorreu de 3 a 10 de junho de 2024, durante a Jornada de Transformação conduzida pelo TransformaLAB/Sead.'],
                 'Um público com letramento digital heterogêneo é um bom teste: a tecnologia deve se adaptar ao humano, e não o inverso.')]),

    section('02', 'fundamentos', 'Do valor público ao Duplo Diamante',
            'O referencial que sustenta o redesenho: transformação digital, design e inclusão.',
            [fig('passaporte-duplo-diamante.jpg', 'Modelo do Duplo Diamante: descobrir e definir, no espaço do problema; desenvolver e entregar, no espaço da solução.',
                 ('O Duplo Diamante alterna pensamento divergente e convergente: primeiro entender o problema (descobrir e definir), depois construir a solução (desenvolver e entregar).', FONTE_SLIDE))],
            [acc('Transformação digital não é só digitalizar',
                 ['A literatura associa a transformação digital no setor público a mudanças na cultura organizacional, nos modelos de operação e na relação entre Estado e cidadão, e a orienta pela geração de valor público.',
                  'Brito (2025) critica índices de governo digital que privilegiam métricas quantitativas, como o número de serviços digitalizados, em detrimento de inclusão, equidade e participação cidadã.'],
                 'Contar serviços online mede o que foi digitalizado, não quem conseguiu usá-los.'),
             acc('Design Thinking e Design de Serviços',
                 ['O Design Thinking trabalha com ciclos iterativos de empatia, ideação, prototipação e teste. O Design de Serviços coordena processos, pontos de contato, atores e experiências ao longo da jornada do usuário.',
                  'Combinadas, as duas abordagens permitem explorar o problema com amplitude antes de convergir para soluções viáveis.']),
             acc('Inclusão digital de pessoas idosas',
                 ['Para pessoas idosas, o acesso digital pede desenho acessível, suporte assistido e manutenção de canais presenciais e telefônicos, de modo a evitar exclusões forçadas e favorecer a autonomia progressiva.',
                  'Estudos citados no artigo apontam barreiras como complexidade da navegação, terminologia inadequada e falta de suporte humano.'],
                 'Estratégias multicanal só produzem inclusão quando consideram perfis diversos de letramento digital.')]),

    section('03', 'metodo', 'Pesquisa e empatia: dando rosto aos dados',
            'Design Science Research, cinco fontes de dados e uma persona construída a partir do campo.',
            [fig('passaporte-pesquisa-empatia.jpg', 'Perfil dos 126 idosos pesquisados por gênero e idade, com a persona Maria Aparecida e os artefatos mapa de atores, matriz CSD e mapa de empatia.',
                 ('A amostra e a persona Maria Aparecida, 68 anos, sintetizam os pontos de dor e orientaram a cocriação.', FONTE_SLIDE))],
            [acc('Design Science Research',
                 ['A pesquisa adota a Design Science Research (DSR), de Hevner et al. (2004), adaptada a políticas públicas por Drechsler e Hevner (2022): construir e avaliar artefatos para resolver problemas organizacionais relevantes.',
                  'O processo teve três fases: identificação do problema, desenvolvimento do artefato (metodologia e protótipos) e avaliação com usuários e indicadores.']),
             acc('Cinco fontes de dados, triangulação',
                 ['Entrevistas semiestruturadas com 126 usuários do serviço com 60 anos ou mais, 7 representantes da área de negócio e 5 membros do TransformaLAB; oficinas de cocriação intersetoriais; observação participante de 12 reuniões de imersão e 5 reuniões de trabalho; análise documental; e artefatos de design.',
                  'Os artefatos incluem mapa de empatia, mapa de atores, persona, matriz CSD (Certezas, Suposições e Dúvidas) e o mapeamento das jornadas AS IS e TO BE.']),
             acc('Quem foi ouvido',
                 ['Dos 126 participantes, 60 eram mulheres (47,6%), 55 eram homens (43,7%) e 1 preferiu não informar o gênero (0,8%). Quanto à idade, 96 (76,2%) tinham entre 60 e 69 anos e 20 (15,9%) tinham mais de 69. Predominaram pessoas de baixa renda, em linha com o critério de elegibilidade do programa.',
                  'Em cada uma dessas duas variáveis, as categorias somam 116 dos 126 participantes (92,1%). Os 10 restantes (7,9%) não aparecem nas categorias apresentadas no artigo.',
                  'A persona Maria Aparecida, 68 anos, aposentada, valoriza a autonomia, mas enfrenta barreiras tecnológicas e busca um serviço menos burocrático.']),
             acc('Cuidados éticos',
                 ['A pesquisa seguiu a Resolução nº 510/2016 do Conselho Nacional de Saúde. Os participantes assinaram o Termo de Consentimento Livre e Esclarecido, escrito em linguagem acessível e com opção de consentimento verbal gravado em áudio para quem tinha dificuldade de leitura.',
                  'O anonimato foi preservado e os dados pessoais foram tratados conforme a Lei Geral de Proteção de Dados.'])]),

    section('04', 'as-is', 'Diagnóstico AS IS: o labirinto burocrático',
            'Um processo fragmentado, com seis categorias de pontos de dor.',
            [fig('passaporte-as-is-labirinto.jpg', 'Diagnóstico da jornada atual: descoberta difusa, solicitação presencial, caça aos papéis, caixa preta de até 60 dias e retirada presencial.',
                 ('Da informação dispersa à retirada do papel: cada etapa exigia deslocamento, documentos e espera.', FONTE_SLIDE))],
            [acc('Informação dispersa e documentos difíceis de reunir',
                 ['As informações sobre o benefício eram obtidas na rodoviária, com conhecidos, no CRAS ou no Vapt Vupt, o que gerava incerteza sobre o direito e sobre os procedimentos.',
                  'Os idosos tinham dificuldade para identificar e obter os documentos, em especial o comprovante de renda familiar (extrato do INSS e espelho do CadÚnico), o que levava a idas a lan houses e a cópias desnecessárias.'],
                 'O Estado exigia que o cidadão atuasse como mensageiro entre órgãos que não se comunicavam.'),
             acc('Deslocamentos, espera e falta de acompanhamento',
                 ['A solicitação exigia ir a um posto de atendimento (SEDS, Vapt Vupt ou CRAS), com risco de documentação incompleta e de necessidade de retorno.',
                  'A validação levava até 60 dias no interior, e não era possível consultar a situação do pedido, o que gerava ansiedade e incerteza.']),
             acc('Até agendar a viagem era um obstáculo',
                 ['Marcar a viagem exigia comparecer pessoalmente à rodoviária com antecedência, sem garantia de vaga.'])]),

    section('05', 'to-be', 'Redesenho TO BE: interoperabilidade e multicanalidade',
            'As soluções cocriadas em oficinas intersetoriais com SEDS, Vapt Vupt, CRAS, AGR e empresas de transporte.',
            [fig('passaporte-interoperabilidade.jpg', 'Interoperabilidade nos bastidores: o portal EXPRESSO e o WhatsApp na superfície, conectados às bases da SEDS, do INSS, do CadÚnico e da AGR.',
                 ('Na superfície, o cidadão usa WhatsApp ou o EXPRESSO; nos bastidores, as bases de dados conversam entre si.', FONTE_SLIDE)),
             fig('passaporte-multicanalidade.jpg', 'Multicanalidade: portal EXPRESSO, mensageria por WhatsApp com áudio e canal físico no CRAS e no Vapt Vupt.',
                 ('Três canais convivem: portal EXPRESSO, WhatsApp com suporte de áudio e atendimento presencial.', FONTE_SLIDE))],
            [acc('Comunicação proativa e multicanalidade inclusiva',
                 ['Ao completarem 60 anos, os idosos passam a receber mensagens por WhatsApp com informações sobre o benefício e orientações sobre o CadÚnico.',
                  'A solicitação pode ser feita pelo portal EXPRESSO, por WhatsApp (com suporte de áudio para pessoas com baixa literacia digital) ou presencialmente.'],
                 'Manter o atendimento presencial não atrasa a transformação digital: é condição para sua legitimidade.'),
             acc('Interoperabilidade como redutora de burocracia',
                 ['A integração com as bases do CadÚnico e do INSS permite a validação automática de elegibilidade e dispensa a apresentação manual de documentos. A integração inclui ainda os sistemas da Agência Goiana de Regulação (AGR).'],
                 'Não pedir ao cidadão o que o Estado já sabe.'),
             acc('Transparência, acompanhamento e protótipo navegável',
                 ['O cidadão pode consultar on-line a situação da solicitação, visualizar o passaporte emitido e ver o histórico de viagens.',
                  'O protótipo navegável representa todos os percursos possíveis: usuários com e sem CadÚnico, beneficiários e não beneficiários do INSS, preferência por passaporte digital ou físico.'])]),

    section('06', 'resultados', 'Resultados: do labirinto à linha expressa',
            'O que mudou entre a jornada AS IS e a jornada TO BE.',
            [fig('passaporte-matriz-as-is-to-be.jpg', 'Matriz de transformação estrutural comparando a situação atual (AS IS) e a desejada (TO BE) em informação, documentos, canais, prazo e retirada.',
                 ('Da informação difusa à comunicação proativa; do papel à validação automática; do presencial obrigatório ao multicanal.', FONTE_SLIDE)),
             fig('passaporte-impacto-operacional.jpg', 'Impacto operacional: tempo de emissão de 60 dias para 24 horas na emissão automática ou 5 dias úteis com análise.',
                 ('O tempo de emissão do passaporte digital passou de até 60 dias para até 24 horas (emissão automática) ou até 5 dias úteis (com análise).', FONTE_SLIDE))],
            [acc('Prazo de emissão',
                 ['O passaporte digital é emitido em até 24 horas na emissão automática, ou em até 5 dias úteis quando há análise documental. O passaporte físico fica disponível para retirada em até 30 dias.'],
                 'De até 60 dias para até 5 dias úteis no passaporte digital.'),
             acc('Canais, documentação e deslocamentos',
                 ['Antes, o serviço era apenas presencial, com documentação manual e várias cópias, sem acompanhamento e com comunicação reativa. Exigia de 3 a 5 deslocamentos.',
                  'Depois, oferece EXPRESSO, WhatsApp (com áudio) e atendimento presencial, com validação automática pelo CadÚnico e pelo INSS, consulta on-line em tempo real, comunicação proativa e de 0 a 1 deslocamento (presencial opcional).']),
             acc('Testes de usabilidade e validação',
                 ['A fase de Teste e Capacitação incluiu testes funcionais e de usabilidade com servidores e cidadãos, em situações simuladas de uso real, e o retorno foi usado para ajustar a solução.',
                  'A manutenção do atendimento presencial e o uso de mensagens em áudio foram adotados deliberadamente como estratégias de inclusão digital progressiva.'])]),
]

framework = ('<section aria-labelledby="framework" class="mt-16 rounded-2xl border bg-secondary/50 p-7">'
             '<h2 id="framework" class="text-2xl font-semibold">A síntese: inclusão digital progressiva</h2>'
             '<p class="mt-3 leading-relaxed text-muted-foreground">O artigo propõe que a transformação digital de serviços para populações vulneráveis não siga uma lógica binária, digital ou presencial, e sim um contínuo. O framework tem três dimensões complementares.</p>'
             '<div class="mt-6 space-y-5">'
             '<div><h3 class="text-lg font-semibold text-ochre">Multicanalidade adaptativa</h3><p class="mt-2 leading-relaxed text-muted-foreground">Canais digitais e presenciais oferecidos ao mesmo tempo, para o cidadão escolher o meio compatível com o seu letramento digital, sem migração forçada.</p></div>'
             '<div><h3 class="text-lg font-semibold text-ochre">Autonomia progressiva</h3><p class="mt-2 leading-relaxed text-muted-foreground">A comunicação proativa por WhatsApp, inclusive em áudio, funciona como um andaime digital: familiariza aos poucos o usuário idoso sem eliminar a opção presencial.</p></div>'
             '<div><h3 class="text-lg font-semibold text-ochre">Interoperabilidade como redutora de burocracia</h3><p class="mt-2 leading-relaxed text-muted-foreground">A validação automática entre CadÚnico e INSS dispensa o cidadão de comprovar ao Estado informações que o próprio Estado já possui.</p></div>'
             '</div>'
             '<p class="mt-6 rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] italic leading-relaxed text-accent-foreground">A tecnologia é o meio; o design orientado ao humano é o método; o valor público é o fim.</p>'
             '</section>')

limits = ('<section id="limites" aria-labelledby="limites-titulo" class="mt-14"><div class="flex items-baseline gap-4">'
          '<span class="font-display text-3xl text-ochre">07</span><div><h2 id="limites-titulo" class="text-2xl font-semibold">O que o estudo permite afirmar — e o que não permite</h2>'
          '<p class="mt-1 text-sm text-muted-foreground">Limitações declaradas pelos autores e agenda de pesquisa.</p></div></div>'
          '<div class="mt-6 space-y-3">'
          + acc('Um estudo exploratório', ['O estudo foca a jornada de obtenção do passaporte e não avalia a taxa de uso efetivo nas rodoviárias após a implementação. Isso exigiria desenhos longitudinais para verificar a sustentabilidade das melhorias.'],
                'Os resultados são indícios, e não prova de que o benefício passou a ser mais usado.')
          + acc('Amostra e viés', ['Os 126 participantes são adequados à abordagem qualitativa, mas não permitem generalização estatística para toda a população idosa de Goiás.',
                                     'A pesquisa foi conduzida por equipe vinculada ao TransformaLAB/Sead, o que pode ter introduzido viés de desejabilidade social nas respostas.'])
          + acc('Sem grupo de controle', ['Não houve grupo de idosos que não passou pela transformação, o que limita a atribuição das melhorias exclusivamente ao redesenho.',
                                          'Os resultados também são específicos do contexto institucional de Goiás e da legislação estadual vigente; transferi-los a outros estados ou países exige adaptação.'])
          + acc('Agenda de pesquisa', ['Avaliar o impacto longitudinal sobre a taxa de utilização do benefício; investigar a percepção de idosos com mais de 80 anos e com deficiências sensoriais; comparar a metodologia goiana com experiências internacionais (Reino Unido, Estônia e Coreia do Sul); e desenvolver indicadores de inclusão digital específicos para serviços governamentais.'])
          + '</div></section>')


def nav_html(pages, active):
    pill = 'shrink-0 rounded-full px-4 py-1.5 text-sm font-medium transition-colors '
    off = pill + 'text-muted-foreground hover:bg-secondary'
    on = pill + 'bg-primary text-primary-foreground'
    items = [('../', 'Início', 'home')] + [('../%s/' % s, l, s) for s, l in pages]
    links = ''.join('<a href="%s" class="%s"%s>%s</a>' % (h, on if k == active else off, ' aria-current="page"' if k == active else '', l) for h, l, k in items)
    return ('<nav class="sticky top-0 z-50 border-b border-border/60 bg-background/90 backdrop-blur">'
            '<div class="mx-auto flex max-w-3xl items-center gap-2 overflow-x-auto px-6 py-3">%s</div></nav>' % links)


def build(pages):
    stat = lambda n, l: '<div><dt class="font-display text-2xl text-ochre">%s</dt><dd class="mt-1 text-xs uppercase tracking-wide text-primary-foreground/70">%s</dd></div>' % (n, l)
    header = ('<header class="relative overflow-hidden text-primary-foreground" style="background-image:var(--gradient-deep)">'
              '<div class="surface-paper absolute inset-0 opacity-30" aria-hidden="true"></div>'
              '<div class="relative mx-auto max-w-3xl px-6 py-20 sm:py-28">'
              '<p class="text-xs font-semibold uppercase tracking-[0.2em] text-ochre">Design Science Research · Governo digital · Goiás</p>'
              '<h1 class="mt-6 text-4xl leading-[1.1] font-semibold sm:text-5xl">Transformação digital e design de serviços no <span class="text-gradient-warm">setor público</span></h1>'
              '<p class="mt-5 text-lg leading-relaxed text-primary-foreground/80">Lições do redesenho do Passaporte da Pessoa Idosa em Goiás: multicanalidade, interoperabilidade e comunicação proativa.</p>'
              '<p class="mt-8 text-sm text-primary-foreground/70">Carlos Hernane de Oliveira · Cristiane Rachel de Paiva Felipe</p>'
              '<div class="mt-6"><a href="../assets/pdf/Passaporte_da_Pessoa_Idosa.pdf" target="_blank" rel="noopener noreferrer" '
              'class="inline-flex items-center gap-2 rounded-full bg-ochre px-6 py-3 text-sm font-semibold text-ochre-foreground shadow-lift transition-transform hover:-translate-y-0.5">'
              + BOOK + 'Leia o Artigo na Íntegra</a>'
              '<p class="mt-3 max-w-md text-sm leading-relaxed text-primary-foreground/70">Abre o PDF completo do artigo em uma nova aba, para leitura direta no navegador.</p></div>'
              '<dl class="mt-10 grid grid-cols-2 gap-6 sm:grid-cols-4">'
              + stat('126', 'pessoas idosas ouvidas') + stat('60 → 5', 'dias até a emissão digital') + stat('24 h', 'na emissão automática') + stat('3', 'canais de acesso')
              + '</dl></div></header>')
    intro = ('<section aria-labelledby="resumo-pi"><h2 id="resumo-pi" class="text-2xl font-semibold">Do que trata o artigo</h2>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">O estudo analisa como a Jornada de Transformação de Serviços Públicos, baseada em Design Thinking e Design de Serviços, foi aplicada ao redesenho do serviço de emissão do Passaporte da Pessoa Idosa em Goiás, com atenção a pessoas idosas de baixa literacia digital.</p>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">A leitura mostra que digitalizar não basta: o ganho de prazo veio junto com canais que respeitam níveis diferentes de letramento digital e com bases de dados que conversam entre si.</p></section>'
             '<section aria-labelledby="objetivos-pi" class="mt-10 rounded-2xl border bg-secondary/50 p-7"><h2 id="objetivos-pi" class="text-2xl font-semibold">Pergunta e contribuições</h2>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Pergunta de pesquisa</h3><p class="mt-2 leading-relaxed text-muted-foreground">De que modo a combinação de princípios de Design de Serviços, multicanalidade inclusiva e interoperabilidade de dados pode reduzir barreiras de acesso e melhorar a experiência de pessoas idosas no uso de serviços públicos digitais?</p></div>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Três contribuições</h3><ul class="mt-3 space-y-2 text-muted-foreground">'
             + ''.join('<li class="flex gap-3"><span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-sage"></span><span class="leading-relaxed">%s</span></li>' % t for t in [
                 'Um framework analítico que relaciona inclusão digital progressiva, design inclusivo e interoperabilidade governamental.',
                 'Evidências empíricas da aplicação da Design Science Research em governo digital estadual no Brasil.',
                 'Implicações para políticas públicas alinhadas aos ODS 10 (Redução das Desigualdades) e 16 (Paz, Justiça e Instituições Eficazes).'])
             + '</ul></div></section>')
    main = '<main class="mx-auto max-w-3xl px-6 py-16">' + intro + '<div class="mt-14 space-y-14">' + ''.join(sections) + '</div>' + framework + limits + '</main>'
    footer = ('<footer class="border-t bg-card"><div class="mx-auto max-w-3xl px-6 py-10 text-sm text-muted-foreground">'
              '<p class="font-display text-base text-foreground">Transformação digital e design de serviços no setor público: lições do redesenho do Passaporte da Pessoa Idosa em Goiás</p>'
              '<p class="mt-2">Carlos Hernane de Oliveira · Cristiane Rachel de Paiva Felipe. Escola de Governo do Estado de Goiás.</p>'
              '<p class="mt-4">Palavras-chave: transformação digital; design de serviços; governo digital; inclusão digital; pessoa idosa; Design Science Research.</p></div></footer>')
    page = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>'
            '<title>Passaporte da Pessoa Idosa: transformação digital e design de serviços</title>'
            '<meta name="description" content="Artigo sobre o redesenho do Passaporte da Pessoa Idosa em Goiás com Design de Serviços: tópicos, resultados e limites do estudo."/>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap"/>'
            '<link rel="stylesheet" href="../assets/styles.css"/></head><body>'
            + nav_html(pages, SLUG) + '<div class="min-h-screen">' + header + main + footer + '</div>'
            '<script src="../assets/app.js"></script></body></html>')
    import os
    os.makedirs('%s/%s' % (S, SLUG), exist_ok=True)
    open('%s/%s/index.html' % (S, SLUG), 'w', encoding='utf8').write(page)


def patch_nav_and_assets(pages_other):
    new = ('<a href="../%s/" class="shrink-0 rounded-full px-4 py-1.5 text-sm font-medium transition-colors text-muted-foreground hover:bg-secondary">Pessoa idosa</a>' % SLUG)
    for slug in pages_other:
        f = '%s/%s/index.html' % (S, slug)
        h = open(f, encoding='utf8').read()
        if SLUG not in h:
            h = h.replace('BPM em PMEs</a>', 'BPM em PMEs</a>' + new, 1)
            open(f, 'w', encoding='utf8').write(h)
    shutil.copy('src/orig/Passaporte_da_Pessoa_Idosa.pdf', S + '/assets/pdf/Passaporte_da_Pessoa_Idosa.pdf')
