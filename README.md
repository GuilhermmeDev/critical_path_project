# 📊 Método do Caminho Crítico (CPM) com Python e Matplotlib

Este projeto implementa o **Método do Caminho Crítico (Critical Path Method)** em Python, utilizando **NetworkX** e **Matplotlib** para gerar o **diagrama de rede estilo PERT**, conforme o modelo clássico usado em gerenciamento de projetos.

## 🔍 O que o projeto faz

- Lê uma tabela com atividades e seus tempos de início e término;
- Calcula:
  - **Folga** (Slack) de cada atividade;
  - **Caminho crítico** do projeto;
- Gera uma imagem com o **diagrama em rede hierárquico horizontal**:
  - Atividades iniciais à esquerda;
  - Conexões com base na **precedência**;
  - Destaque em **vermelho** para atividades críticas.

---
