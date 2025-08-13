# Dashboard de Dados do ComexStat

Este projeto utiliza a API pública do [ComexStat](https://api-comexstat.mdic.gov.br/) 
para exibir dados de exportação e importação em um dashboard interativo no Streamlit.

## Estrutura
- `main.py` → Página inicial
- `pages/1_comex_cidades.py` → Dashboard por cidade
- `utils/comex_api.py` → Funções para consumir a API do ComexStat

## Como rodar localmente
```bash
pip install -r requirements.txt
streamlit run main.py