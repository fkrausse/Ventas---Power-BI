
import pandas as pd

dados = pd.read_excel("Vendas.xlsx", parse_dates=['DataEmissao'])

dados2 = dados.groupby(["DataEmissao", 'cdProduto'], as_index=False)['ValorVenda'].sum()
dados2.head()

dados2['Dia_do_mes'] = dados2['DataEmissao'].dt.day
dados2['Mes'] = dados2['DataEmissao'].dt.month
dados2['Ano'] = dados2['DataEmissao'].dt.year
dados2['Dia_da_semana'] = dados2['DataEmissao'].dt.weekday
dados3 = dados2.drop("DataEmissao", axis=1)


from sklearn.tree import DecisionTreeRegressor

modelo = DecisionTreeRegressor()
modelo.fit(dados3[['Dia_do_mes','Mes', 'Ano', 'Dia_da_semana', 'cdProduto']], dados3['ValorVenda'])


futuro = pd.date_range("2019-03-14", "2019-03-31", freq='D')

futuro_todos = []

for cdProduto in dados3['cdProduto'].unique():
    futuro_df = pd.DataFrame()
    futuro_df['Dia_do_mes'] = futuro.day
    futuro_df['Mes'] = futuro.month
    futuro_df['Ano'] = futuro.year
    futuro_df['Dia_da_semana'] = futuro.weekday
    futuro_df['cdProduto'] = cdProduto
     
    p = modelo.predict(futuro_df)
    
    futuro_df['ValorVenda'] = p
    
    futuro_todos.append(futuro_df)
    
futuro_todos_df = pd.concat(futuro_todos, ignore_index=True)