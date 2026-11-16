"""Artigo 08: Da governança à interface: requisitos de UX para uma IA transparente e contestável em serviços públicos.

Gera docs/governanca-ux-ia/index.html a partir do texto do artigo e dos 14 slides da apresentação
(src/orig/governanca-ux-ia/img). As imagens ganham a galeria animada de build/mmdi.css e build/mmdi.js.
"""
import json, os, shutil, sys
sys.path.insert(0, 'build')
import shell
from artigo4 import acc, e, BOOK

S = 'docs'
SLUG = 'governanca-ux-ia'
SRC = 'src/orig/governanca-ux-ia'
PDF = 'Da_governanca_a_interface_UX_IA_servicos_publicos.pdf'
SEQ = {}


def gfig(n, title, alt, tour):
    """Imagem animada: slide n da apresentação, com roteiro de regiões em destaque (x, y, largura, altura em %, texto)."""
    SEQ[n] = len(SEQ) + 1
    img = 'ux-slide-%02d.jpg' % n
    return ('<figure class="gfig mt-6 overflow-hidden rounded-xl border bg-card shadow-[var(--shadow-soft)]" data-tour=\'[]\'>'
            '<div class="gfig-stage"><div class="gfig-zoom">'
            '<img class="gfig-img" src="../assets/img/%s" width="1376" height="768" loading="lazy" alt="%s"/>'
            '<div class="gfig-fx" aria-hidden="true"><i class="gfig-sweep"></i><i class="gfig-scan"></i><i class="gfig-glare"></i><i class="gfig-wipe"></i></div>'
            '</div></div>'
            '<figcaption class="border-t px-5 py-4 text-sm leading-relaxed text-muted-foreground">%s'
            '<span class="mt-1 block text-xs text-muted-foreground/80">Imagem %d da apresentação do artigo. '
            '<a class="underline underline-offset-2" href="../assets/img/%s" target="_blank" rel="noopener">Ver a imagem original</a></span></figcaption></figure>'
            % (img, e(alt), e(title, quote=False), SEQ[n], img))


def section(num, sid, title, sub, blocks, accs):
    return ('<section id="%s" aria-labelledby="%s-titulo"><div class="flex items-baseline gap-4">'
            '<span class="font-display text-3xl text-ochre">%s</span><div><h2 id="%s-titulo" class="text-2xl font-semibold">%s</h2>'
            '<p class="mt-1 text-sm text-muted-foreground">%s</p></div></div>%s<div class="mt-6 space-y-3">%s</div></section>'
            % (sid, sid, num, sid, e(title, quote=False), e(sub, quote=False), ''.join(blocks), ''.join(accs)))


def table(caption, head, rows, source, widths=None):
    th = 'style="padding:8px 10px;text-align:left;border-bottom:2px solid var(--border);font-weight:600;white-space:nowrap"'
    td = 'style="padding:8px 10px;border-bottom:1px solid var(--border);vertical-align:top"'
    hh = ''.join('<th %s>%s</th>' % (th, e(h)) for h in head)
    bb = ''.join('<tr>' + ''.join('<td %s>%s</td>' % (td, e(c)) for c in r) + '</tr>' for r in rows)
    return ('<figure class="mt-6 rounded-xl border bg-card p-5 shadow-[var(--shadow-soft)]"><p class="text-sm font-medium text-foreground">%s</p>'
            '<div style="overflow-x:auto;margin-top:12px"><table style="width:100%%;border-collapse:collapse;font-size:13.5px;line-height:1.45;min-width:560px">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="mt-3 text-xs text-muted-foreground">%s</p></figure>' % (e(caption), hh, bb, e(source)))


# ---------- figuras (slides) ----------
F1 = gfig(1, 'Da governança à interface: o cidadão no controle da IA, com requisitos de UX para serviços públicos transparentes e contestáveis (caso Programa Goiás Cidadão).',
          'Slide de abertura: uma mão toca um celular de onde saem balões de conversa com as palavras Transparência, Controle, Cidadão, Interação e IA Governamental, sobre feixes de fibra óptica azul.',
          [[9, 6, 82, 25, 'O título: da governança à interface, com o cidadão no controle da IA em serviços públicos transparentes e contestáveis.'],
           [48, 32, 38, 46, 'Os balões da conversa: transparência, controle, cidadão, interação e IA governamental são os temas que o estudo traduz em requisitos de tela.'],
           [0, 55, 45, 40, 'Os feixes de dados que chegam ao celular: o que acontece nos sistemas precisa se tornar algo que o cidadão enxerga e usa.']])

F2 = gfig(2, 'O paradoxo da IA no setor público: uma interação tecnicamente impecável pode ser totalmente incompreensível para o cidadão.',
          'À esquerda, uma sala de servidores com um braço mecânico que carimba Processado/Aprovado; à direita, um cidadão confuso com o celular e pontos de interrogação.',
          [[2.5, 9, 94, 14, 'O paradoxo: a interação pode ser impecável para o sistema e incompreensível para o cidadão, que no serviço público não escolhe outro prestador.'],
           [0, 25, 50, 72, 'O lado do sistema: tudo foi processado e aprovado, e do ponto de vista técnico não há erro.'],
           [46, 28, 10, 60, 'A ruptura entre os dois lados: é aqui que o estudo propõe construir uma ponte.'],
           [52, 25, 47, 72, 'O lado do cidadão: sem entender o resultado, ele pode perder acesso a direitos e benefícios essenciais.']])

F3 = gfig(3, 'Fundações antes da proatividade: a IA e a proatividade só operam sobre dados maduros e governados.',
          'Um anel laranja chamado Gate de Maturidade envolve o Canal Único, a Identificação Única, os 12 Momentos de Vida e a Base Única; do lado de fora, um braço robótico representa a IA Aplicada.',
          [[2.5, 3, 93, 17, 'O horizonte de 48 meses do Programa Goiás Cidadão: eliminar silos primeiro, e só depois aplicar IA e proatividade.'],
           [24, 24, 38, 8, 'A etapa formal de liberação (gate de maturidade): exige finalidade e base legal aprovadas, controles de acesso e auditoria, teste e supervisão.'],
           [33, 44, 16, 24, 'O Canal Único, no centro: aplicativo e número oficial de WhatsApp, sem eliminar o atendimento presencial.'],
           [82, 38, 15, 38, 'A IA aplicada fica do lado de fora do anel, e só entra depois que as fundações de dados passam pela etapa de liberação.']])

F4 = gfig(4, 'O abismo entre dois mundos: manuais de ética dizem o que proteger, mas não onde fica o botão nem como escrever a mensagem.',
          'Pilhas de documentos, livros e servidores rotulados Governança, Ética e LGPD, separados por um abismo de um celular na outra margem, ligados por uma ponte chamada Matriz de UX para IA.',
          [[2.5, 3, 94, 18, 'Ter manuais e frameworks diz o que deve ser protegido, mas não indica onde o botão deve ficar ou como a mensagem deve ser escrita.'],
           [0, 26, 36, 52, 'O mundo da governança: documentos, normas, ética e a LGPD, que descrevem controles de retaguarda.'],
           [34, 32, 42, 40, 'A ponte: a matriz de UX para IA traduz os controles de governança (back-end) em requisitos de interface (front-end).'],
           [74, 36, 22, 48, 'O mundo do cidadão: o celular, onde a governança precisa se tornar perceptível e utilizável.']])

F5 = gfig(5, 'A matriz de UX para IA: 13 requisitos em quatro dimensões, que funcionam como etapa de liberação antes de qualquer agente de IA entrar em produção.',
          'Planta técnica de um celular ao centro, com quatro dimensões nos cantos: Utilidade (resolutividade e continuidade), Transparência (explicabilidade e origem), Confiança (supervisão e erros) e Controle (recusa e contestação).',
          [[2.5, 3, 94, 17, 'Treze requisitos organizados em quatro dimensões, propostos como critério de liberação antes de a IA entrar em produção.'],
           [5, 25, 32, 14, 'Utilidade: resolutividade e continuidade. A interação conclui a tarefa do cidadão.'],
           [68, 25, 30, 14, 'Transparência: explicabilidade e origem. A interface comunica o uso da IA, seus limites e a origem dos dados.'],
           [5, 63, 28, 14, 'Confiança: supervisão e tratamento de erros. A confiança é calibrada, e não cega.'],
           [69, 63, 26, 14, 'Controle: recusa e contestação. O cidadão pode corrigir, recusar e contestar.']])

F6 = gfig(6, 'Utilidade: a IA não deve frustrar o usuário pedindo o que o Estado já sabe.',
          'Dois celulares lado a lado. No da esquerda, o assistente pede para digitar o endereço completo novamente; no da direita, confirma o endereço mais recente atualizado na Saneago e pergunta se pode seguir com ele.',
          [[2.5, 3, 94, 13, 'A IA não deve frustrar o usuário pedindo o que o Estado já sabe.'],
           [2.5, 19, 44, 19, 'A governança exige qualidade dos dados e regras de precedência.'],
           [13, 42, 28, 56, 'Sem isso: o assistente pede de novo o endereço completo e o cidadão repete informação.'],
           [52.5, 19, 44, 19, 'A UX entrega: reaproveita dados já informados, usa a fonte oficial correta e admite incerteza.'],
           [59, 42, 28, 56, 'Com isso: o assistente confirma o dado mais recente e pergunta se pode seguir com ele.']])

F7 = gfig(7, 'Transparência: o cidadão tem o direito de saber com quem, e com quais dados, está falando.',
          'Um celular inclinado mostra a mensagem Estou sugerindo a renovação baseado no vencimento da sua CNH (Fonte: Detran/GO), com a etiqueta Aviso de IA, e dois quadros de texto sobre governança e UX.',
          [[2.5, 3, 94, 13, 'O cidadão tem o direito de saber com quem, e com quais dados, está falando.'],
           [2.5, 19, 47, 19, 'A governança exige finalidade explícita, explicabilidade apropriada e linhagem do dado.'],
           [51, 19, 46, 19, 'Na UX, o assistente se identifica como máquina, usa linguagem simples e explica de qual base oficial veio a informação.'],
           [12, 42, 46, 34, 'O aviso de IA no ponto de uso: a mensagem proativa diz por que foi enviada e qual é a fonte do dado.'],
           [70, 62, 27, 26, 'A origem do dado, com a base oficial e a data de atualização, visível para o cidadão.']])

F8 = gfig(8, 'Confiança: a confiança na automação não deve ser cega, e sim calibrada. O cidadão nunca deve se sentir preso em um ciclo infinito.',
          'Um robô de IA verde passa um bastão luminoso a uma pessoa laranja, sobre o botão Falar com Atendente, com dois quadros de texto: o que a governança exige e o que a UX entrega.',
          [[2.5, 3, 94, 15, 'Confiança calibrada, e não cega: o cidadão nunca deve se sentir preso em um ciclo infinito de IA.'],
           [10, 21, 76, 40, 'A passagem do bastão: a IA entrega a conversa a uma pessoa, sem que o cidadão precise recomeçar.'],
           [29, 63, 42, 14, 'O botão Falar com Atendente, disponível em qualquer etapa da conversa.'],
           [2.5, 78, 47, 18, 'A governança exige supervisão humana e plano de contingência.'],
           [51, 78, 46, 18, 'A UX entrega o escalonamento imediato, com todo o contexto transferido, e mensagens de erro focadas em resolução.']])

F9 = gfig(9, 'Controle: o poder de dizer não. O cidadão é o protagonista da jornada.',
          'Um celular com o interruptor Permitir sugestões proativas desligado e um botão laranja Contestar este resultado, ao lado de dois quadros de texto sobre governança e UX.',
          [[2.5, 3, 94, 11, 'O cidadão é o protagonista absoluto da jornada.'],
           [2.5, 19, 47, 20, 'A governança exige gestão de preferências e consentimento, quando aplicável.'],
           [2.5, 40, 47, 22, 'Na UX, a recusa de usos proativos (em inglês, opt-out) é simples e reversível, no próprio canal, e há um caminho visível para contestar resultados algorítmicos.'],
           [55, 44, 40, 14, 'O interruptor Permitir sugestões proativas: recusar é um gesto simples, no mesmo canal da mensagem.'],
           [49, 62, 49, 20, 'O botão Contestar este resultado: o caminho para contestar fica visível, e não escondido em um menu.']])

F10 = gfig(10, 'O ponto cego legal: a LGPD garante o direito de contestar decisões automatizadas, mas a exigência de revisão por pessoa natural foi vetada.',
           'Um fluxo com um martelo de juiz e o rótulo Art. 20 LGPD levando a Direito de Contestar; o caminho Revisão por Humano está riscado com um X vermelho, e um caminho verde, a partir de Decisão de Governança do Estado, leva a Revisão Humana Garantida.',
           [[2.5, 3, 94, 23, 'O art. 20 da LGPD garante o direito de contestar, mas o dispositivo que exigia revisão por pessoa natural foi vetado. Garantir a revisão humana é uma escolha de governança, e não uma obrigação legal.'],
            [5, 26, 26, 28, 'O art. 20 da LGPD: direito de pedir revisão de decisões tomadas unicamente com base em tratamento automatizado.'],
            [36, 30, 22, 24, 'O direito de contestar existe na lei.'],
            [53, 37, 26, 32, 'A revisão por pessoa natural, riscada: o dispositivo foi vetado, e o veto foi mantido pelo Congresso em 2019.'],
            [5, 60, 13, 35, 'A decisão de governança do Estado: quem define em quais casos haverá revisão humana é o próprio programa.'],
            [71, 63, 26, 25, 'O caminho verde: a revisão humana garantida por escolha de governança, ao menos nas decisões de impacto relevante.']])

F11 = gfig(11, 'O iceberg das métricas: a satisfação geral é a ponta visível, e a compreensão e o controle ficam sob a água.',
           'Um iceberg com a nota 7,4 de satisfação geral na ponta e, submersos, 404 comentários negativos (29,5%), taxa de escalonamento (invisível), compreensão do uso de dados (não medido) e tentativas de fraude ou golpe (não monitorado). À direita, o texto A Colisão com a Realidade (Linha de Base).',
           [[38, 9, 22, 12, 'A ponta do iceberg: a nota média de satisfação, cerca de 7,4, é o que o painel mostra.'],
            [18, 35, 34, 58, 'Sob a água: os comentários negativos (29,5%) e o que o painel não mede, como o escalonamento, a compreensão do uso de dados e as tentativas de golpe.'],
            [67, 6, 31, 24, 'A colisão com a realidade: a linha de base do Canal Único.'],
            [67, 32, 30, 42, 'Em 63.282 atendimentos via WhatsApp, a métrica dominante é a satisfação, que pode dar uma falsa sensação de segurança e não mede compreensão.']])

F12 = gfig(12, 'Matriz de contraste: seis dos 13 requisitos não têm dado de medição no painel atual. Satisfação não é compreensão.',
           'Dois quadros ligados por feixes de luz: Estado Atual (a ilusão), com nota de 1 a 10, comentário e avaliação da entrega; e Estado Futuro (para IA), com taxa de recusa, compreensão do aviso de IA, uso da consulta Meus Dados e tempo para resolução de divergências.',
           [[2.5, 3, 94, 21, 'Seis dos 13 requisitos da matriz não têm nenhum dado no painel atual. Para operar IA com segurança, satisfação não é compreensão.'],
            [4, 28, 34, 64, 'O estado atual: nota de 0 a 10, comentário e avaliação da entrega do serviço. Mede a satisfação.'],
            [38, 42, 24, 40, 'O salto de medição: dos indicadores de satisfação para indicadores de compreensão e de controle.'],
            [63, 28, 34, 64, 'O estado futuro, para a IA: taxa de recusa, compreensão do aviso de IA, uso da consulta Meus Dados e tempo para resolução de divergências.']])

F13 = gfig(13, 'Recomendações e próximos passos: critérios de UX como etapa de liberação, jornada de contestação, novos indicadores e proteção do canal.',
           'Quatro itens com marcas de verificação: Critérios como Gate, Jornada de Contestação, Evolução dos KPIs e Proteção do Canal.',
           [[9, 3, 82, 13, 'Quatro recomendações para o programa, a partir da matriz e das lacunas encontradas.'],
            [10, 21, 80, 17, 'Critérios de UX na etapa de liberação: inserir os 13 requisitos como trava obrigatória antes de lançar qualquer onda de IA.'],
            [10, 40, 80, 17, 'Jornada de contestação: protocolo, prazo e regra clara sobre a revisão humana.'],
            [10, 59, 80, 17, 'Evolução dos indicadores: medir compreensão e controle, independentemente da satisfação.'],
            [10, 78, 80, 18, 'Proteção do canal: padrões rígidos para que o cidadão reconheça o WhatsApp oficial e não o confunda com golpes.']])

F14 = gfig(14, 'O Estado invisível, mas auditável: tornar a burocracia invisível, com respeito, transparência e controle inquestionáveis para o cidadão.',
           'Duas mãos seguram um celular com a tela verde brilhante, sobre uma grade de linhas luminosas, com o título O Estado Invisível, mas Auditável.',
           [[17, 9, 67, 12, 'O Estado invisível, mas auditável.'],
            [11, 20, 79, 17, 'O objetivo final do governo digital não é exibir a IA, e sim tornar a burocracia invisível, com respeito, transparência e controle oferecidos ao cidadão de modo inquestionável.'],
            [41, 44, 32, 52, 'Nas mãos do cidadão: o que a governança promete só vale se aparecer na tela e puder ser verificado.']])


# ---------- tabelas ----------
T1 = table('Tabela 1 – Serviços monitorados no WhatsApp: atendimentos, avaliações e notas (03/08 a 01/10/2026)',
           ['Serviço', 'Atendimentos', 'Avaliações', 'Nota do canal', 'Nota do serviço', 'Comentários negativos / válidos'],
           [['Carteira de Identidade Nacional (CIN)', '47.192', '1.878', '7,19', '7,13', '344 de 1.002 (34%)'],
            ['Renovação da CNH', '8.632', '185', '7,88', '7,86', '14 de 98 (14%)'],
            ['Ouvidoria', '6.652', '479', '8,30', '8,29', '45 de 266 (17%)'],
            ['Licenciamento ambiental', '806', '7', '6,57', '6,57', '1 de 2'],
            ['Total', '63.282', '2.549', '≈ 7,5', '≈ 7,4', '404 de 1.368 (29,5%)']],
           'Fonte: elaboração própria, com base em dados do painel de monitoramento dos serviços no WhatsApp. Notas de 0 a 10; os valores totais de notas são médias ponderadas pelo número de avaliações.')

MATRIZ = [
    ('Utilidade', [
        ('1. Resolutividade e continuidade', 'Controle de governança: resolutividade e continuidade de contexto entre canais (metas de serviço do programa).',
         'Requisito de UX: o assistente conclui a tarefa de ponta a ponta, reaproveita dados já informados e mantém o contexto ao mudar de aplicativo para WhatsApp ou atendimento presencial.'),
        ('2. Qualidade dos dados antes da IA', 'Controle de governança: qualidade e governança dos dados antes da IA (regras de precedência e reconciliação).',
         'Requisito de UX: a resposta usa a fonte oficial correta e evita informar dado desatualizado ou divergente como se fosse certo. Quando houver dúvida, a interface admite a incerteza.')]),
    ('Transparência', [
        ('3. Aviso de IA', 'Controle de governança: etapa de liberação da IA, com finalidade, base legal e avaliação de privacidade aprovadas antes do uso.',
         'Requisito de UX: aviso em linguagem simples, no início e no ponto de uso, sobre para que serve a IA e quais dados ela consulta. O aviso não fica escondido em termos de uso.'),
        ('4. Explicabilidade', 'Controle de governança: explicabilidade apropriada e controle de vieses como critério de liberação.',
         'Requisito de UX: o assistente se identifica como automatizado e declara capacidades e limites. Em elegibilidade proativa, explica por que a pessoa recebeu a mensagem e de que fonte veio o dado.'),
        ('5. Rastreabilidade do dado', 'Controle de governança: rastreabilidade do dado, com origem, data, titularidade e linhagem.',
         'Requisito de UX: o cidadão consegue ver quais dados o Estado usou, de que origem e de que data, antes de confiar na resposta ou de contestá-la.'),
        ('6. Canal oficial', 'Controle de governança: canal oficial de comunicação com o cidadão (Domicílio Digital).',
         'Requisito de UX: a interface distingue comunicação oficial de mensagem do assistente e ajuda o cidadão a reconhecer o canal autêntico, o que reduz o risco de golpes por WhatsApp.')]),
    ('Confiança', [
        ('7. Supervisão humana e escalonamento', 'Controle de governança: supervisão humana, escalonamento e plano de contingência.',
         'Requisito de UX: opção de falar com uma pessoa disponível em qualquer etapa, com transferência do contexto. A conversa não prende o cidadão em um ciclo de IA.'),
        ('8. Tratamento de erros', 'Controle de governança: monitoramento, tratamento de erros e avaliação de resultados.',
         'Requisito de UX: mensagens de erro que dizem o que aconteceu e o que fazer em seguida. Sinalizar uma resposta incorreta exige poucos toques.'),
        ('9. Minimização de dados e auditoria', 'Controle de governança: acesso por finalidade, minimização de dados e trilha de auditoria.',
         'Requisito de UX: o assistente pede somente os dados necessários à tarefa e informa o motivo. O cidadão pode consultar quem acessou seus dados e para quê.')]),
    ('Controle', [
        ('10. Recusa de usos proativos', 'Controle de governança: recusa de usos proativos e gestão de preferências e consentimento.',
         'Requisito de UX: recusar ou desativar a proatividade é simples, reversível e feito no mesmo canal da mensagem. O consentimento, quando aplicável, é específico, e não um aceite genérico.'),
        ('11. Correção e contestação', 'Controle de governança: correção e contestação pelo cidadão; LGPD, art. 20 (direito de pedir revisão de decisões automatizadas; a exigência de revisão por pessoa natural foi vetada).',
         'Requisito de UX: caminho visível para contestar um dado ou resultado, com protocolo, prazo, status e retorno por escrito no Domicílio Digital. A revisão por uma pessoa não é exigida pela LGPD e, por isso, deve ser definida pela governança do programa, com a recomendação de assegurá-la nas decisões de impacto relevante.'),
        ('12. Reconciliação de divergências', 'Controle de governança: reconciliação manual de divergências de dados.',
         'Requisito de UX: o cidadão é informado de que há análise em andamento, do que falta e do prazo, em vez de receber um erro genérico ou um “tente mais tarde”.'),
        ('13. Inclusão e acesso', 'Controle de governança: inclusão e acesso, com manutenção do atendimento presencial, acessibilidade e linguagem simples.',
         'Requisito de UX: a alternativa presencial ou assistida é explícita e não penaliza quem não usa IA. Os fluxos funcionam para pessoas com baixa literacia digital ou com deficiência.')]),
]


def matriz_acc(dim, rows):
    paras = []
    for t, g, u in rows:
        paras.append(t + '. ' + g + ' ' + u)
    return acc('Dimensão %s: %d requisito%s' % (dim.lower(), len(rows), 's' if len(rows) > 1 else ''), paras)


REFS = [
    'ALMADA, Marco. Human intervention in automated decision-making: toward the construction of contestable systems. In: INTERNATIONAL CONFERENCE ON ARTIFICIAL INTELLIGENCE AND LAW, 17., 2019, Montreal. Proceedings [...]. New York: ACM, 2019. p. 2–11. DOI 10.1145/3322640.3326699.',
    'AMERSHI, Saleema et al. Guidelines for human-AI interaction. In: CHI CONFERENCE ON HUMAN FACTORS IN COMPUTING SYSTEMS, 2019, Glasgow. Proceedings [...]. New York: ACM, 2019. DOI 10.1145/3290605.3300233.',
    'ARAÚJO, Patrick de; PEREIRA, Rute; PEREIRA, Georgia; MONTEIRO, Ingrid; ROMERO, Davi. “Isto foi útil?” Análise de instrumentos de avaliação de satisfação em aplicações de serviços públicos. In: SIMPÓSIO BRASILEIRO SOBRE FATORES HUMANOS EM SISTEMAS COMPUTACIONAIS (IHC), 20., 2021, Online. Anais [...]. Porto Alegre: SBC, 2021.',
    'BARROS, Ygor Santos; OUTÃO, Juliana Carvalho Silva do; SACRAMENTO, Carolina; FERREIRA, Simone Bacellar Leal; PIMENTEL, Mariano Gomes; SANTOS, Rodrigo Pereira dos. Avaliação de acessibilidade da plataforma Gov.br por ferramentas automatizadas. In: WORKSHOP DE COMPUTAÇÃO APLICADA EM GOVERNO ELETRÔNICO (WCGE), 12., 2024, [S. l.]. Anais [...]. Porto Alegre: SBC, 2024. p. 50–61. DOI 10.5753/wcge.2024.2282.',
    'BATISTA, Gabriely Oliveira da Silva; MONTEIRO, Mateus de Souza; SALGADO, Luciana Cardoso de Castro. Investigando chatbots governamentais: um panorama sobre a usabilidade dentro e fora do Brasil. In: WORKSHOP DE COMPUTAÇÃO APLICADA EM GOVERNO ELETRÔNICO (WCGE), 10., 2022, Niterói. Anais [...]. Porto Alegre: SBC, 2022. p. 73–84. DOI 10.5753/wcge.2022.223318.',
    'BRASIL. Decreto nº 12.198, de 24 de setembro de 2024. Institui a Estratégia Federal de Governo Digital para o período de 2024 a 2027 e a Infraestrutura Nacional de Dados. Brasília, DF: Presidência da República, 2024.',
    'BRASIL. Lei nº 13.460, de 26 de junho de 2017. Dispõe sobre participação, proteção e defesa dos direitos do usuário dos serviços públicos da administração pública. Brasília, DF: Presidência da República, 2017.',
    'BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Brasília, DF: Presidência da República, 2018. Com as alterações da Lei nº 13.853, de 8 de julho de 2019.',
    'BRASIL. Lei nº 14.129, de 29 de março de 2021. Dispõe sobre princípios, regras e instrumentos para o Governo Digital e para o aumento da eficiência pública. Brasília, DF: Presidência da República, 2021a.',
    'BRASIL. Ministério da Ciência, Tecnologia e Inovações. Portaria MCTI nº 4.617, de 6 de abril de 2021. Institui a Estratégia Brasileira de Inteligência Artificial. Brasília, DF: MCTI, 2021b. Alterada pela Portaria MCTI nº 4.979, de 13 de julho de 2021.',
    'BRASIL. Senado Federal. Projeto de Lei nº 2338, de 2023. Dispõe sobre o uso da Inteligência Artificial. Brasília, DF: Congresso Nacional, 2023. Disponível em: https://www.congressonacional.leg.br/web/atividade/materias/-/materia/157233. Acesso em: 16 nov. 2026.',
    'CRISTÓVAM, José Sérgio da Silva; SAIKALI, Lucas Bossoni; SOUSA, Thanderson Pereira de. Governo digital na implementação de serviços públicos para a concretização de direitos sociais no Brasil. Sequência: Estudos Jurídicos e Políticos, Florianópolis, n. 84, p. 209–242, abr. 2020. DOI 10.5007/2177-7055.2020v43n84p209.',
    'GOIÁS. Programa Goiás Cidadão: estruturação de projetos. Goiânia: [s. n.], 2026. Documento interno, em validação institucional.',
    'GOOGLE. People + AI Guidebook. Mountain View: Google PAIR, [2019]. Disponível em: https://pair.withgoogle.com/guidebook/. Acesso em: 16 nov. 2026.',
    'JOBIN, Anna; IENCA, Marcello; VAYENA, Effy. The global landscape of AI ethics guidelines. Nature Machine Intelligence, v. 1, n. 9, p. 389–399, 2019. DOI 10.1038/s42256-019-0088-2.',
    'LEE, John D.; SEE, Katrina A. Trust in automation: designing for appropriate reliance. Human Factors, v. 46, n. 1, p. 50–80, 2004. DOI 10.1518/hfes.46.1.50_30392.',
    'LIAO, Q. Vera; GRUEN, Daniel; MILLER, Sarah. Questioning the AI: informing design practices for explainable AI user experiences. In: CHI CONFERENCE ON HUMAN FACTORS IN COMPUTING SYSTEMS, 2020, Honolulu. Proceedings [...]. New York: ACM, 2020. p. 1–15. DOI 10.1145/3313831.3376590.',
    'LYONS, Henrietta; VELLOSO, Eduardo; MILLER, Tim. Conceptualising contestability: perspectives on contesting algorithmic decisions. Proceedings of the ACM on Human-Computer Interaction, v. 5, n. CSCW1, art. 106, 2021. DOI 10.1145/3449180.',
    'MACOHIN, Aline. Inteligência artificial na administração pública brasileira: uma abordagem transparente e explicável. Rio de Janeiro: Lumen Juris, 2023.',
    'NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY (Estados Unidos). Artificial Intelligence Risk Management Framework (AI RMF 1.0). Gaithersburg: NIST, 2023. (NIST AI 100-1). DOI 10.6028/NIST.AI.100-1.',
    'NUNES, Erik Henrique da Costa; PACHECO, Sávio Teixeira; SOUZA, Moisés Cruz; MONTEIRO, Ingrid Teixeira. Diagnóstico da acessibilidade digital em serviços públicos prioritários usando a Lei de Acesso à Informação. In: SIMPÓSIO BRASILEIRO SOBRE FATORES HUMANOS EM SISTEMAS COMPUTACIONAIS (IHC), 24., 2025, [S. l.]. Anais [...]. Porto Alegre: SBC, 2025. p. 423–445. DOI 10.5753/ihc.2025.10754.',
    'PEDROSA, Glauco Vitor; CANEDO, Edna Dias; SILVA, Wander C. M. Pereira da; FIGUEIREDO, Rejane M. da C. Evaluating digital public services in Brazil: insights from federal managers. Journal on Interactive Systems, Porto Alegre, v. 17, n. 1, p. 846–862, 2026. DOI 10.5753/jis.2026.6874.',
    'SHNEIDERMAN, Ben. Human-centered artificial intelligence: reliable, safe & trustworthy. International Journal of Human–Computer Interaction, v. 36, n. 6, p. 495–504, 2020. DOI 10.1080/10447318.2020.1741118.',
    'SILVA, Jhennifer Pereira; SANTOS, Lorena Caroline Fernandes. Percepções dos usuários sobre serviços de e-gov no Brasil: uma análise qualitativa. Revista do Serviço Público, Brasília, v. 76, n. 3, p. 417–439, 2025. DOI 10.21874/rsp.v76i3.11163.',
    'WACHTER, Sandra; MITTELSTADT, Brent; FLORIDI, Luciano. Why a right to explanation of automated decision-making does not exist in the General Data Protection Regulation. International Data Privacy Law, v. 7, n. 2, p. 76–99, 2017. DOI 10.1093/idpl/ipx005.',
    'WIRTZ, Bernd W.; WEYERER, Jan C.; GEYER, Carolin. Artificial intelligence and the public sector: applications and challenges. International Journal of Public Administration, v. 42, n. 7, p. 596–615, 2019. DOI 10.1080/01900692.2018.1498103.',
]

sections = [
    section('01', 'problema', 'O paradoxo e o abismo',
            'Uma interação tecnicamente correta nem sempre é compreensível ou contestável por quem a utiliza.',
            [F2, F4],
            [acc('Por que o risco é maior no serviço público',
                 ['A inteligência artificial (IA) está cada vez mais presente em assistentes virtuais, buscas, recomendações e serviços automatizados, e o setor público a incorpora em áreas de aplicação diversas (Wirtz, Weyerer e Geyer, 2019). Uma interação tecnicamente correta, porém, nem sempre é compreensível, verificável ou contestável por quem a utiliza.',
                  'No serviço público, o risco é maior, pois o cidadão não escolhe outro prestador e erros podem afetar o acesso a benefícios, documentos e direitos. Estudos nacionais sobre chatbots governamentais registram, por exemplo, casos em que o atendimento não deixa claro que é automatizado (Batista, Monteiro e Salgado, 2022).']),
             acc('Governança e UX, em separado',
                 ['A literatura oferece diretrizes de UX para a interação humano-IA (Amershi et al., 2019), discussões sobre explicação e contestabilidade (Wachter, Mittelstadt e Floridi, 2017; Almada, 2019) e estruturas de governança de IA (NIST, 2023). Esses eixos costumam ser tratados em separado, e raramente no serviço público digital brasileiro.',
                  'Nas buscas realizadas para este estudo, não foi localizado trabalho que traduza controles de governança de IA em requisitos de interface e indicadores de avaliação. É essa lacuna que a matriz procura ocupar.'])]),
    section('02', 'caso', 'O caso: Programa Goiás Cidadão',
            'Fundações de dados primeiro, proatividade e IA depois, com uma etapa formal de liberação.',
            [F3, T1],
            [acc('O programa e o Canal Único',
                 ['O Programa Goiás Cidadão propõe evoluir o EXPRESSO, canal digital já consolidado com autenticação gov.br, para um modelo integrado e centrado na jornada do cidadão (Goiás, 2026). Organiza-se em duas camadas: uma fundação de dados, com interoperabilidade, identificação única e base única do cidadão, e uma camada de serviços e operação, com jornadas por momentos de vida, canal único, IA aplicada e gestão inteligente.',
                  'O horizonte é de 48 meses, em cinco níveis de maturidade. A regra de dependência estabelece que a proatividade e a IA vêm depois de dados governados e de supervisão humana, com uma etapa formal de liberação (gate, em inglês) que exige finalidade e base legal aprovadas, controles de acesso e auditoria, teste e supervisão.',
                  'O Canal Único integra o aplicativo e um número oficial de WhatsApp, sem eliminar o atendimento presencial, e prevê um Domicílio Digital do Cidadão como fonte oficial de comunicações.']),
             acc('Os quatro serviços monitorados',
                 ['Os serviços monitorados no período analisado foram a Carteira de Identidade Nacional (CIN), a renovação da Carteira Nacional de Habilitação (CNH), a Ouvidoria e a consulta ao licenciamento ambiental. Esses serviços são fluxos do WhatsApp e não foram identificados como serviços com IA, de modo que funcionam como linha de base do canal antes da IA.',
                  'O CIN concentrou cerca de 75% dos atendimentos (47.192 de 63.282) e teve as menores notas entre os serviços com amostra relevante (7,19 no canal e 7,13 no serviço), além da maior proporção de comentários negativos (34%). A Ouvidoria teve as maiores notas (8,30 e 8,29), e o licenciamento ambiental tem amostra pequena, com sete avaliações.'])]),
    section('03', 'referencial', 'O que a literatura oferece',
            'Diretrizes de UX, confiança, explicação, contestabilidade e o ponto cego da LGPD.',
            [F10],
            [acc('UX para interação humano-IA, confiança e controle',
                 ['Amershi et al. (2019) propõem 18 diretrizes para a interação humano-IA, agrupadas conforme o momento de uso: início da interação, durante a interação, quando o sistema erra e ao longo do tempo. O People + AI Guidebook (Google, 2019) reúne padrões de projeto sobre calibração da confiança, exibição de incerteza, retorno do usuário e possibilidade de assumir o controle quando o sistema falha. Liao, Gruen e Miller (2020) propõem um banco de perguntas que os usuários fazem à IA, útil para derivar requisitos de explicação.',
                  'Lee e See (2004) tratam a confiança em automação como atitude que deve ser calibrada: o objetivo não é maximizá-la, e sim favorecer a dependência apropriada. Shneiderman (2020) propõe que a IA centrada no humano combine alto grau de automação com alto grau de controle humano, o que fundamenta requisitos como escalonamento para atendimento humano e correção pelo usuário.']),
             acc('Governança, explicação e contestabilidade',
                 ['Os princípios éticos de IA, por si sós, não indicam o que o usuário deve ver ou poder fazer. Jobin, Ienca e Vayena (2019) encontraram convergência em torno de transparência, justiça, não maleficência, responsabilidade e privacidade, com grande variação na interpretação e na implementação. O AI Risk Management Framework do NIST (2023) organiza a gestão de risco em quatro funções (Govern, Map, Measure e Manage).',
                  'Wachter, Mittelstadt e Floridi (2017) argumentam que o regulamento europeu não cria um direito geral à explicação de decisões automatizadas. Almada (2019) defende sistemas contestáveis desde a concepção, com previsão de intervenção humana, e Lyons, Velloso e Miller (2021) examinam como conceituar a contestabilidade. No Brasil, Macohin (2023) sustenta que a legislação de proteção de dados, isoladamente, não basta para assegurar transparência.']),
             acc('O que a LGPD exige, e o que não exige',
                 ['A Lei Geral de Proteção de Dados (LGPD) prevê, em seu art. 20, o direito de solicitar a revisão de decisões tomadas unicamente com base em tratamento automatizado de dados pessoais (Brasil, 2018). O dispositivo que exigia que a revisão fosse feita por pessoa natural foi vetado, e o veto foi mantido pelo Congresso em 2019.',
                  'A revisão humana, portanto, não decorre diretamente da lei e precisa ser definida por política de governança. O Projeto de Lei nº 2338/2023, sobre o uso da IA, foi aprovado pelo Senado e tramita na Câmara dos Deputados (Brasil, 2023).']),
             acc('Avaliação da experiência em serviços públicos digitais',
                 ['Araújo et al. (2021) examinaram 25 portais web e 9 aplicativos móveis de governos estaduais e observaram inconsistência na ocorrência dos instrumentos de satisfação e falta de clareza sobre o que se pretendia avaliar. Pedrosa et al. (2026), com três grupos focais com 27 gestores federais de 12 instituições, identificaram baixa visibilidade da interface de avaliação, confusão entre avaliar a qualidade do serviço e o seu resultado e pouca participação do usuário.',
                  'Na acessibilidade, Barros et al. (2024) avaliaram o portal gov.br com ferramentas automatizadas e apontaram barreiras, e Nunes et al. (2025) analisaram os 80 serviços prioritários da Estratégia de Governo Digital e verificaram que os órgãos frequentemente terceirizam a responsabilidade pelos testes e que falta capacitação específica.'])]),
    section('04', 'matriz', 'A matriz governança × UX',
            'Treze requisitos em quatro dimensões: utilidade, transparência, confiança e controle.',
            [F5, F6, F7, F8, F9],
            [matriz_acc(d, r) for d, r in MATRIZ] +
            [acc('Como a matriz foi construída',
                 ['A matriz foi construída em cinco passos: (1) extração dos controles de governança de IA do documento do programa; (2) agrupamento em categorias gerais, apoiado nos referenciais de governança; (3) associação de cada categoria a requisitos de UX derivados da literatura, nas quatro dimensões de análise; (4) definição de evidências e indicadores, distinguindo os que constam no programa dos que são propostos pelo estudo; e (5) confronto de cada linha com a linha de base do painel.',
                  'As quatro dimensões são uma operacionalização do estudo, e não categorias estabelecidas na literatura. Os controles de governança entram como insumo, e a adequação institucional da governança não é avaliada.'])]),
    section('05', 'linha-de-base', 'Linha de base e lacunas',
            'O monitoramento atual mede satisfação, mas não compreensão, escalonamento, recusa ou contestação.',
            [F11, F12],
            [acc('O que o painel mostra',
                 ['Sete das 13 linhas têm dado correspondente, e todos são medidas de satisfação ou menções em comentários. A disponibilidade do serviço foi indicada para melhorar em 455 das 2.549 avaliações (17,8%) e, no CIN, em 390 de 1.878 (20,8%); a entrega do serviço, em 362 (14,2%); a clareza das informações, em 165 (6,5%); e a segurança da informação, em 62 (2,4%).',
                  'Dos 1.368 comentários válidos, 404 (29,5%) foram classificados como negativos, e os termos “atendente” e “humano” aparecem em apenas cinco e três comentários, respectivamente.']),
             acc('O que o painel não mostra',
                 ['Seis linhas, relativas a dados governados, aviso de IA, rastreabilidade do dado, recusa de usos proativos, contestação e reconciliação de divergências, não têm dado no painel. Isso indica que o monitoramento atual mede a satisfação com o canal e com o serviço, mas não a compreensão, o escalonamento, a recusa de usos proativos nem a contestação, que são justamente as dimensões que a matriz propõe medir.']),
             acc('Como ler esses números',
                 ['Esses números devem ser lidos com cautela. Araújo et al. (2021) e Pedrosa et al. (2026) mostram que instrumentos de satisfação nem sempre deixam claro o que avaliam. No painel analisado, as notas do canal e do serviço são coletadas separadamente, o que dialoga com essa preocupação, mas a nota de satisfação não mede compreensão nem controle.',
                  'Além disso, os serviços monitorados são fluxos do WhatsApp e não foram identificados como serviços com IA. Os dados funcionam como linha de base do canal antes da IA, e não como avaliação de interações com IA.']),
             acc('Seis lacunas a verificar na leitura documental',
                 ['Primeiro, o checklist de prontidão por serviço cobre acessibilidade, linguagem simples e escalonamento, mas não traz critérios específicos para interações com IA, como identificação do assistente, explicação de resultados ou fluxo de contestação. Segundo, a contestação aparece como entrega prevista, mas sem prazo, canal ou indicador definidos.',
                  'Terceiro, os indicadores de proatividade (aceite, recusa, reclamações e erros) medem o comportamento do cidadão, mas não se ele compreendeu por que recebeu a oferta. Quarto, falta distinguir o canal oficial de tentativas de fraude, o que importa em um canal como o WhatsApp.',
                  'Quinto, não há critério de UX na etapa de liberação da IA, que depende de base legal, dados e supervisão. Sexto, o programa precisa decidir em quais casos a contestação terá revisão humana, já que a lei não a exige. Essas lacunas são hipóteses derivadas da análise documental e dependem de verificação com as equipes responsáveis.'])]),
    section('06', 'recomendacoes', 'Recomendações',
            'Seis medidas a partir da matriz e das lacunas.',
            [F13],
            [acc('As seis recomendações',
                 ['(a) Incluir critérios de UX para IA no checklist de prontidão por serviço e na etapa de liberação da proatividade. (b) Definir a contestação com protocolo, prazo, retorno e regra de revisão humana. (c) Acrescentar ao monitoramento indicadores de compreensão do aviso de IA, de escalonamento, de recusa e de contestação, separados da satisfação com o resultado.',
                  '(d) Testar com usuários diversos, incluindo pessoas com baixa literacia digital e com deficiência, antes de cada onda de IA, em linha com as preocupações de acessibilidade apontadas por Barros et al. (2024) e Nunes et al. (2025). (e) Definir padrões para que o cidadão reconheça o canal oficial. (f) Validar a matriz em oficina com as equipes do Canal Único e da IA aplicada.'])]),
    section('07', 'metodo', 'Método, limites e referências',
            'Estudo de caso propositivo, com análise documental, revisão narrativa e dados agregados.',
            [],
            [acc('Como o estudo foi feito',
                 ['O estudo tem abordagem qualitativa e propositiva e adota o método de estudo de caso, tendo como caso o Programa Goiás Cidadão e, nele, o Canal Único (aplicativo e WhatsApp). Foram utilizadas três fontes: o documento de estruturação do programa, versão de outubro de 2026, documento interno em validação institucional; a literatura, reunida por revisão narrativa, com buscas em bases abertas, nos anais do IHC e do WCGE e em repositórios institucionais, sem pretensão de exaustividade; e a base agregada do painel de monitoramento dos serviços no WhatsApp, de 03/08 a 01/10/2026.',
                  'As avaliações trazem notas de 0 a 10 para o canal e para o serviço, critérios marcados como pontos a melhorar ou positivos e comentários cujo sentimento foi classificado pela equipe do painel, cujo método não está documentado na base. Os percentuais foram calculados sobre as 2.549 avaliações, e os comentários de testes foram excluídos, restando 1.368 comentários válidos.']),
             acc('Limitações',
                 ['O estudo é propositivo, os serviços monitorados não são serviços com IA, a base analisada vai até 01/10/2026 e a matriz não foi validada com especialistas ou cidadãos. Não há dados de uso real de IA nos serviços monitorados. A análise é acadêmica e não representa posição oficial do Estado.',
                  'Como trabalhos futuros, sugerem-se a validação da matriz em oficina e em testes com cidadãos, sua aplicação a um fluxo concreto de IA nas ondas seguintes, a comparação com outro caso de governo digital e a ampliação da linha de base com os dados posteriores a 01/10/2026.']),
             acc('Referências (%d)' % len(REFS), REFS)]),
]

closing = ('<section aria-labelledby="sintese" class="mt-16 rounded-2xl border bg-secondary/50 p-7"><h2 id="sintese" class="text-2xl font-semibold">A síntese</h2>'
           '<p class="mt-3 leading-relaxed text-muted-foreground">A resposta proposta é uma matriz de 13 linhas, em quatro dimensões, que relaciona categorias gerais de controle de governança a requisitos de interface, evidências e indicadores, confrontados com a linha de base do canal. A contribuição está em tornar operacional a relação entre governança e UX em um caso real de serviço público digital, e em mostrar que o monitoramento atual, centrado em satisfação, não mede compreensão, escalonamento, recusa de usos proativos nem contestação. A revisão humana de decisões automatizadas não é exigida pela LGPD e, por isso, depende de decisão de governança.</p>'
           + F14 +
           '<p class="mt-6 rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] italic leading-relaxed text-accent-foreground">O objetivo final do governo digital não é exibir a IA, e sim tornar a burocracia invisível, com respeito, transparência e controle que o cidadão possa verificar.</p></section>')


def build():
    stat = lambda n, l, count=True: ('<div><dt class="font-display text-2xl text-ochre"%s>%s</dt>'
                                     '<dd class="mt-1 text-xs uppercase tracking-wide text-primary-foreground/70">%s</dd></div>'
                                     % ('', n, l))
    header = ('<header class="relative overflow-hidden text-primary-foreground" style="background-image:var(--gradient-deep)">'
              '<div class="surface-paper absolute inset-0 opacity-30" aria-hidden="true"></div>'
              '<div class="relative mx-auto max-w-3xl px-6 py-20 sm:py-28">'
              '<p class="text-xs font-semibold uppercase tracking-[0.2em] text-ochre">Experiência do usuário · Inteligência artificial · Serviços públicos digitais</p>'
              '<h1 class="mt-6 text-4xl leading-[1.1] font-semibold sm:text-5xl">Da <span class="text-gradient-warm">governança</span> à interface</h1>'
              '<p class="mt-5 text-lg leading-relaxed text-primary-foreground/80">Requisitos de UX para uma IA transparente e contestável em serviços públicos.</p>'
              '<p class="mt-4 text-base leading-relaxed text-primary-foreground/70">O cidadão no controle da IA: o caso do Programa Goiás Cidadão.</p>'
              '<p class="mt-8 text-sm text-primary-foreground/70">Carlos Hernane de Oliveira</p>'
              '<div class="mt-6" style="display:flex;flex-wrap:wrap;gap:12px"><a href="../assets/pdf/%s" target="_blank" rel="noopener noreferrer" '
              'class="inline-flex items-center gap-2 rounded-full bg-ochre px-6 py-3 text-sm font-semibold text-ochre-foreground shadow-lift">'
              % PDF + BOOK + 'Leia o Artigo na Íntegra</a></div>'
              '<p class="mt-3 max-w-md text-sm leading-relaxed text-primary-foreground/70">Abre o PDF completo do artigo em uma nova aba, para leitura direta no navegador.</p>'
              '<dl class="mt-10 grid grid-cols-2 gap-6 sm:grid-cols-4">'
              + stat('13', 'requisitos de UX') + stat('4', 'dimensões') + stat('63.282', 'atendimentos analisados', False) + stat('6', 'linhas sem dado')
              + '</dl></div></header>')
    intro = ('<section aria-labelledby="resumo-ux"><h2 id="resumo-ux" class="text-2xl font-semibold">Do que trata o artigo</h2>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">A inteligência artificial avança em serviços públicos digitais, mas interações tecnicamente corretas podem ser pouco compreensíveis ou contestáveis pelo cidadão. O artigo propõe uma matriz que relaciona categorias de controle de governança de IA a requisitos de experiência do usuário (UX) para transparência e contestabilidade.</p>'
             '<p class="mt-4 leading-relaxed text-muted-foreground">Trata-se de um estudo de caso propositivo do Programa Goiás Cidadão, com análise documental, revisão de literatura e uma linha de base do painel de monitoramento dos serviços no WhatsApp (63.282 atendimentos e 2.549 avaliações, de 03/08 a 01/10/2026). A matriz reúne 13 requisitos em quatro dimensões: utilidade, transparência, confiança e controle. O monitoramento atual mede satisfação, mas não compreensão, escalonamento, recusa de usos proativos nem contestação, e seis das 13 linhas não têm dado correspondente.</p>'
             '<p class="mt-4 rounded-lg border-l-2 border-ochre bg-accent/50 px-4 py-3 text-[15px] leading-relaxed text-accent-foreground">Estudo propositivo: os serviços monitorados não são serviços com IA, a matriz ainda não foi validada com especialistas ou cidadãos, e o documento do programa citado como caso é interno e está em validação institucional. A análise é acadêmica e não representa posição oficial do Estado.</p>'
             + F1 + '</section>'
             '<section aria-labelledby="objetivos-ux" class="mt-10 rounded-2xl border bg-secondary/50 p-7"><h2 id="objetivos-ux" class="text-2xl font-semibold">Pergunta e objetivo</h2>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Pergunta de pesquisa</h3><p class="mt-2 leading-relaxed text-muted-foreground">Como traduzir os controles de governança de IA do Programa Goiás Cidadão em requisitos de UX que mantenham o cidadão informado, capaz de contestar resultados e no controle da interação?</p></div>'
             '<div class="mt-6"><h3 class="text-lg font-semibold text-ochre">Objetivo</h3><p class="mt-2 leading-relaxed text-muted-foreground">Propor e aplicar uma matriz que relacione categorias gerais de controle de governança a requisitos de UX, com evidências e indicadores. Os controles de governança entram como insumo, e não como objeto de avaliação.</p></div></section>')
    main = '<main class="mx-auto max-w-3xl px-6 py-16">' + intro + '<div class="mt-14 space-y-14">' + ''.join(sections) + '</div>' + closing + '</main>'
    footer = ('<footer class="border-t bg-card"><div class="mx-auto max-w-3xl px-6 py-10 text-sm text-muted-foreground">'
              '<p class="font-display text-base text-foreground">Da governança à interface: requisitos de UX para uma IA transparente e contestável em serviços públicos</p>'
              '<p class="mt-2">Carlos Hernane de Oliveira.</p>'
              '<p class="mt-2">Aspectos éticos: estudo documental com dados agregados, sem participantes; não foram reproduzidos comentários de cidadãos. Conflito de interesses: o autor atua em órgão envolvido na execução do programa estudado; as análises são acadêmicas e não representam posição oficial.</p>'
              '<p class="mt-4">Palavras-chave: experiência do usuário; inteligência artificial; governança; serviços públicos digitais; transparência.</p></div></footer>')
    page = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>'
            '<title>Da governança à interface: UX para uma IA transparente e contestável</title>'
            '<meta name="description" content="Matriz que traduz controles de governança de IA em 13 requisitos de UX para transparência e contestabilidade, com o caso do Programa Goiás Cidadão e uma linha de base do atendimento por WhatsApp.">'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&display=swap"/>'
            '<link rel="stylesheet" href="../assets/styles.css"/><link rel="stylesheet" href="../assets/mmdi.css"/>'
            '<script>document.documentElement.classList.add("js")</script></head><body>'
            + shell.nav(SLUG, '../') + '<div class="min-h-screen">' + header + main + footer + '</div>'
            '<script src="../assets/app.js"></script><script src="../assets/mmdi.js"></script></body></html>')
    os.makedirs('%s/%s' % (S, SLUG), exist_ok=True)
    open('%s/%s/index.html' % (S, SLUG), 'w', encoding='utf8').write(page)
    for f in os.listdir(SRC + '/img'):
        shutil.copy(SRC + '/img/' + f, S + '/assets/img/' + f)
    shutil.copy(SRC + '/' + PDF, S + '/assets/pdf/' + PDF)
    shutil.copy('build/mmdi.css', S + '/assets/mmdi.css')
    shutil.copy('build/mmdi.js', S + '/assets/mmdi.js')


if __name__ == '__main__':
    build()
