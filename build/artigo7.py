"""Artigo 07: Fatores organizacionais associados à intenção de servidores públicos de aprender e usar IA (revisão de escopo).

Gera docs/ia-no-setor-publico/index.html a partir do texto do artigo e de 12 dos 15 slides da apresentação
(src/orig/ia-servidores/img). As imagens ganham a galeria animada de build/mmdi.css e build/mmdi.js.
Os slides 9, 11 e 12 da apresentação original ficaram de fora por afirmarem mais do que a revisão sustenta.
"""
import json, os, shutil, sys
sys.path.insert(0, 'build')
import shell
import artigo4
from artigo4 import acc, e, BOOK

S = 'docs'
SLUG = 'ia-no-setor-publico'
SRC = 'src/orig/ia-servidores'
PDF = 'Fatores_organizacionais_IA_servidores_revisao_escopo.pdf'
SEQ = {}  # número do slide original -> número exibido na página


def gfig(n, title, alt, tour):
    """Imagem animada: slide n da apresentação, com roteiro de regiões em destaque (x, y, largura, altura em %, texto)."""
    SEQ[n] = len(SEQ) + 1
    img = 'ia-slide-%02d.jpg' % n
    return ('<figure class="gfig mt-6 overflow-hidden rounded-xl border bg-card shadow-[var(--shadow-soft)]" data-tour=\'%s\'>'
            '<div class="gfig-stage"><div class="gfig-zoom">'
            '<img class="gfig-img" src="../assets/img/%s" width="1376" height="768" loading="lazy" alt="%s"/>'
            '<div class="gfig-fx" aria-hidden="true"><i class="gfig-sweep"></i><i class="gfig-scan"></i><i class="gfig-glare"></i><i class="gfig-wipe"></i></div>'
            '<div class="gfig-spot" aria-hidden="true"></div></div></div>'
            '<div class="gfig-bar"></div>'
            '<figcaption class="border-t px-5 py-4 text-sm leading-relaxed text-muted-foreground">%s'
            '<span class="mt-1 block text-xs text-muted-foreground/80">Imagem %d da apresentação do artigo. '
            '<a class="underline underline-offset-2" href="../assets/img/%s" target="_blank" rel="noopener">Ver a imagem original</a></span></figcaption></figure>'
            % (e(json.dumps(tour, ensure_ascii=False), quote=True).replace('&#x27;', '&#39;'), img, e(alt), e(title, quote=False), SEQ[n], img))


def section(num, sid, title, sub, blocks, accs):
    return ('<section id="%s" aria-labelledby="%s-titulo"><div class="flex items-baseline gap-4">'
            '<span class="font-display text-3xl text-ochre">%s</span><div><h2 id="%s-titulo" class="text-2xl font-semibold">%s</h2>'
            '<p class="mt-1 text-sm text-muted-foreground">%s</p></div></div>%s<div class="mt-6 space-y-3">%s</div></section>'
            % (sid, sid, num, sid, e(title, quote=False), e(sub, quote=False), ''.join(blocks), ''.join(accs)))


# ---------- gráficos em HTML ----------
BARR = [('Conhecimento limitado das ferramentas', 2.4, '#2d5bd1'), ('Treinamento inadequado em IA', 2.4, '#2d5bd1'),
        ('Benefícios pouco claros para o próprio trabalho', 2.3, '#5a6b7a'), ('Falta de diretrizes organizacionais', 2.2, '#137d5c'),
        ('Falta de ferramentas adequadas no órgão', 2.1, '#5a6b7a'), ('Pouco apoio dos pares', 2.0, '#cf7638'),
        ('Pouco tempo para aprender as ferramentas', 1.9, '#a8483a')]
barras = ('<div class="wchart reveal rounded-xl border bg-card p-5 shadow-[var(--shadow-soft)] mt-6" role="group" aria-label="Barreiras percebidas por servidores finlandeses que não usavam IA">'
          '<p class="text-sm font-medium">Barreiras percebidas por servidores que não usavam IA (média de 0 a 3)</p>'
          '<p class="mt-1 text-xs text-muted-foreground">Pulkkinen (2026a): organização pública de saúde e assistência social da Finlândia, 236 respondentes não usuários, taxa de resposta de 10,3%.</p>'
          '<div class="wchart-rows" style="display:grid;gap:12px;margin-top:18px">'
          + ''.join('<div class="wrow"><b>%s</b><span class="wtrack"><i style="--w:%.1f%%;--c:%s;--d:%.2fs"></i></span><span class="wval">%s</span></div>'
                    % (e(n), v / 3 * 100, c, .15 * i, ('%.1f' % v).replace('.', ',')) for i, (n, v, c) in enumerate(BARR))
          + '</div><p class="mt-4 text-sm text-muted-foreground">É um levantamento de uma única organização, e o tempo para aprender aparece como a barreira de menor média entre as sete, mas ainda assim relevante.</p></div>')

FUNIL = [('Resultados exibidos nas 8 buscas', 281, '#5a6b7a'), ('Títulos únicos', 200, '#276fa0'), ('Triados por resumo', 113, '#2d5bd1'),
         ('Com resumo disponível', 103, '#137d5c'), ('Estudos na síntese preliminar', 50, '#cf7638'), ('Lidos em texto completo', 13, '#a8483a')]
funil = ('<div class="wchart reveal rounded-xl border bg-card p-5 shadow-[var(--shadow-soft)] mt-6" role="group" aria-label="Fluxo de identificação e seleção dos estudos">'
         '<p class="text-sm font-medium">Do primeiro resultado à síntese preliminar</p>'
         '<p class="mt-1 text-xs text-muted-foreground">Busca exploratória no Consensus em 10 de novembro de 2026. As demais bases ainda não foram pesquisadas.</p>'
         '<div class="wchart-rows" style="display:grid;gap:12px;margin-top:18px">'
         + ''.join('<div class="wrow"><b>%s</b><span class="wtrack"><i style="--w:%.1f%%;--c:%s;--d:%.2fs"></i></span>'
                   '<span class="wval" data-count data-from="0" data-to="%d" data-delay="%d">%d</span></div>'
                   % (e(n), v / 281 * 100, c, .15 * i, v, 150 * i, v) for i, (n, v, c) in enumerate(FUNIL))
         + '</div></div>')

# ---------- figuras (slides) ----------
F1 = gfig(1, 'A arquitetura da adoção de IA no setor público: o que transforma a disponibilidade tecnológica em intenção de aprender e usar.',
          'Slide de abertura com um desenho técnico de uma torre em construção e o título A Arquitetura da Adoção de IA no Setor Público.',
          [[52, 22, 45, 31, 'O título: a adoção de IA tratada como arquitetura, algo que se constrói por condições organizacionais deliberadas.'],
           [52, 56, 42, 20, 'A pergunta do estudo: que fatores organizacionais transformam a disponibilidade tecnológica em intenção de aprender e usar.'],
           [5, 5, 42, 85, 'A torre ainda em planta: a imagem sugere uma estrutura em construção, e a revisão mapeia o que se sabe sobre os alicerces.']])

F2 = gfig(2, 'Três diretrizes convergem para uma mesma premissa: a adoção exige servidores capacitados e dispostos a mudar.',
          'Três painéis, OCDE (2026), Plano Brasileiro de IA (2025) e Guia do TCU (2024), com vias que convergem para um círculo central chamado O Servidor Público.',
          [[9.8, 19, 25, 20, 'OCDE (2026): alfabetização básica em IA para a maioria dos servidores, com necessidades diferentes por perfil.'],
           [37.4, 19, 24.4, 20, 'Plano Brasileiro de IA (2025): capacitação contínua dos servidores para acompanhar a adoção.'],
           [64.7, 19, 25.4, 20, 'Guia do TCU (2024): decisões automatizadas por IA generativa não devem ser adotadas sem revisão humana.'],
           [42.5, 66, 14, 20, 'O servidor público: no centro, é quem precisa avaliar o que a ferramenta produz.'],
           [21.8, 83, 56, 11.5, 'A premissa comum: a adoção exige servidores capacitados e dispostos a mudar.']])

F3 = gfig(3, 'O descompasso: a expectativa institucional avança, e a formação real não acompanha.',
          'Duas colunas, a Expectativa Institucional, com uma nuvem de servidores, e a Realidade Humana, com um rosto em malha, separadas por engrenagens que não se encaixam.',
          [[3.6, 28, 30, 50, 'A expectativa institucional: o Poder Executivo lidera 61% das ações de IA em 311 documentos de governo analisados (Alcântara, Oliveira e Moraes, 2026).'],
           [36, 20, 28, 58, 'As engrenagens fora de sincronia: a imagem representa o desencontro entre o plano e a prática.'],
           [66.5, 22, 30, 56, 'A realidade humana: percepção de ganhos de eficiência e falta de preparo, em um levantamento de amostra pequena (Toledo e Mendonça, 2023).'],
           [3.6, 80.7, 92.7, 12.4, 'Há bom desenho normativo, como a Matriz de Competências do MGI (2026), mas a evidência sobre a formação real é escassa.']])

F4 = gfig(4, 'Usar e aprender são intenções diferentes, e as condições que favorecem uma e outra podem diferir.',
          'Tabela comparando Intenção de Usar e Intenção de Aprender em definição, gatilho motivacional e resultado organizacional.',
          [[14.5, 21.5, 39.6, 10, 'Intenção de usar: apertar botões e usar prompts básicos para ganhar tempo.'],
           [14.5, 33, 39.6, 45, 'O gatilho é a pressão por produtividade e a utilidade percebida, com o risco de automação superficial sem revisão humana.'],
           [55.2, 21.5, 40.7, 10, 'Intenção de aprender: entender como a ferramenta funciona, seus limites e seus riscos.'],
           [55.2, 33, 40.7, 45, 'Aqui entram segurança para errar, tempo protegido e governança. É uma distinção conceitual do autor, a testar em estudo empírico.'],
           [3.8, 81, 92.5, 12.5, 'Quem quer usar uma ferramenta para ganhar tempo não necessariamente quer estudá-la.']])

F5 = gfig(5, 'O ponto cego: a literatura mede sobretudo a intenção de usar, e quase nunca a de aprender.',
          'Gráfico de radar com seis eixos, Adoção, Uso Declarado, Prontidão Tecnológica, Intenção de Aprender, Aceitação e Adoção, em que o eixo Intenção de Aprender é quase nulo, e três blocos de texto à direita.',
          [[4, 20, 50, 74, 'O radar: adoção, uso declarado, prontidão e aceitação aparecem bem medidos; a intenção de aprender, quase nada.'],
           [20, 58, 16, 30, 'O eixo da intenção de aprender é o que quase não aparece nos estudos.'],
           [58, 22.8, 38.3, 21.5, 'Entre os 50 estudos de 2020 a 2026, predominam os referenciais TOE, TAM e UTAUT.'],
           [59, 51.4, 36, 19.6, 'A lacuna: quase nenhum estudo tem a intenção de aprender IA como desfecho; a aprendizagem aparece como necessidade de treinamento.'],
           [58, 75, 38.3, 17, 'A conclusão do slide é uma leitura do autor: oferecer um curso não cria, por si, a disposição de fazê-lo.']])

F6 = gfig(6, 'Quatro pilares organizacionais para a intenção de aprender e usar.',
          'Quatro blocos em losango convergem para um cubo central azul: Governança, Cultura, Capacitação e Confiança, com um feixe de luz chamado Intenção Autêntica de Aprender.',
          [[10.5, 40, 40, 22, '1. Governança: a clareza das regras, com orientação sobre dados, revisão humana e ferramentas autorizadas.'],
           [50.5, 40, 40, 22, '2. Cultura: o apoio psicossocial da chefia, da alta gestão e dos colegas.'],
           [7, 62, 43, 23, '3. Capacitação: acesso a ferramentas e cursos, e tempo para aprender.'],
           [50.5, 62, 43, 23, '4. Confiança: a segurança psicológica, ou segurança para experimentar.'],
           [47, 29, 46, 9, 'No centro, a intenção de aprender, tratada pelo autor como o resultado dos quatro pilares.']])

F7 = gfig(7, 'Pilar 1: regras claras funcionam como barreiras de proteção.',
          'Uma ponte azul entre duas grades de aço, com rótulos Risco Institucional, Ambiguidade Legal, Estrutura Provisória e Barreira Definida, e três colunas de texto.',
          [[7, 19, 86, 43, 'A ponte com guarda-corpos: as regras delimitam um terreno seguro para agir.'],
           [7.3, 62.5, 25, 29.3, 'A ambiguidade: incerteza jurídica, vazio de responsabilização e regulação ambígua aparecem como barreiras em estudos da Áustria, do Vietnã e da Finlândia.'],
           [37, 62.5, 27.7, 29.3, 'O medo de errar: sem orientação sobre ética e segurança da informação, o servidor pode evitar a ferramenta.'],
           [68, 62.5, 27.2, 29.3, 'A solução estrutural: orientações claras, como o guia do TCU, delimitam o que pode ser feito. Que isso aumente a adoção é uma hipótese a testar.']])

F8 = gfig(8, 'Pilar 2: o apoio vem da alta gestão, da chefia imediata e dos colegas.',
          'Três blocos de texto à esquerda e, à direita, um triângulo com Alta Gestão, Chefia Imediata e Pares em torno do círculo O Servidor.',
          [[5.5, 21.9, 44.6, 19.5, 'Transferência de aprendizagem: aplicar o que se aprende depende do suporte psicossocial (Abbad e Sallorenzo, 2001; Rozendo, 2014).'],
           [5.5, 43.6, 44.6, 22.2, 'A dinâmica do suporte: a chefia valida o esforço, e os colegas validam a cultura de aprender.'],
           [5.5, 67.7, 44.6, 19.8, 'O alerta: sem apoio ao aprendizado depois do curso, o investimento em licenças e cursos pode não se converter em uso.'],
           [54, 22, 40, 68, 'O servidor no centro de três apoios: alta gestão, chefia imediata e pares.']])

F10 = gfig(10, 'Pilar 4: segurança psicológica como o direito de experimentar.',
           'Uma caixa de areia isométrica com formas geométricas e, à direita, três itens: A Natureza Probabilística da IA, O Fator Edmondson e A Morte da Adoção.',
           [[5.4, 22, 41.8, 64.6, 'O sandbox: um espaço delimitado em que errar faz parte de aprender.'],
            [49.4, 22, 45, 19.7, 'A IA generativa é probabilística e pode errar; aprender a usá-la envolve tentar, errar e refinar.'],
            [49.4, 46, 45, 19, 'Edmondson (1999): segurança psicológica é a crença de que a equipe é segura para assumir riscos interpessoais.'],
            [49.4, 69.7, 45, 20.3, 'Se errar durante o aprendizado é punido, a experimentação tende a diminuir. A relação com a IA no setor público ainda é uma hipótese não testada.']])

F13 = gfig(13, 'O modelo de síntese: insumos organizacionais, filtro individual e dois caminhos de intenção.',
           'Diagrama com quatro insumos, Governança, Apoio, Tempo e Acesso e Segurança, que passam por um Filtro Individual (Propósito e Vínculo) e seguem por dois caminhos, Intenção de Usar e Intenção de Aprender, até a Adoção Efetiva, Segura e Sustentável.',
           [[5.8, 28.6, 16.4, 54.7, 'Os insumos da organização: governança, apoio, tempo e acesso, e segurança.'],
            [30.5, 43, 16.7, 30, 'O filtro individual: propósito e vínculo entram como variáveis secundárias, a investigar.'],
            [47.2, 28, 25.5, 24, 'Intenção de usar, com foco em eficiência e produtividade.'],
            [47.2, 56, 25.5, 17, 'Intenção de aprender, com foco em domínio e riscos: o caminho que a literatura quase não mede.'],
            [72, 31, 24.3, 47, 'A adoção efetiva, segura e sustentável. O modelo é uma proposta conceitual, com hipóteses ainda não testadas.']])

F14 = gfig(14, 'Recomendações práticas do autor para gestores públicos, a partir do mapa da literatura.',
           'Quatro itens com marcas de verificação: separe as métricas de avaliação, institucionalize o tempo protegido, crie um sandbox cultural e comunique as regras básicas hoje.',
           [[10.9, 20.8, 78, 17, '1. Separar as métricas: acesso à ferramenta é diferente de aprendizagem real e de aplicação no dia a dia.'],
            [10.9, 40.8, 78, 16.5, '2. Institucionalizar o tempo protegido: formalizar a liberação de carga de trabalho para estudar.'],
            [10.9, 59.9, 78, 16.9, '3. Criar um sandbox cultural: tratar o erro de testes com IA como aprendizagem, e não como infração.'],
            [10.9, 79.4, 78, 17, '4. Comunicar as regras básicas já: limites claros sobre dados e ética, sem esperar a regulação perfeita.']])

F15 = gfig(15, 'O sucesso da IA no setor público não é um desafio de software.',
           'Slide final sobre fundo azul-escuro com a frase O sucesso da IA no setor público não é um desafio de software, e o subtítulo sobre arquitetura organizacional.',
           [[6, 13, 88, 48, 'O sucesso da IA no setor público não é um desafio de software.'],
            [6, 70, 88, 16, 'É um desafio de arquitetura organizacional: oferecer a ferramenta é o início, e construir a intenção de aprender é a transformação.']])

sections = [
    section('01', 'norma', 'A expectativa normativa e o descompasso',
            'Os documentos orientadores tratam a capacitação como condição da adoção, mas a formação real não acompanha.',
            [F2, F3],
            [acc('O que os documentos orientadores dizem',
                 ['Em uma análise de 200 casos de uso em 11 funções centrais de governo, a OCDE (2025) constatou que a IA é prioridade para a maioria dos governos, mas que os esforços ainda não são sistemáticos, e que todos os casos podem trazer algum tipo de risco quando não são desenhados e usados de forma confiável.',
                  'O Plano Brasileiro de Inteligência Artificial afirma que os servidores precisam ser capacitados de forma contínua. A Matriz de Competências em IA propõe perfis e níveis de proficiência para orientar trilhas de aprendizagem. O guia do Tribunal de Contas da União orienta que decisões automatizadas por IA generativa não sejam adotadas sem revisão humana. A OCDE (2026) acrescenta que a maior parte dos servidores precisará de alfabetização básica em IA.']),
             acc('Sinais de que a formação não acompanha',
                 ['A OCDE (2019) identificou, no setor público federal brasileiro, lacunas percebidas em competências de inovação e indícios de que o acesso a treinamento para desenvolvê-las era desconhecido ou inexistente.',
                  'Um levantamento com servidores e empregados públicos registrou percepção de ganhos de eficiência e, ao mesmo tempo, falta de preparo para as mudanças digitais, embora os autores advirtam que a amostra é pequena e os resultados não são generalizáveis (Toledo e Mendonça, 2023). Um estudo documental sobre 311 documentos governamentais mostrou crescimento das ações de IA, lideradas pelo Poder Executivo (61%), seguido do Legislativo (21%) e do Judiciário (18%) (Alcântara, Oliveira e Moraes, 2026).']),
             acc('Pouca evidência organizada sobre o servidor',
                 ['Em uma pesquisa com 12.562 servidores do Cazaquistão, cerca de nove em cada dez não usavam IA ou nunca a tinham tentado. A posição de gestão e o acesso a ferramentas digitais associaram-se ao uso, e o maior tempo de serviço, negativamente (Daueshova et al., 2026). Em 129 servidores marroquinos, os mais jovens eram mais abertos à IA e mais de 40% apontaram a falta de competências digitais como barreira (Barodi e Lalaoui, 2025).',
                  'Essas evidências estão dispersas entre administração pública, sistemas de informação, gestão de pessoas e educação corporativa, e usam termos diferentes, como adoção, aceitação, intenção e prontidão.'])]),

    section('02', 'desfecho', 'Usar não é o mesmo que aprender',
            'A literatura mede sobretudo a intenção de usar. A de aprender quase não aparece.',
            [F4, F5],
            [acc('Quatro desfechos relacionados, mas distintos',
                 ['A revisão trata intenção, adoção, uso e aprendizagem como desfechos relacionados e distintos. Quem pretende usar uma ferramenta não necessariamente pretende estudá-la, e as condições que favorecem uma e outra podem diferir.',
                  'A teoria unificada de aceitação e uso de tecnologia (UTAUT) reúne expectativa de desempenho, expectativa de esforço, influência social e condições facilitadoras como determinantes da intenção e do uso (Venkatesh et al., 2003).']),
             acc('O ponto cego do conjunto de estudos',
                 ['Na síntese preliminar de 50 estudos de 2020 a 2026, predominam os desenhos de corte transversal (survey) e os referenciais TOE (16 estudos), TAM (11) e UTAUT (9). O desfecho mais frequente é a intenção ou a disposição de adotar IA, seguida do uso declarado e da prontidão.',
                  'Entre os estudos com servidores, nenhum tem a intenção de aprender IA como desfecho principal. A aprendizagem aparece como necessidade de treinamento, como barreira ou como efeito de um curso.'],
                 'A frase final do slide, de que a organização estaria medindo a métrica errada, é uma leitura do autor a partir do mapa, e não um resultado da revisão.')]),

    section('03', 'pilares', 'Quatro pilares e o que a literatura indica',
            'O que os estudos mostram sobre regras, apoio, tempo e acesso, e segurança para experimentar.',
            [F6, F7, F8, barras, F10],
            [acc('Clareza das regras e governança',
                 ['Servidores municipais finlandeses deram mais valor à orientação ética e de segurança da informação, e a falta de diretrizes organizacionais teve média de 2,2 em 3 entre as barreiras de servidores que não usavam IA (Pulkkinen, 2026a, 2026b). Especialistas suíços incluíram diretrizes claras entre as medidas prioritárias (Stübi, 2026).',
                  'Incerteza jurídica, vazio de responsabilização e regulação ambígua aparecem como barreiras na Áustria e no Vietnã (Eibl et al., 2026; Duy et al., 2026). O apoio regulatório foi significativo em estudos do Kuwait e de municípios europeus (Al Wael et al., 2023; Mikalef et al., 2021, lidos pelo resumo).']),
             acc('Apoio da chefia, da liderança e dos colegas',
                 ['Servidores finlandeses em cargos de supervisão usaram mais IA (70% contra 40%), e a falta de apoio dos pares teve média de 2,0 em 3 entre as barreiras (Pulkkinen, 2026a). No Cazaquistão, o cargo de gestão associou-se ao uso (Daueshova et al., 2026), e na Suíça dar o exemplo foi uma das medidas priorizadas (Stübi, 2026).',
                  'Os resultados não são uniformes: o apoio da liderança não foi significativo em um estudo dos Emirados Árabes (Al-Kaabi et al., 2025), e a influência social foi ambivalente em Dubai (Blaique et al., 2026), ambos lidos pelo resumo.'],
                 'Na literatura brasileira de treinamento, o suporte psicossocial é preditor da transferência da aprendizagem para o trabalho (Abbad e Sallorenzo, 2001; Rozendo, 2014).'),
             acc('Acesso, treinamento e o fator tempo',
                 ['Entre servidores finlandeses que não usavam IA, conhecimento limitado das ferramentas e treinamento inadequado foram as maiores barreiras (2,4 em 3), e o pouco tempo para aprender teve média de 1,9 (Pulkkinen, 2026a). Especialistas suíços priorizaram garantir acesso e treinamento, e a coerção ficou em último lugar (Stübi, 2026). No Cazaquistão, o acesso a ferramentas digitais teve associação positiva pequena com o uso, e o modelo explicou pouco da adoção (Daueshova et al., 2026).',
                  'O tempo aparece como um item entre outros: falta de tempo e orçamento para treinamento na Áustria (Eibl et al., 2026) e restrição de tempo e recursos de 4,2 a 5,0 em 5 em dois municípios catarinenses (Lima et al., 2026). A carga de trabalho percebida inibiu a intenção na China (Yao et al., 2026, lido pelo resumo).'],
                 'O tempo protegido é citado com frequência e raramente medido como fator da intenção de aprender, o que o torna uma variável a investigar.'),
             acc('Segurança para experimentar',
                 ['Nenhum dos 50 estudos mediu a segurança psicológica de equipe (Edmondson, 1999; Ramalho e Porto, 2021) como fator da intenção de usar ou aprender IA. Há sinais indiretos: experimentação informal e dúvida sobre quem responde por erros (Duy et al., 2026) e apoio organizacional que amortece o risco percebido (Nguyen-Duy et al., 2026).',
                  'No Chile, intervenções tecnoculturais elevaram a segurança psicológica e reduziram o tecnoestresse, com efeito maior no setor público, mas o desfecho não é a intenção de uso (Contreras Flores, 2025).'],
                 'A relação entre segurança psicológica e disposição de aprender IA no serviço público permanece uma hipótese plausível e não testada.'),
             acc('Fatores individuais e resultados mistos',
                 ['Utilidade percebida e confiança em IA são os preditores individuais mais recorrentes. Cargo de gestão, idade e tempo de serviço também aparecem associados ao uso ou à abertura. No Cazaquistão, o poder explicativo do modelo de adoção foi baixo, de modo que variáveis não medidas pesam.',
                  'Os desenhos são em sua maioria transversais, o que limita a leitura de causalidade, e para 37 dos 50 estudos a extração se baseou apenas no resumo.'])]),

    section('04', 'metodo', 'Como a revisão foi feita',
            'Uma revisão de escopo, ainda preliminar, com busca exploratória em plataforma de IA.',
            [funil],
            [acc('Pergunta e critérios',
                 ['A pergunta foi estruturada em População, Conceito e Contexto: servidores, empregados e gestores públicos de qualquer vínculo; fatores organizacionais associados à intenção, à adoção, ao uso ou à aprendizagem de IA, incluindo IA generativa; e a administração pública, em qualquer nível de governo e país.',
                  'Foram considerados estudos empíricos, revisões e estudos de caso, em português, inglês e espanhol, a partir de 2018. A condução segue o Joanna Briggs Institute (Peters et al., 2020), com relato conforme o PRISMA-ScR (Tricco et al., 2018).']),
             acc('A busca exploratória',
                 ['Em 10 de novembro de 2026 foram feitas oito buscas na plataforma Consensus, que ordena e sintetiza artigos por IA. Foram carregados até 40 resultados por busca e registrados título, ano, periódico e a conclusão exibida. Os DOIs ausentes foram procurados por título no Crossref e aceitos quando título, ano e primeiro autor conferiam.',
                  'Como a ordenação e as sínteses da plataforma podem variar entre consultas, essa etapa complementa as bases tradicionais, e não as substitui.']),
             acc('O que ainda falta',
                 ['A triagem por título e resumo e a extração preliminar foram feitas por um revisor assistido por IA, com leitura de texto completo apenas dos estudos de acesso aberto legíveis (13 de 50). A triagem definitiva, a extração nos textos completos e a conferência por um segundo revisor ainda serão feitas.',
                  'Scopus, Web of Science, SciELO, Spell e BDTD ainda não foram pesquisadas, e o protocolo será registrado em plataforma aberta antes da busca definitiva.'],
                 'Os números desta página descrevem uma síntese preliminar, e não a revisão final.')]),

    section('05', 'modelo', 'Do mapa ao modelo conceitual',
            'Insumos organizacionais, filtro individual e dois caminhos de intenção, em forma de hipóteses.',
            [F13],
            [acc('O modelo e as hipóteses',
                 ['A síntese sustenta um modelo em que a intenção de aprender e usar IA depende de condições organizacionais (apoio de chefias e colegas, tempo protegido, acesso a ferramentas e cursos, segurança para experimentar e clareza das regras), de fatores individuais recorrentes (utilidade percebida e confiança) e, como variáveis secundárias, do propósito e do vínculo.',
                  'Hipóteses candidatas, a testar com servidores do Executivo de Goiás: (H1) o apoio da chefia e dos colegas se associa positivamente à intenção de aprender IA; (H2) o tempo protegido se associa positivamente e a carga de trabalho percebida, negativamente; (H3) o acesso a ferramentas autorizadas e a cursos ligados às tarefas se associa positivamente; (H4) a segurança para experimentar se associa positivamente; (H5) a clareza das regras se associa positivamente; (H6) o propósito e o tipo de vínculo moderam essas relações, de forma exploratória.'],
                 'As direções de H2 e H4 se apoiam em poucos estudos e devem ser tratadas como exploratórias.'),
             acc('Propósito e vínculo',
                 ['A motivação para o serviço público aparece em poucos estudos e em papel secundário: reforçou o efeito da liderança digital sobre o desempenho proativo (Song et al., 2026), teve efeito intrínseco maior que o extrínseco sobre o desempenho percebido com IA generativa (Choi et al., 2025) e associou-se ao empoderamento no trabalho com IA (Noor et al., 2026). Nenhum desses estudos tem a intenção de usar ou aprender como desfecho principal.',
                  'Nenhum resumo lido distingue servidores efetivos, comissionados e temporários. As variáveis funcionais que aparecem são cargo de gestão, tempo de serviço e idade (Daueshova et al., 2026), e a natureza pública ou privada do empregador (Revillod, 2025). A literatura geral sobre estabilidade sugere que ela não define a motivação (Machado et al., 2021; Espínola e Cruz, 2022).'],
                 'A motivação para o serviço público mede uma disposição geral e não deve ser lida como justificativa para sobrecarga de trabalho.'),
             acc('Produção brasileira e lacunas',
                 ['Na busca exploratória, dois registros têm foco no Brasil. Lima et al. (2026) estudaram modelos de treinamento adaptativo com IA para servidores municipais de Santa Catarina, com entrevistas e escala Likert, e apontam necessidades como aproximar teoria e prática e dar apoio depois do treinamento. Costa et al. (2026) estudaram servidores da Receita Federal diante de um novo sistema, sem foco em IA.',
                  'Lacunas: quase não há estudos com a intenção de aprender IA como desfecho; o tempo protegido aparece como item de barreira, e não como fator medido; a segurança psicológica quase não é medida; o vínculo não é distinguido; o propósito aparece como moderador, e não como fator da intenção; predominam estudos transversais de países asiáticos e europeus; e a produção brasileira é mínima, o que ainda depende da busca em SciELO, Spell e BDTD.'])]),

    section('06', 'limites', 'Limitações e próximos passos',
            'O que a síntese preliminar permite afirmar, e o que ainda depende de leitura e de novas buscas.',
            [],
            [acc('Limitações',
                 ['Dos 50 estudos da síntese, 13 foram lidos em texto completo e 37 foram extraídos de resumos. A direção das associações e as amostras desses 37 devem ser conferidas nos artigos, e dez registros sem resumo ficaram pendentes.',
                  'A busca recuperou, em sete das oito consultas, só os 40 primeiros resultados, e a plataforma ordena e sintetiza por IA, de modo que os resultados não são plenamente reprodutíveis. Os metadados foram incompletos e a cobertura de periódicos brasileiros é incerta.',
                  'A revisão de escopo não estima efeitos nem avalia a qualidade dos estudos. O recorte de idiomas e de período (2018 em diante) exclui outros trabalhos.']),
             acc('Próximos passos',
                 ['Pesquisar as demais bases, ler os textos completos, concluir a extração com conferência por um segundo revisor, registrar o protocolo e atualizar os resultados.',
                  'Em seguida, desenhar o estudo empírico com servidores do Executivo de Goiás, com questionário anônimo, que meça a intenção de aprender separada da de usar e inclua tempo, segurança para experimentar, propósito e vínculo. Ele depende de aprovação do comitê de ética e de adaptação dos instrumentos validados no Brasil.'])]),

    section('07', 'recomendacoes', 'Do mapa à prática',
            'O que o mapa sugere para quem forma servidores.',
            [F14],
            [acc('O que a síntese sugere',
                 ['Oferecer cursos e ferramentas é condição necessária, mas não suficiente. Apoio de chefias, tempo e regras claras merecem o mesmo cuidado, e vale medir a aprendizagem e a intenção de aprender separadamente do acesso e do uso.'],
                 'As quatro recomendações da imagem são propostas do autor a partir do mapa da literatura. Elas não foram testadas.')]),
]

closing = ('<section aria-labelledby="sintese" class="mt-16 rounded-2xl border bg-secondary/50 p-7"><h2 id="sintese" class="text-2xl font-semibold">A síntese</h2>'
           '<p class="mt-3 leading-relaxed text-muted-foreground">A adoção de IA no serviço público depende de condições organizacionais que a instituição pode alterar. O mapa preliminar indica o que a literatura já mostra e onde ela é silenciosa, em especial sobre a intenção de aprender, o tempo protegido, a segurança para experimentar, o vínculo e a produção brasileira.</p>'
           + F15 +
           '<p class="mt-6 rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] italic leading-relaxed text-accent-foreground">Oferecer a ferramenta é apenas o início; construir a intenção de aprender é a verdadeira transformação.</p></section>')


def build():
    stat = lambda n, l: ('<div><dt class="font-display text-2xl text-ochre" data-count data-from="0" data-to="%s">%s</dt>'
                         '<dd class="mt-1 text-xs uppercase tracking-wide text-primary-foreground/70">%s</dd></div>' % (n, n, l))
    header = ('<header class="relative overflow-hidden text-primary-foreground" style="background-image:var(--gradient-deep)">'
              '<div class="surface-paper absolute inset-0 opacity-30" aria-hidden="true"></div>'
              '<div class="relative mx-auto max-w-3xl px-6 py-20 sm:py-28">'
              '<p class="text-xs font-semibold uppercase tracking-[0.2em] text-ochre">Revisão de escopo · Inteligência artificial · Servidores públicos</p>'
              '<h1 class="mt-6 text-4xl leading-[1.1] font-semibold sm:text-5xl">A arquitetura da <span class="text-gradient-warm">adoção de IA</span> no setor público</h1>'
              '<p class="mt-5 text-lg leading-relaxed text-primary-foreground/80">Fatores organizacionais associados à intenção de servidores públicos de aprender e usar inteligência artificial: uma revisão de escopo.</p>'
              '<p class="mt-4 text-base leading-relaxed text-primary-foreground/70">Os fatores organizacionais que transformam a disponibilidade tecnológica em intenção de aprender e usar.</p>'
              '<p class="mt-8 text-sm text-primary-foreground/70">Carlos Hernane de Oliveira</p>'
              '<div class="mt-6" style="display:flex;flex-wrap:wrap;gap:12px"><a href="../assets/pdf/%s" target="_blank" rel="noopener noreferrer" '
              'class="inline-flex items-center gap-2 rounded-full bg-ochre px-6 py-3 text-sm font-semibold text-ochre-foreground shadow-lift transition-transform hover:-translate-y-0.5">'
              % PDF + BOOK + 'Leia o Artigo na Íntegra</a></div>'
              '<p class="mt-3 max-w-md text-sm leading-relaxed text-primary-foreground/70">Abre o PDF completo do artigo em uma nova aba, para leitura direta no navegador.</p>'
              '<dl class="reveal mt-10 grid grid-cols-2 gap-6 sm:grid-cols-4">'
              + stat('50', 'estudos na síntese') + stat('13', 'lidos em texto completo') + stat('5', 'fatores organizacionais') + stat('25', 'países, no mínimo')
              + '</dl></div></header>')
    intro = ('<section aria-labelledby="resumo-ia"><h2 id="resumo-ia" class="text-2xl font-semibold">Do que trata o artigo</h2>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">A adoção da inteligência artificial na administração pública exige servidores que queiram aprender e usar essas ferramentas, mas pouco se sabe sobre quais condições organizacionais favorecem essa disposição. O estudo mapeia a literatura sobre os fatores organizacionais associados à intenção, à adoção e à aprendizagem de IA por servidores públicos, com atenção ao propósito, ao tipo de vínculo e à produção brasileira.</p>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">Trata-se de uma revisão de escopo, conduzida conforme o Joanna Briggs Institute e relatada segundo o PRISMA-ScR. Na síntese preliminar, 50 estudos de 2020 a 2026 mostraram que regras claras, acesso a ferramentas, treinamento e apoio de chefias e pares costumam se associar ao uso e à intenção, com resultados mistos. Quase nenhum estudo tem a intenção de aprender IA como desfecho, mede o tempo protegido ou a segurança para experimentar, distingue o tipo de vínculo ou trata o propósito como fator, e a produção brasileira é mínima.</p>'
             '<p class="mt-4 rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] leading-relaxed text-accent-foreground">Esta é uma síntese preliminar: 13 dos 50 estudos foram lidos em texto completo e os demais por resumo, e as buscas em Scopus, Web of Science, SciELO, Spell e BDTD ainda não foram feitas.</p>'
             + F1 + '</section>'
             '<section aria-labelledby="objetivos-ia" class="mt-10 rounded-2xl border bg-secondary/50 p-7"><h2 id="objetivos-ia" class="text-2xl font-semibold">Pergunta e objetivos</h2>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Pergunta de pesquisa</h3><p class="mt-2 leading-relaxed text-muted-foreground">Que fatores organizacionais a literatura associa à intenção, à adoção e à aprendizagem de IA por servidores públicos, e que lacunas existem, em especial no contexto brasileiro?</p></div>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Cinco objetivos específicos</h3><ul class="mt-3 space-y-2 text-muted-foreground">'
             + ''.join('<li class="flex gap-3"><span class="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-sage"></span><span class="leading-relaxed">%s</span></li>' % t for t in [
                 'Identificar os fatores organizacionais estudados e a direção das associações.',
                 'Descrever os referenciais teóricos e a forma como os construtos foram medidos.',
                 'Verificar se os estudos consideram o propósito ou a motivação para o serviço público e o tipo de vínculo.',
                 'Identificar a produção brasileira e as lacunas em relação à internacional e aos documentos oficiais.',
                 'Propor um modelo conceitual e hipóteses para um estudo empírico posterior.'])
             + '</ul></div></section>')
    main = '<main class="mx-auto max-w-3xl px-6 py-16">' + intro + '<div class="mt-14 space-y-14">' + ''.join(sections) + '</div>' + closing + '</main>'
    footer = ('<footer class="border-t bg-card"><div class="mx-auto max-w-3xl px-6 py-10 text-sm text-muted-foreground">'
              '<p class="font-display text-base text-foreground">Fatores organizacionais associados à intenção de servidores públicos de aprender e usar inteligência artificial: uma revisão de escopo</p>'
              '<p class="mt-2">Carlos Hernane de Oliveira.</p>'
              '<p class="mt-2">Aspectos éticos: esta etapa usou apenas literatura publicada e documentos oficiais, sem participação de seres humanos; o estudo empírico previsto dependerá de apreciação por comitê de ética. A triagem e a extração preliminares foram assistidas por inteligência artificial e serão conferidas por revisor humano.</p>'
              '<p class="mt-4">Palavras-chave: inteligência artificial; servidores públicos; revisão de escopo; condições organizacionais; aprendizagem no trabalho.</p></div></footer>')
    page = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>'
            '<title>A arquitetura da adoção de IA no setor público</title>'
            '<meta name="description" content="Revisão de escopo sobre os fatores organizacionais associados à intenção de servidores públicos de aprender e usar inteligência artificial: regras claras, apoio, tempo, acesso e segurança para experimentar."/>'
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
