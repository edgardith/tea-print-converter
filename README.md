# TEA-Print Converter (Streamlit)

Interface gráfica para converter atividades pedagógicas originais em versões
adaptadas e prontas para impressão, para alunos com TEA — Educação Infantil.

- Níveis de suporte DSM-5 (N1/N2/N3), Campos de Experiência BNCC, CAA
- Pictogramas reais do [ARASAAC](https://arasaac.org) (CC BY-NC-SA 4.0)
- PDF de 2 páginas A4: atividade do aluno + orientações para o professor

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Abre automaticamente em `http://localhost:8501`. Cole sua Anthropic API Key
na barra lateral (fica só na sessão do navegador, nunca é salva em disco).

> Para OCR de imagens funcionar localmente, instale também o binário do
> Tesseract:
> - Linux/Debian: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
> - macOS: `brew install tesseract tesseract-lang`
> - Windows: https://github.com/UB-Mannheim/tesseract/wiki

## Hospedar de graça (para compartilhar com outros pais/educadores)

1. Suba esta pasta para um repositório no GitHub (pode ser público ou privado).
2. Acesse [share.streamlit.io](https://share.streamlit.io) (Streamlit Community
   Cloud), conecte sua conta GitHub e escolha o repositório + `app.py`.
3. O arquivo `packages.txt` já está incluso, então o Tesseract OCR (com
   idioma português) é instalado automaticamente no servidor deles — de
   graça, sem custo de hospedagem.
4. **Cada pessoa que usar o app cola a própria Anthropic API Key** na barra
   lateral — assim você não paga pelo uso de outras famílias/escolas. Se
   preferir bancar o custo você mesmo (ex: para uma comunidade pequena),
   dá pra usar `st.secrets` para guardar uma chave compartilhada, mas isso
   expõe você a uso ilimitado por qualquer visitante — não recomendado sem
   um limite de requisições.

## Estrutura

- `app.py` — interface (Streamlit), replica visualmente o protótipo original
  em HTML (cores teal/âmbar, stepper de 4 etapas, cards)
- `core.py` — toda a lógica: leitura de arquivos, busca ARASAAC, chamada à
  API da Anthropic, geração do PDF com ReportLab
- `requirements.txt` — dependências Python
- `packages.txt` — dependências de sistema (Tesseract OCR) para deploy

## Licença dos pictogramas

Os pictogramas vêm do ARASAAC (Governo de Aragón, Espanha) sob licença
**CC BY-NC-SA 4.0**: uso gratuito e não comercial, com atribuição — que já
fica automaticamente no rodapé de cada PDF gerado. Perfeitamente adequado
para uso pessoal e para oferecer gratuitamente a outras famílias/escolas.
