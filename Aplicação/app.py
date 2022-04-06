from unittest import result
import streamlit as st
import pickle as pk
import pandas as pd

class app:
    def __init__(self):
        self.modelo = self.carrega_modelo()
        self.filmes = pd.read_csv('../Dados/filmes_completo.csv')

        self.header()
        filme = self.recebe_filme()
        self.recomendacao(filme)

    def header(self):
        st.write('# Sistema de recomendação de filmes')
        st.write('Sistema que recomenda filmes baseado em época e popularidade.')
        st.write('')
        st.write('')

    def recebe_filme(self):
        nome_filme = st.selectbox('Insira um nome de filme: ', self.filmes['Name'].unique())
        filme = self.filmes[self.filmes['Name'] == nome_filme]
        ano_filme = filme['Year'].values[0]

        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f'**Nome:** {nome_filme}')

        with col2:
            st.write(f'**Ano:** {ano_filme}')

        st.write('')
        st.write('')

        return filme

    def recomendacao(self, filme):
        dists, indices_recomendacao = self.modelo.kneighbors(filme[['mais_antigo', 
                                                                    'anos_80',
                                                                    'anos_90',
                                                                    'coeficiente_popularidade']], 11)

        resultados = self.filmes.iloc[indices_recomendacao[0]].copy()
        resultados['dist'] = dists[0]
        resultados = resultados.sort_values(by='dist', ascending=True).reset_index(drop=True)

        st.write('**Com base no filme escolhido, talvez você goste de:**')

        for i in range(1, resultados.shape[0]):
            nome = resultados.iloc[i]['Name']
            ano = resultados.iloc[i]['Year']

            linha = f'{nome} ({ano})'
            link = f'https://www.google.com/search?q={self.elimina_espaco(nome)}'

            st.markdown(f'{i}. [{linha}]({link})')

    def carrega_modelo(self):
        arq = open('../Modelos/modelo-sistema-rec.pk', 'rb')
        modelo = pk.load(arq)
        arq.close()
        return modelo

    def elimina_espaco(self, string):
        return string.replace(' ', '+')

if __name__ == '__main__':
    app()