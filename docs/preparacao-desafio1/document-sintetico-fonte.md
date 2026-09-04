# Conteúdo-fonte do PDF sintético (fallback de DEC-03)

> Autorizado pelo owner em 2026-09-04 ("crie um com as informações necessárias às perguntas exemplo").
> Uso: **somente** se o `document.pdf` do template falhar na verificação da fatia A1 (não contiver o fato de aceite), ou como fixture de teste.
> Geração do binário `.pdf` ocorre na Fase B (requer Python instalado) — este arquivo é apenas a fonte de texto.

## Regras de conteúdo

1. **DEVE** conter, de forma explícita e literária, o fato de aceite: faturamento da Empresa SuperTechIABrazil = 10 milhões de reais (resposta esperada: "O faturamento foi de 10 milhões de reais.").
2. **NÃO DEVE** conter: número de clientes em 2024 (nem qualquer contagem de clientes por ano), capitais de países, ou qualquer dado que responda às perguntas fora-de-contexto do enunciado.
3. Sem PII real, sem segredos, sem dados de pessoas — conteúdo 100% fictício (DEC-07 já autoriza envio, mas o fixture deve ser seguro por construção).
4. Tamanho alvo: 2.000–4.000 caracteres (≥3 chunks de 1000 com overlap 150), para exercitar o split de forma representativa.

## Texto aprovado para o PDF

```text
Relatório Anual SuperTechIABrazil — Exercício 2025

A Empresa SuperTechIABrazil é uma companhia fictícia de tecnologia sediada em
São Paulo, fundada em 2018, que atua no desenvolvimento de soluções de
inteligência artificial aplicadas a atendimento ao cliente e automação de
processos corporativos.

Resultados financeiros
O faturamento da Empresa SuperTechIABrazil foi de 10 milhões de reais no
exercício de 2025. O resultado representa crescimento em relação ao ano
anterior, impulsionado pela expansão da carteira de produtos de IA generativa
e pela renovação de contratos corporativos de longo prazo.

Produtos e operações
O portfólio da empresa inclui uma plataforma de busca semântica documental,
um assistente de atendimento baseado em modelos de linguagem e uma ferramenta
de extração de dados de notas fiscais. A operação é organizada em três
frentes: pesquisa e desenvolvimento, engenharia de produto e suporte ao
cliente corporativo.

Governança e compliance
A SuperTechIABrazil mantém políticas internas de proteção de dados alinhadas
à LGPD, com revisão anual de fornecedores de nuvem e de APIs externas de
inteligência artificial. Todo o conteúdo deste relatório é fictício e foi
produzido exclusivamente para fins educacionais.

Perspectivas
Para o próximo exercício, a empresa planeja ampliar a equipe de engenharia,
investir em avaliação sistemática de modelos e publicar relatórios
trimestrais de qualidade das respostas geradas por seus assistentes.
```

## Verificação na Fase B (fatia A1)

- [ ] `document.pdf` do template contém "SuperTechIABrazil" e "10 milhões"? → usar o do template.
- [ ] Caso contrário: gerar PDF a partir do texto acima (fonte aprovada) e registrar em 12-DECISIONS.md que DEC-03=B.
