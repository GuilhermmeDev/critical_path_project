import pandas as pd
import matplotlib.pyplot as plt

# Exemplo de DataFrame
data = {
    'Item': ['A', 'B', 'C', 'D'],
    'Early Start': [0, 2, 4, 5],
    'Early Finish': [2, 4, 6, 7],
    'Late Start': [0, 2, 5, 5],
    'Late Finish': [2, 4, 7, 7]
}

df = pd.DataFrame(data)

# Calcular a folga
df['Folga'] = df['Late Start'] - df['Early Start']

# Identificar os itens críticos (Folga == 0)
df['Crítico'] = df['Folga'] == 0

# Exibir os itens críticos
print("Itens críticos:")
print(df[df['Crítico']]['Item'].tolist())

# Gerar imagem da tabela
fig, ax = plt.subplots(figsize=(12, 0.8 * len(df) + 1))
ax.axis('off')

# Criar a tabela
table = ax.table(
    cellText=df.drop(columns=['Crítico']).values,
    colLabels=df.drop(columns=['Crítico']).columns,
    cellLoc='center',
    loc='center'
)

# Ajustes de estilo
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 2)  # Aumenta altura das células

# Pinta linhas críticas de vermelho
for i in range(len(df)):
    if df.iloc[i]['Crítico']:
        for j in range(len(df.columns) - 1):  # -1 porque 'Crítico' não aparece na tabela
            cell = table[(i + 1, j)]  # i+1 porque linha 0 é cabeçalho
            cell.set_facecolor('#f28b82')  # cor vermelha clara

# Salvar imagem
plt.savefig('caminho_critico_bonito.png', bbox_inches='tight', dpi=300)

plt.show()

