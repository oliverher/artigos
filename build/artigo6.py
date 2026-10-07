"""Artigo 06: Framework de maturidade digital para o setor público goiano (MMDI-GO).

Gera docs/mmdi-go/index.html a partir do texto do artigo e dos 15 slides da apresentação
(src/orig/mmdi-go/img). As imagens ganham a galeria animada de build/mmdi.css e build/mmdi.js.
"""
import json, os, shutil, sys
sys.path.insert(0, 'build')
import shell
import artigo4
from artigo4 import acc, e, BOOK

S = 'docs'
SLUG = 'mmdi-go'
SRC = 'src/orig/mmdi-go'
PDF = 'MMDI-GO_artigo_ABNT.pdf'


def gfig(n, title, alt, tour, cap=None):
    """Imagem animada: slide n da apresentação, com roteiro de regiões em destaque (x, y, largura, altura em %, texto)."""
    img = 'mmdi-slide-%02d.jpg' % n
    return ('<figure class="gfig mt-6 overflow-hidden rounded-xl border bg-card shadow-[var(--shadow-soft)]" data-tour=\'%s\'>'
            '<div class="gfig-stage"><div class="gfig-zoom">'
            '<img class="gfig-img" src="../assets/img/%s" width="1376" height="768" loading="lazy" alt="%s"/>'
            '<div class="gfig-fx" aria-hidden="true"><i class="gfig-sweep"></i><i class="gfig-scan"></i><i class="gfig-glare"></i><i class="gfig-wipe"></i></div>'
            '<div class="gfig-spot" aria-hidden="true"></div></div></div>'
            '<div class="gfig-bar"></div>'
            '<figcaption class="border-t px-5 py-4 text-sm leading-relaxed text-muted-foreground">%s'
            '<span class="mt-1 block text-xs text-muted-foreground/80">Slide %d da apresentação do artigo. '
            '<a class="underline underline-offset-2" href="../assets/img/%s" target="_blank" rel="noopener">Ver a imagem original</a></span></figcaption></figure>'
            % (e(json.dumps(tour, ensure_ascii=False), quote=True).replace('&#x27;', '&#39;'), img, e(alt), e(title, quote=False), n, img))


def section(num, sid, title, sub, blocks, accs):
    return ('<section id="%s" aria-labelledby="%s-titulo"><div class="flex items-baseline gap-4">'
            '<span class="font-display text-3xl text-ochre">%s</span><div><h2 id="%s-titulo" class="text-2xl font-semibold">%s</h2>'
            '<p class="mt-1 text-sm text-muted-foreground">%s</p></div></div>%s<div class="mt-6 space-y-3">%s</div></section>'
            % (sid, sid, num, sid, e(title, quote=False), e(sub, quote=False), ''.join(blocks), ''.join(accs)))


# ---------- gráficos em HTML ----------
DIMS = [('Liderança e Estratégia Digital', 25, '#137d5c'), ('Dados e Interoperabilidade', 20, '#276fa0'),
        ('Processos e Serviços (CVI)', 20, '#cf7638'), ('Cultura e Competências', 15, '#7a4fa3'),
        ('Experiência do Cidadão', 12, '#a8483a'), ('Infraestrutura e Tecnologia', 8, '#5a6b7a')]
weights = ('<div class="wchart reveal rounded-xl border bg-card p-5 shadow-[var(--shadow-soft)] mt-6" role="group" aria-label="Pesos iniciais das seis dimensões">'
           '<p class="text-sm font-medium">Pesos iniciais das dimensões no índice global</p>'
           '<p class="mt-1 text-xs text-muted-foreground">Propostos pelo autor e sujeitos à calibração por especialistas (método Delphi).</p><div class="wchart-rows" style="display:grid;gap:12px;margin-top:18px">'
           + ''.join('<div class="wrow"><b>%s</b><span class="wtrack"><i style="--w:%.1f%%;--c:%s;--d:%.2fs"></i></span>'
                     '<span class="wval" data-count data-from="0" data-to="%d" data-suffix="%%" data-delay="%d">%d%%</span></div>'
                     % (e(n), v * 3.6, c, .15 * i, v, 150 * i, v) for i, (n, v, c) in enumerate(DIMS))
           + '</div><p class="mt-4 text-sm text-muted-foreground">A soma dos pesos é de 100%. O índice global é a média das dimensões ponderada por esses pesos.</p></div>')

LEVELS = [('Nível 1', 'Inicial', 'Processos ad hoc, baixa digitalização e dependência de iniciativas individuais.', '#5a6b7a', 120),
          ('Nível 2', 'Fragmentado', 'Algumas áreas digitalizadas, sem integração e com processos ainda analógicos.', '#276fa0', 150),
          ('Nível 3', 'Definido', 'Estratégia digital formalizada, processos mapeados na CVI e serviços essenciais online.', '#137d5c', 180),
          ('Nível 4', 'Gerenciado', 'Uso intensivo de dados para gestão, alta interoperabilidade e foco na experiência do usuário.', '#cf7638', 210),
          ('Nível 5', 'Otimizado', 'Transformação digital plena, cultura de inovação contínua e serviços proativos e orientados a dados, quando pertinentes ao órgão.', '#b8860b', 250)]
levels = ('<div class="lvls reveal mt-6" role="list" aria-label="Os cinco níveis de maturidade">'
          + ''.join('<div class="lvl" role="listitem" style="--h:%dpx;--c:%s;--d:%.2fs"><b>%s · %s</b>%s</div>'
                    % (h, c, .12 * i, n, e(t), e(d)) for i, (n, t, d, c, h) in enumerate(LEVELS))
          + '</div>')

EX = [('Liderança e Estratégia Digital', '3,0', '0,25', '0,75'), ('Dados e Interoperabilidade', '2,0', '0,20', '0,40'),
      ('Processos e Serviços (CVI)', '3,0', '0,20', '0,60'), ('Cultura e Competências', '2,0', '0,15', '0,30'),
      ('Experiência do Cidadão', '2,0', '0,12', '0,24'), ('Infraestrutura e Tecnologia', '4,0', '0,08', '0,32')]
_td = 'padding:8px 10px;border-top:1px solid var(--border)'
_th = 'padding:8px 10px;font-weight:500'
example = ('<div class="reveal mt-6 rounded-xl border bg-card p-5 shadow-[var(--shadow-soft)]" role="group" aria-label="Exemplo ilustrativo de cálculo do índice global">'
           '<p class="text-sm font-medium">Exemplo ilustrativo de cálculo do índice global</p>'
           '<p class="mt-1 text-xs text-muted-foreground">Dados fictícios, de um órgão hipotético, apenas para mostrar a conta.</p>'
           '<div style="overflow-x:auto;margin-top:14px"><table class="text-sm" style="width:100%%;border-collapse:collapse;min-width:420px">'
           '<thead><tr class="text-xs text-muted-foreground" style="text-align:right"><th style="%s;text-align:left">Dimensão</th>'
           '<th style="%s">Pontuação (1 a 5)</th><th style="%s">Peso</th><th style="%s">Contribuição</th></tr></thead><tbody>' % ((_th,) * 4)
           + ''.join('<tr style="text-align:right"><td style="%s;text-align:left">%s</td><td style="%s">%s</td><td style="%s">%s</td><td style="%s">%s</td></tr>'
                     % (_td, e(n), _td, p, _td, w, _td, c) for n, p, w, c in EX)
           + ('<tr style="text-align:right;font-weight:600"><td style="%s;text-align:left">Índice global informativo (média ponderada)</td><td style="%s"></td><td style="%s">1,00</td><td style="%s">2,61</td></tr>'
              '<tr style="text-align:right"><td style="%s;text-align:left">Média simples (pesos iguais)</td><td style="%s"></td><td style="%s"></td><td style="%s">2,67</td></tr>'
              '<tr style="text-align:right"><td style="%s;text-align:left">Menor pontuação por dimensão (regra preliminar de limitação do nível)</td><td style="%s">2,0</td><td style="%s"></td><td style="%s"></td></tr>'
              % ((_td,) * 12))
           + '</tbody></table></div></div>')

# ---------- figuras ----------
F1 = gfig(2, 'A lacuna subnacional: entre os instrumentos examinados, nenhum combina visão do órgão, cadeia de valor pública e esfera estadual.',
          'Tabela comparando NMDSP, MMD, ITDBr e MMDI-GO em unidade de análise, escopo temático, ancoragem na cadeia de valor e consideração de barreiras culturais; só o MMDI-GO é estadual, holístico e ancorado na cadeia de valor.',
          [[7.5, 44, 85, 24, 'Unidade de análise e escopo: serviço, órgão federal, empresa ou, no MMDI-GO, o órgão público estadual com seis dimensões.'],
           [7.5, 68, 85, 11, 'Ancoragem na cadeia de valor: NMDSP, MMD e ITDBr não têm; o MMDI-GO se apoia na CVI de Goiás.'],
           [7.5, 79, 85, 12, 'Barreiras culturais: ausentes no NMDSP, parciais no MMD, presentes no ITDBr e numa dimensão dedicada no MMDI-GO.'],
           [75, 34, 18, 57, 'A coluna do MMDI-GO: desenhado para a esfera estadual, entre os instrumentos comparados, e ainda sem validação empírica. O quadro é um mapeamento descritivo de escopo, e não prova de superioridade.']])

F2 = gfig(3, 'Uma ponte entre a teoria acadêmica e a prática da gestão pública.',
          'Ponte luminosa ligando a teoria acadêmica à prática da gestão pública, com o MMDI-GO ao centro e, abaixo, três blocos: Design Science Research, fatores críticos e barreiras, e neutralidade tecnológica.',
          [[40, 33, 20, 24, 'O MMDI-GO ao centro: mais que medir o quanto o órgão é digital, é um método de diagnóstico para decidir.'],
           [8, 40, 15, 11, 'De um lado, a teoria acadêmica: modelos de maturidade, valor público e capacidades dinâmicas.'],
           [78, 40, 17, 11, 'Do outro, a prática da gestão pública goiana, organizada pela Cadeia de Valor Integrada.'],
           [4.5, 70, 28.5, 25, 'Design Science Research: criar artefatos que resolvem problemas práticos das organizações.'],
           [35.5, 70, 28.5, 25, 'Fatores críticos e barreiras: variáveis estruturais como a resistência cultural e a restrição orçamentária.'],
           [66.5, 70, 28.5, 25, 'Neutralidade tecnológica: mede a capacidade institucional, e não a adoção de uma tecnologia específica.']])

F3 = gfig(4, 'A digitalização ancorada na Cadeia de Valor Integrada: três camadas interdependentes, lidas de baixo para cima.',
          'Pirâmide de camadas com circuitos e uma seta verde apontando para cima até o rótulo Valor Público e Cidadão; ao lado, os processos finalísticos, gerenciais e de suporte.',
          [[70, 74, 29, 14, 'Base: os processos de suporte, a espinha dorsal de infraestrutura e de recursos humanos.'],
           [70, 60, 28, 13, 'Meio: os processos gerenciais, que medem, monitoram e controlam as metas institucionais.'],
           [63, 45, 31, 13, 'Topo operacional: os processos finalísticos, que entregam valor direto ao cidadão, como saúde, educação e segurança.'],
           [38, 30, 25, 16, 'No alto, o valor público e o cidadão: é para lá que a seta aponta.']])

F4 = gfig(5, 'Por que a retaguarda define a experiência da ponta.',
          'Comparação entre FALHA, uma interface digital sobre pernas de madeira rachadas com um aviso de erro no sistema, e SUCESSO, uma torre sólida ligada por circuitos.',
          [[11, 30, 32, 64, 'Falha: um serviço digital moderno apoiado numa retaguarda analógica e frágil entra em colapso.'],
           [50, 30, 44, 64, 'Sucesso: a modernização da ponta amparada por uma retaguarda digital e integrada.'],
           [33, 78, 35, 19, 'A integração entre as camadas evita que o serviço ao cidadão seja freado por processos de suporte ineficientes.']])

F5 = gfig(6, 'As seis dimensões estruturais da maturidade digital e seus pesos iniciais.',
          'Gráfico de radar de seis eixos com as dimensões do MMDI-GO e seus pesos: Liderança 25%, Dados 20%, Processos 20%, Cultura 15%, Experiência do Cidadão 12% e Infraestrutura 8%.',
          [[20, 36, 24, 10, 'Liderança e Estratégia Digital, 25%: o maior peso, por ser o principal fator crítico de sucesso.'],
           [58, 37, 22, 8, 'Dados e Interoperabilidade, 20%: integrar bases é a transição para um governo inteligente.'],
           [57, 58, 24, 9, 'Processos e Serviços, 20%: digitalização e reengenharia dos processos da CVI.'],
           [58, 80, 16, 12, 'Cultura e Competências, 15%: a resistência cultural e o déficit de competências são barreiras recorrentes.'],
           [36, 80, 13, 10, 'Experiência do Cidadão, 12%: o indicador de resultado, medido na jornada do serviço.'],
           [27, 58, 16, 9, 'Infraestrutura e Tecnologia, 8%: condição necessária, mas não suficiente.'],
           [5, 79, 30, 15, 'Leitura do conjunto: a tecnologia dá o piso e a liderança dita a sustentabilidade da transformação.']])

F6 = gfig(7, 'Liderança forte e cultura receptiva.',
          'Dois painéis: Liderança e Estratégia Digital (25%), com um timão, e Cultura e Competências (15%), com um cérebro conectado a pessoas, cada um com o que mede e a justificativa.',
          [[6, 23, 41, 28, 'O timão: liderança e estratégia digital, com 25% do índice.'],
           [6, 52, 41, 38, 'Mede o engajamento da alta gestão e o alinhamento ao plano de transformação. Sem capital político, as iniciativas se fragmentam.'],
           [53, 23, 41, 28, 'Cultura e competências, 15% do índice: pessoas conectadas em torno do conhecimento.'],
           [53, 52, 41, 38, 'Mede a alfabetização digital, a abertura à inovação e a gestão da mudança, onde as barreiras são mais agudas.']])

F7 = gfig(8, 'Processos, serviços e infraestrutura: a operação interna.',
          'Dois painéis: Processos e Serviços com foco na CVI (20%), com fluxogramas e engrenagens, e Infraestrutura e Tecnologia (8%), com servidores, nuvem e escudo.',
          [[5, 24, 43, 34, 'Processos e Serviços (foco na CVI), 20%: reengenharia e digitalização de ponta a ponta.'],
           [5, 59, 43, 27, 'Justificativa: transforma o modelo de negócio do Estado, trocando estruturas rígidas por fluxos eficientes e desburocratizados.'],
           [52, 24, 43, 34, 'Infraestrutura e Tecnologia, 8%: conectividade, nuvem, segurança e sistemas estruturadores.'],
           [52, 59, 43, 27, 'Peso menor, sob o pressuposto de que Goiás já tem infraestrutura relativamente consolidada, ainda a ser testado.']])

F8 = gfig(9, 'Decisões inteligentes e foco absoluto na jornada do cidadão.',
          'Dois painéis: Dados e Interoperabilidade (20%), com um núcleo de dados em órbita, e Experiência do Cidadão (12%), com uma figura humana cercada de canais.',
          [[16, 16, 33, 35, 'Dados e Interoperabilidade, 20%: um núcleo de dados que conecta as bases do Estado.'],
           [16, 52, 33, 40, 'Mede a integração de bases e o uso de análise de dados. É o motor da passagem do governo apenas digital ao inteligente e preditivo.'],
           [51.5, 16, 33, 35, 'Experiência do Cidadão, 12%: o cidadão no centro de uma jornada multicanal.'],
           [51.5, 52, 33, 40, 'Mede multicanalidade, acessibilidade e satisfação. É o indicador final de resultado, a servicização do Estado.']])

F9 = gfig(10, 'A escada evolutiva da capacidade institucional.',
          'Escada luminosa de cinco degraus ascendentes, do Nível 1 Inicial ao Nível 5 Otimizado, cada um com sua descrição.',
          [[12.5, 67, 18.5, 13, 'Nível 1, Inicial: processos ad hoc, baixa digitalização e isolamento.'],
           [26, 55, 19.5, 13, 'Nível 2, Fragmentado: áreas digitalizadas em silos, sem integração sistêmica.'],
           [40.5, 40, 17, 15.5, 'Nível 3, Definido: estratégia formalizada, processos mapeados na CVI e serviços online.'],
           [57, 28, 17.5, 18.5, 'Nível 4, Gerenciado: uso intensivo de dados, alta interoperabilidade e foco no usuário.'],
           [74.5, 18, 17.5, 15, 'Nível 5, Otimizado: cultura de inovação contínua e serviços proativos e preditivos, quando pertinentes.']])

F10 = gfig(11, 'O motor do diagnóstico: 18 indicadores estratégicos.',
           'Tablet com três exemplos de itens do questionário, cada um com um controle deslizante de 1 a 5, e um destaque sobre a parcimônia de três itens por dimensão.',
           [[4, 17, 86, 11, 'Instrumento preliminar de fácil aplicação, em escala Likert de 1 a 5, com formulações graduais para não penalizar órgãos.'],
            [25, 29, 54, 58, 'Três exemplos: liderança, processos e cidadão. Cada afirmativa é respondida de 1, não existe, a 5, plenamente implementado.'],
            [53, 84, 44, 12, 'Parcimônia: três itens por dimensão permitem respostas rápidas sem comprometer a rotina do órgão.']])

F11 = gfig(12, 'Transformação como processo contínuo e cíclico: as seis fases de aplicação.',
           'Seis anéis encadeados: Sensibilização, Mapeamento, Coleta, Diagnóstico, Plano de Ação e Monitoramento.',
           [[4.4, 38, 16, 40, 'Fase 1, Sensibilização: apresentar os objetivos à alta liderança e buscar o comprometimento institucional.'],
            [19.4, 38, 16, 40, 'Fase 2, Mapeamento: identificar na CVI os macroprocessos e processos que serão avaliados.'],
            [34.5, 38, 16, 40, 'Fase 3, Coleta: aplicar o questionário a gestores e servidores e reunir evidências documentais.'],
            [49.3, 38, 16, 40, 'Fase 4, Diagnóstico: calcular a média ponderada por dimensão e o nível de maturidade.'],
            [64.1, 38, 16, 40, 'Fase 5, Plano de ação: transformar as lacunas em prioridades para subir de nível.'],
            [79, 38, 16, 40, 'Fase 6, Monitoramento: reavaliar todo ano, para que a jornada seja contínua e mensurável.']])

F12 = gfig(13, 'Do diagnóstico estratégico ao plano de ação estruturado.',
           'Um radar com a dimensão Cultura e Competências em baixa pontuação, uma seta verde e uma planta com lista de verificação representando o plano de ação.',
           [[9, 34, 27, 41, 'O diagnóstico aponta o gargalo: neste exemplo, Cultura e Competências com baixa pontuação.'],
            [34, 37, 52, 23, 'A lacuna vira um plano de ação, com prioridades e responsáveis.'],
            [57, 62, 32, 14, 'Direcionamento prático: orçamento para capacitação continuada e gestão da mudança vinculada à CVI.'],
            [21, 81, 58, 14, 'O diagnóstico revela a prontidão organizacional real do órgão, e não apenas um selo de maturidade.']])

F13 = gfig(14, 'A agenda futura: refinamento e empírica institucional.',
           'Caminho luminoso ligando três plataformas: calibração por especialistas, consistência interna e aplicação piloto.',
           [[11, 43, 26, 36, 'Calibração por especialistas: método Delphi para refinar os pesos percentuais das dimensões.'],
            [41, 39, 22, 33, 'Validade do instrumento: ampliar os itens e avaliar medidas de qualidade adequadas a indicadores formativos.'],
            [65, 31, 22, 34, 'Aplicação piloto: execução controlada em secretarias de perfis e complexidades diferentes.']])

F14 = gfig(15, 'Tecnologia é o meio; o valor público é o fim.',
           'Cidade luminosa estilizada, com pontes, prédios públicos e vias de dados em verde e dourado, ao redor da frase final do artigo.',
           [[18, 29, 63, 24, 'Tecnologia é o meio; o valor público é o fim.'],
            [23, 55, 55, 21, 'A transformação acontece na reformulação dos fluxos de poder, da cultura e dos serviços que facilitam a vida do cidadão.']])

sections = [
    section('01', 'abismo', 'A lacuna subnacional na medição da maturidade',
            'O Brasil tem instrumentos consolidados, mas nenhum, entre os examinados, desenhado para o órgão público estadual.',
            [F1],
            [acc('Três referências nacionais',
                 ['O Nível de Maturidade Digital de Serviços Públicos (NMDSP), instituído pela Portaria SGD/MGI nº 1.083/2025, tem o serviço público como unidade de análise e é aplicado a mais de cinco mil serviços do Poder Executivo federal, com reavaliação semestral.',
                  'O Modelo de Maturidade de Dados (MMD) orienta órgãos federais na governança e na gestão de dados, por autoavaliação.',
                  'O Índice Transformação Digital Brasil (ITDBr), da PwC com a Fundação Dom Cabral, mede a maturidade de empresas em dez dimensões, numa escala de 1 a 6.']),
             acc('A lacuna que o artigo identifica',
                 ['Cada instrumento trata de uma unidade de análise diferente: o serviço, o domínio de dados ou a empresa. Entre os examinados no estudo, nenhum oferece, ao mesmo tempo, visão organizacional integrada, ancoragem em cadeia de valor pública e adaptação ao nível estadual.',
                  'A literatura consultada trata da mensuração de resultados da transformação digital (Dobrolyubova, 2021) e da entrega de serviços públicos no Brasil (Filgueiras, Flávio e Palotti, 2019), sem apresentar um instrumento diagnóstico de maturidade para órgãos estaduais.',
                  'O artigo não afirma que inexistam outros instrumentos, nacionais ou internacionais, aplicáveis a governos subnacionais. Essa verificação, por revisão sistemática com protocolo explícito, fica como pesquisa futura.'],
                 'A contribuição é de integração: dimensões de maturidade articuladas a uma arquitetura de processos públicos estaduais, e não dimensões inéditas.'),
             acc('Transformação digital não é digitalização',
                 ['Digitalizar converte processos analógicos em digitais. A transformação digital altera o modelo de operação do Estado, promove a desburocratização e coloca o cidadão no centro.',
                  'Goiás tem posição de destaque em rankings de oferta de serviços digitais, com mais de 700 serviços na Carta de Serviços. Ainda assim, o artigo lembra que digitalizar serviços isoladamente não basta: é preciso mudar cultura, processos e governança.']),
             acc('Complementar, e não substituto',
                 ['O MMDI-GO não pretende substituir os instrumentos federais. Os atributos técnicos do NMDSP podem servir de evidência na dimensão Experiência do Cidadão, e os resultados do MMD podem subsidiar a dimensão Dados e Interoperabilidade.',
                  'O Modelo de Maturidade em Governo Digital (ENAP; MGI, 2023) e o GovTech Maturity Index (Banco Mundial, 2025) são referências conceituais, mas não entram no quadro comparativo, o que o artigo registra como limitação.'])]),

    section('02', 'metodo', 'Método: Design Science Research',
            'Uma ponte entre a teoria e a prática, construída em seis passos e cinco critérios.',
            [F2],
            [acc('Seis atividades de Peffers',
                 ['O processo segue as seis atividades de Peffers et al. (2007): identificar o problema, definir os objetivos da solução, projetar o artefato, demonstrar, avaliar e comunicar.',
                  'Neste artigo, a demonstração é um exemplo ilustrativo de cálculo, com dados fictícios, e a avaliação é teórica, ex ante e formativa: argumentação informada, análise comparativa com instrumentos existentes e o exemplo. A validação empírica não foi realizada e fica como etapa futura em órgãos-piloto.'],
                 'O MMDI-GO é tratado como modelo proposto, instrumento preliminar e artefato a validar, e não como instrumento validado.'),
             acc('Como o artefato foi construído',
                 ['Seis passos: levantar fatores críticos de sucesso e barreiras na literatura; analisar a estrutura da CVI; agrupar os fatores em dimensões; definir a escala de maturidade; atribuir pesos iniciais e definir regras de agregação; e formular os itens do questionário.',
                  'Cinco critérios guiaram o desenho: rastreabilidade, aderência à CVI, gradação (sem critérios absolutos que penalizem órgãos por razões legais, de segurança ou de inclusão), parcimônia e neutralidade tecnológica.']),
             acc('Referenciais teóricos',
                 ['A perspectiva de valor público (Moore, 1995) fundamenta a dimensão Experiência do Cidadão. As capacidades dinâmicas (Teece, Pisano e Shuen, 1997) e os estudos sobre estratégia e cultura (Kane et al., 2015) fundamentam Liderança e Cultura.',
                  'A governança da era digital (Dunleavy et al., 2006) sustenta a ênfase na integração entre processos e entre bases de dados, e a literatura de modelos de maturidade (Paulk et al., 1993; Pöppelbuß e Röglinger, 2011) sustenta a escala em níveis e o propósito descritivo e prescritivo.',
                  'O artigo registra que esses vínculos são uma proposta de articulação do autor, e não resultado de teste empírico.']),
             acc('Seleção da literatura',
                 ['A literatura foi selecionada de forma intencional e não sistemática: periódicos, relatórios do Banco Mundial e da OCDE e documentos oficiais brasileiros, em sua maioria de 2020 a 2025, além de obras fundacionais sobre modelos de maturidade, design science e governança pública.',
                  'Não foram analisados casos de outros países como unidade de estudo: as referências internacionais servem de fundamentação conceitual. A falta de protocolo sistemático limita a reprodutibilidade e a abrangência da revisão, e as lições são consideradas transferíveis ao contexto estadual brasileiro apenas mediante adaptação institucional.'],
                 'Seleção das dimensões, pesos e redação dos itens resultam de julgamento do pesquisador fundamentado na literatura, e não de consenso empírico.')]),

    section('03', 'cvi', 'Ancoragem na Cadeia de Valor Integrada',
            'O mapa de processos do Estado serve de base para o diagnóstico.',
            [F3, F4],
            [acc('Três camadas de processos',
                 ['A Cadeia de Valor Integrada (CVI) de Goiás, inspirada em Porter e adaptada à administração pública, organiza as atividades estaduais em macrofunções, macroprocessos e processos de trabalho.',
                  'Os processos finalísticos entregam valor direto ao cidadão. Os processos gerenciais medem, monitoram e controlam as metas. Os de suporte sustentam a infraestrutura e os recursos humanos.'],
                 'A CVI funciona como o mapa sobre o qual o framework de maturidade é aplicado.'),
             acc('Por que a retaguarda importa',
                 ['A integração digital entre as camadas evita que a modernização da ponta, o serviço ao cidadão, seja freada por uma retaguarda analógica e ineficiente (Filgueiras, Flávio e Palotti, 2019).',
                  'O artigo apresenta essa relação como proposição teórica que o MMDI-GO poderá ajudar a testar. Como o estudo não mediu órgãos, não permite concluir que ela de fato ocorra.']),
             acc('Fatores críticos de sucesso',
                 ['O apoio da alta gestão, porque a transformação exige remanejar recursos e mudar normas. E a governança de dados e a interoperabilidade, que permitem à administração funcionar de forma sistêmica e não como silos isolados (Banco Mundial, 2025).']),
             acc('Barreiras organizacionais',
                 ['A resistência cultural dos servidores, o déficit de competências digitais e as restrições orçamentárias e normativas, como a rigidez dos processos licitatórios e a descontinuidade de fluxos financeiros em projetos de longo prazo (Fitriani et al., 2025; Filgueiras, Flávio e Palotti, 2019).'])]),

    section('04', 'dimensoes', 'As seis dimensões e seus pesos',
            'Seis dimensões ponderadas, derivadas da literatura e da estrutura da CVI.',
            [F5, weights, F6, F7, F8],
            [acc('Rastreabilidade das dimensões',
                 ['Cada dimensão se associa a fontes da literatura, a um elemento da CVI e a uma justificativa. Liderança e Estratégia Digital liga-se aos processos gerenciais. Cultura e Competências e Infraestrutura e Tecnologia, aos processos de suporte.',
                  'Processos e Serviços cobre as três camadas da CVI. Dados e Interoperabilidade é transversal às camadas. Experiência do Cidadão vincula-se aos processos finalísticos e à Carta de Serviços.']),
             acc('Pesos iniciais, sujeitos ao método Delphi',
                 ['Os pesos são propostos pelo autor, por julgamento fundamentado na literatura, e não derivados de procedimento empírico. A frequência com que um fator aparece na literatura não equivale à sua contribuição relativa para a maturidade, razão pela qual os pesos são hipótese de trabalho. O peso de 25% da dimensão Liderança, em particular, ainda não tem validação.',
                  'A calibração será feita por método Delphi, com número de rodadas, critério de consenso e perfil dos especialistas definidos em protocolo prévio.'],
                 'Tecnologia é condição necessária, mas não suficiente: por isso pesa 8%, enquanto liderança pesa 25%.'),
             acc('Regras de cálculo e conversão em nível',
                 ['A pontuação de cada dimensão é a média dos itens respondidos, excluídos os marcados como "não se aplica", com justificativa registrada. O índice global informativo é a média das dimensões ponderada pelos pesos.',
                  'Como os níveis são cumulativos, propõe-se, como regra preliminar a testar no piloto, que o nível do órgão seja limitado pela dimensão de menor pontuação: um desempenho elevado numa dimensão não compensa a deficiência em outra.',
                  'Os pontos de corte que convertem pontuações em níveis não estão definidos no artigo e dependerão da calibração por especialistas e do piloto. Análises de sensibilidade vão comparar o índice com os pesos propostos e com pesos iguais.'],
                 'A regra do menor valor é não compensatória: é ela que impede que uma nota alta mascare uma lacuna.')]),

    section('05', 'escala', 'Escala de maturidade e instrumento de coleta',
            'Cinco níveis cumulativos e um questionário preliminar de 24 itens.',
            [F9, levels],
            [acc('Uma escala inspirada no CMMI, e não uma adaptação formal',
                 ['Foram aproveitados o princípio de níveis cumulativos e a lógica de evolução de processos informais para processos definidos, gerenciados e otimizados, reinterpretados para a administração pública.',
                  'A escala descreve a evolução da capacidade institucional, e não a adoção de uma tecnologia específica. Serviços preditivos, por exemplo, não são condição para o nível 5. Os descritores são gerais, e os específicos por dimensão virão na validação de conteúdo.',
                  'A escala de níveis é distinta da escala de resposta dos itens: esta mede o grau de implementação, e a conversão das pontuações em nível segue a regra de cálculo da seção anterior.']),
             acc('O questionário diagnóstico',
                 ['São 24 afirmativas, de três a seis por dimensão, respondidas numa escala ordinal de cinco pontos que mede o grau de implementação, e não a concordância: 1, inexistente; 2, iniciado ou pontual; 3, formalizado em parte; 4, implementado na maior parte do escopo do órgão; 5, plenamente implementado e revisado periodicamente. Há ainda a opção "não se aplica", com justificativa registrada.',
                  'Exemplos: o órgão possui plano de transformação digital formalizado; o órgão compartilha e consome dados de outros órgãos, evitando que o cidadão repita informações; o cidadão consegue iniciar e concluir o serviço por mais de um canal, respeitadas as exceções legais.',
                  'Os itens foram redigidos para não combinar condições distintas, e os que as combinavam na versão preliminar foram desdobrados.'],
                 'Cada item vem com a fonte que sustenta o tema, e não a existência de um item equivalente na fonte.'),
             acc('Por que não usar só o alfa de Cronbach',
                 ['As dimensões são concebidas como índices formativos: os indicadores compõem o construto, em vez de refleti-lo. Nesse caso, o alfa de Cronbach pode não ser o indicador adequado, e consistência interna não equivale a validade.',
                  'Com apenas três a seis itens por dimensão, o conjunto é versão preliminar, passível de ampliação. O piloto avaliará alternativas, como a análise de colinearidade entre itens e a validade de conteúdo por especialistas.'])]),

    section('06', 'aplicacao', 'Aplicação: do diagnóstico ao plano de ação',
            'Seis fases cíclicas que fazem da medição uma rotina de melhoria.',
            [F11, F12, example],
            [acc('As seis fases',
                 ['1. Sensibilização: apresentar os objetivos à alta liderança. 2. Mapeamento na CVI: identificar os macroprocessos e processos a avaliar. 3. Coleta de dados: aplicar o questionário e reunir evidências documentais, registrando no relatório as divergências relevantes entre respostas e documentos.',
                  '4. Diagnóstico: calcular a pontuação por dimensão, o índice global e o nível de maturidade. 5. Plano de ação: gerar o relatório de diagnóstico e a análise de lacunas, com as prioridades para subir de nível. 6. Monitoramento: reavaliar anualmente.'],
                 'O diagnóstico não entrega só um selo de maturidade: entrega um mapa de lacunas.'),
             acc('Exemplo ilustrativo, com dados fictícios',
                 ['O artigo calcula o índice de um órgão hipotético, sem relação com nenhum órgão do Estado, para mostrar o funcionamento da conta. Com os pesos iniciais o índice global informativo é 2,61, e com pesos iguais é 2,67, o que indica baixa sensibilidade aos pesos neste exemplo.',
                  'Pela regra do menor valor, o nível do órgão ficaria limitado pela menor pontuação (2,0), cuja correspondência com um nível depende de pontos de corte ainda não definidos. Dados e Interoperabilidade, Cultura e Competências e Experiência do Cidadão seriam as dimensões prioritárias no plano de ação.'],
                 'O exemplo mostra o funcionamento do cálculo e a diferença entre a regra compensatória e a não compensatória. Não permite inferir a validade do modelo.'),
             acc('Propósito do modelo',
                 ['O MMDI-GO tem propósito descritivo, para diagnosticar a situação atual, e prescritivo, para indicar caminhos de melhoria. Não é comparativo entre órgãos, uso que exigiria validação prévia.'])]),

    section('07', 'limites', 'Discussão, limites e agenda futura',
            'O que a proposta permite afirmar, e o que ainda depende de validação.',
            [F13],
            [acc('Três diferenciais propostos',
                 ['Desenho para a unidade estadual, escala pouco contemplada pelos modelos federais analisados. Ancoragem na CVI de Goiás, que nesta versão delimita o escopo e contextualiza os resultados, enquanto a captura da interdependência entre processos finalísticos, gerenciais e de suporte ainda precisa ser verificada em aplicação. E pesos diferenciados por dimensão, calibráveis pelo método Delphi, cuja vantagem sobre pesos iguais será avaliada por análise de sensibilidade.',
                  'Em conjunto, configuram uma contribuição de integração, e não a criação de dimensões inéditas. Como os critérios do quadro comparativo partem do que o MMDI-GO pretende ter, a comparação pode favorecê-lo e deve ser lida como mapeamento de escopo.']),
             acc('Hipóteses a testar',
                 ['A liderança e a interoperabilidade de dados podem ser motores da evolução entre níveis. Cultura e competências podem ser o principal desafio entre os níveis intermediários e avançados. Tudo isso são expectativas teóricas, que dependem de validação empírica.']),
             acc('Limitações declaradas',
                 ['O MMDI-GO não foi validado empiricamente, e o exemplo de cálculo usa dados fictícios. Os pesos são iniciais, propostos pelo autor, e os pontos de corte entre níveis não estão definidos. O instrumento é curto, com 24 itens, e nem a consistência interna nem a adequação de medidas a indicadores formativos foram testadas.',
                  'A seleção da literatura foi intencional, sem protocolo sistemático, e a transferibilidade das lições internacionais não foi demonstrada. Parte da literatura trata de contextos nacionais distintos do brasileiro.',
                  'O modelo de governo digital da ENAP e o GovTech Maturity Index ficaram fora do quadro comparativo. O instrumento depende de autorrelato, sujeito a viés de desejabilidade social. A ancoragem na CVI delimita o escopo, e não estrutura a pontuação por processo.',
                  'Por fim, o autor integra a instituição responsável pelos documentos que sustentam o modelo (SCTP/TransformaLAB, SEAD-GO), o que pode influenciar a interpretação do contexto goiano.'],
                 'O estudo não mediu órgãos: nada se afirma sobre a validade, a confiabilidade ou a efetividade do modelo.'),
             acc('Agenda de pesquisa',
                 ['Validar o conteúdo e calibrar os pesos por Delphi com especialistas. Aplicar um piloto em secretarias de complexidades diferentes, avaliando confiabilidade, validade e pontos de corte. Ampliar os itens, elaborar descritores por dimensão e avaliar a natureza formativa dos indicadores.',
                  'Fazer análise de sensibilidade dos pesos e avaliar a pontuação por processo ou por camada da CVI. Adotar protocolo sistemático de revisão da literatura, incluindo outros instrumentos nacionais e internacionais. Tratar a ética e a proteção de dados dos respondentes, conforme a LGPD. E desenvolver uma plataforma digital para coletar e processar os dados do diagnóstico.'])]),
]

closing = ('<section aria-labelledby="sintese" class="mt-16 rounded-2xl border bg-secondary/50 p-7"><h2 id="sintese" class="text-2xl font-semibold">A síntese</h2>'
           '<p class="mt-3 leading-relaxed text-muted-foreground">A transformação digital do setor público é, antes de tudo, um desafio de gestão de pessoas e processos. O MMDI-GO propõe um mapa diagnóstico para que gestores antecipem obstáculos e priorizem ações, o que depende de verificação em aplicação.</p>'
           + F14 +
           '<p class="mt-6 rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] italic leading-relaxed text-accent-foreground">Tecnologia é o meio; o valor público é o fim.</p></section>')


def build():
    stat = lambda n, l: ('<div><dt class="font-display text-2xl text-ochre" data-count data-from="0" data-to="%s">%s</dt>'
                         '<dd class="mt-1 text-xs uppercase tracking-wide text-primary-foreground/70">%s</dd></div>' % (n, n, l))
    header = ('<header class="relative overflow-hidden text-primary-foreground" style="background-image:var(--gradient-deep)">'
              '<div class="absolute inset-0" style="opacity:.2;background:url(../assets/img/mmdi-slide-01.jpg) 100%% 40%%/auto 150%% no-repeat;mix-blend-mode:screen" aria-hidden="true"></div>'
              '<div class="surface-paper absolute inset-0 opacity-30" aria-hidden="true"></div>'
              '<div class="relative mx-auto max-w-3xl px-6 py-20 sm:py-28">'
              '<p class="text-xs font-semibold uppercase tracking-[0.2em] text-ochre">Design Science Research · Maturidade digital · Goiás</p>'
              '<h1 class="mt-6 text-4xl leading-[1.1] font-semibold sm:text-5xl">Maturidade digital no <span class="text-gradient-warm">setor público goiano</span></h1>'
              '<p class="mt-5 text-lg leading-relaxed text-primary-foreground/80">O MMDI-GO: proposta de um framework e de um instrumento de medição ancorados na Cadeia de Valor Integrada do Estado.</p>'
              '<p class="mt-8 text-sm text-primary-foreground/70">Carlos Hernane de Oliveira</p>'
              '<div class="mt-6"><a href="../assets/pdf/%s" target="_blank" rel="noopener noreferrer" '
              'class="inline-flex items-center gap-2 rounded-full bg-ochre px-6 py-3 text-sm font-semibold text-ochre-foreground shadow-lift transition-transform hover:-translate-y-0.5">'
              % PDF + BOOK + 'Leia o Artigo na Íntegra</a>'
              '<p class="mt-3 max-w-md text-sm leading-relaxed text-primary-foreground/70">Abre o PDF completo do artigo em uma nova aba, para leitura direta no navegador.</p></div>'
              '<dl class="reveal mt-10 grid grid-cols-2 gap-6 sm:grid-cols-4">'
              + stat('6', 'dimensões') + stat('5', 'níveis de maturidade') + stat('24', 'itens diagnósticos') + stat('6', 'fases de aplicação')
              + '</dl></div></header>')
    intro = ('<section aria-labelledby="resumo-mm"><h2 id="resumo-mm" class="text-2xl font-semibold">Do que trata o artigo</h2>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">Goiás priorizou a digitalização de serviços, mas não tem um instrumento padronizado para medir a evolução digital dos seus órgãos. O artigo propõe, em caráter preliminar, o Modelo de Maturidade Digital Integrado de Goiás (MMDI-GO), um framework e uma metodologia de medição para a administração pública estadual.</p>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">Com base na Design Science Research, o modelo reúne seis dimensões de maturidade, num contínuo de cinco níveis, e traz regras de cálculo e um questionário diagnóstico de 24 itens. A Cadeia de Valor Integrada delimita o escopo e contextualiza a leitura dos resultados por camada de processos.</p>'
             '<p class="mt-4 rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] leading-relaxed text-accent-foreground">O artefato passou por avaliação teórica e por um exemplo ilustrativo de cálculo, e ainda não foi validado empiricamente. Os pesos das dimensões são iniciais e dependem de calibração por especialistas.</p></section>'
             '<section aria-labelledby="objetivos-mm" class="mt-10 rounded-2xl border bg-secondary/50 p-7"><h2 id="objetivos-mm" class="text-2xl font-semibold">Pergunta e objetivos</h2>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Pergunta de pesquisa</h3><p class="mt-2 leading-relaxed text-muted-foreground">Como estruturar um modelo de maturidade digital para órgãos públicos estaduais que integre capacidades digitais, arquitetura de processos e entrega de valor público, considerando as especificidades institucionais do Estado de Goiás?</p></div>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Quatro objetivos específicos</h3><ul class="mt-3 space-y-2 text-muted-foreground">'
             + ''.join('<li class="flex gap-3"><span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-sage"></span><span class="leading-relaxed">%s</span></li>' % t for t in [
                 'Sistematizar, a partir da literatura e de documentos institucionais de Goiás, os fatores críticos de sucesso e as barreiras organizacionais da transformação digital no setor público.',
                 'Integrar as dimensões de maturidade digital à Cadeia de Valor Integrada, abrangendo processos finalísticos, gerenciais e de suporte.',
                 'Desenvolver um instrumento diagnóstico preliminar, com indicadores, itens, regras de agregação e uma escala de cinco níveis.',
                 'Oferecer uma base teórico-metodológica para uma aplicação piloto futura.'])
             + '</ul></div></section>')
    main = '<main class="mx-auto max-w-3xl px-6 py-16">' + intro + '<div class="mt-14 space-y-14">' + ''.join(sections) + '</div>' + closing + '</main>'
    footer = ('<footer class="border-t bg-card"><div class="mx-auto max-w-3xl px-6 py-10 text-sm text-muted-foreground">'
              '<p class="font-display text-base text-foreground">Framework de maturidade para a transformação digital e de serviços no setor público goiano: proposição de um instrumento de medição</p>'
              '<p class="mt-2">Carlos Hernane de Oliveira. Superintendência Central de Transformação Pública (SCTP/TransformaLAB), Secretaria de Estado da Administração de Goiás (SEAD-GO).</p>'
              '<p class="mt-2">Conflito de interesses: o autor integra a instituição responsável pelos documentos institucionais citados (Goiás, 2021; 2023). Aspectos éticos: esta etapa usou apenas literatura e documentos institucionais, sem participação de seres humanos.</p>'
              '<p class="mt-4">Palavras-chave: transformação digital; maturidade digital; setor público; cadeia de valor; Design Science Research; Governo de Goiás.</p></div></footer>')
    page = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>'
            '<title>MMDI-GO: maturidade digital no setor público goiano</title>'
            '<meta name="description" content="Artigo que propõe o Modelo de Maturidade Digital Integrado de Goiás (MMDI-GO): seis dimensões, cinco níveis e um questionário de 24 itens, delimitado pela Cadeia de Valor Integrada."/>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap"/>'
            '<link rel="stylesheet" href="../assets/styles.css"/><link rel="stylesheet" href="../assets/anim.css"/><link rel="stylesheet" href="../assets/mmdi.css"/>'
            '<script>document.documentElement.classList.add("js")</script></head><body>'
            + shell.nav(SLUG, '../') + '<div class="min-h-screen">' + header + main + footer + '</div>'
            '<script src="../assets/app.js"></script><script src="../assets/anim.js"></script><script src="../assets/mmdi.js"></script></body></html>')
    os.makedirs('%s/%s' % (S, SLUG), exist_ok=True)
    open('%s/%s/index.html' % (S, SLUG), 'w', encoding='utf8').write(page)
    for f in os.listdir(SRC + '/img'):
        shutil.copy(SRC + '/img/' + f, S + '/assets/img/' + f)
    shutil.copy(SRC + '/' + PDF, S + '/assets/pdf/' + PDF)
    shutil.copy('build/mmdi.css', S + '/assets/mmdi.css')
    shutil.copy('build/mmdi.js', S + '/assets/mmdi.js')
    shutil.copy('build/anim.css', S + '/assets/anim.css')
    shutil.copy('build/anim.js', S + '/assets/anim.js')


if __name__ == '__main__':
    build()
