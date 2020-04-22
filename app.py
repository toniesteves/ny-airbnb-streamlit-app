import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import altair as alt
import seaborn as sns
sns.set(style="whitegrid")
import base64
from matplotlib import rcParams
rcParams['figure.figsize'] = 15,7


@st.cache
def get_data():
  # return pd.read_csv("http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv")
  return pd.read_csv("data/listings.csv")

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(sep='\t', decimal=',', index=False, header=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">csv file</a>'
    return href


def main():
  df = get_data()
  st.title("Análise de Dados no Airbnb NY")
  st.markdown("Através dos dados do Airbnb NY vamos efetuar uma análise exploratoria e oferecer insights sobre esses dados. Para isso vamos utilizar o [dataset](http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv) do Airbnb, contendo os anuncios de NY até o ano de 2020")

  st.header("Resumo")

  st.markdown("O Airbnb é uma plataforma que fornece e orienta a oportunidade de vincular dois grupos - os anfitriões e os convidados. Qualquer pessoa com uma sala aberta ou espaço livre pode fornecer serviços no Airbnb à comunidade global. É uma boa maneira de fornecer renda extra com o mínimo esforço. É uma maneira fácil de anunciar espaço, porque a plataforma possui tráfego e uma base global de usuários para apoiá-lo. O Airbnb oferece aos hosts uma maneira fácil de monetizar um espaço que seria desperdiçado.")

  st.markdown("Por outro lado, temos hóspedes com necessidades muito específicas - alguns podem estar procurando acomodações acessíveis perto das atrações da cidade, enquanto outros são um apartamento de luxo à beira-mar. Eles podem ser grupos, famílias ou indivíduos locais e estrangeiros. Depois de cada visita, os hóspedes têm a oportunidade de avaliar e ficar com seus comentários. Vamos tentar descobrir o que contribui para a popularidade da listagem e prever se a listagem tem potencial para se tornar uma das 100 acomodações mais revisadas com base em seus atributos.")

  st.markdown('-----------------------------------------------------')

  st.header("Anúncios do Airbnb em Nova York: Exploração de Dados")
  st.markdown("Os primeiros 10 registros dos dados do Airbnb")

  st.dataframe(df.head(10))

  #################### DISTRIBUIÇÃO GEOGRÁFICA ######################

  st.header("Localização")
  st.markdown("Abaixo destacamos  a distribuição geográfica das hopedagens por preço. ")
  values = st.slider('', 100, 10000, (500))
  st.map(df.query(f"price>={values}")[["latitude", "longitude"]].dropna(how="any"), zoom=10)


  #################### FILTRANDO POR ÁREAS DE INTERESSE ######################
  st.subheader("Selecting a subset of columns")
  st.markdown("_**Note:** É possível buscar pelas seguintes características: **Preço**, **Tipo de Acomodação**, **Mínimo de Noites**, **Distrito**, **Nome do Local**, **Reviews**_")
  st.write(f"Out of the {df.shape[1]} columns, you might want to view only a subset. Streamlit has a [multiselect](https://streamlit.io/docs/api.html#streamlit.multiselect) widget for this.")
  defaultcols = ["price", "minimum_nights", "room_type", "neighbourhood", "name", "number_of_reviews"]
  cols = st.multiselect("Columns", df.columns.tolist(), default=defaultcols)
  st.dataframe(df[cols].head(10))


  ################################## DISTRITOS ###############################

  st.subheader("Distritos")
  st.markdown("A Cidade de Nova Iorque abrange cinco divisões administrativas em nível de condados chamadas *boroughs*: **Bronx**, **Brooklyn**, **Manhattan**, **Queens** e **Staten Island**. Cada *borough* é coincidente com um respectivo condado do Estado de Nova Iorque. Os boroughs de Queens e Bronx são concomitantes com os condados de mesmo nome, enquanto os boroughs de Manhattan, Brooklyn e Staten Island correspondem aos de Nova Iorque, Kings e Richmond, respectivamente.")

  st.write(df.query("price>=800").sort_values("price", ascending=False).head())

  st.markdown("Abaixo é possível verificar que a média de preço no distrito de Manhattan consegue ser bem superior")

  fig = sns.barplot(x='neighbourhood_group', y='price', data=df.groupby('neighbourhood_group')['price'].mean().reset_index(),
  palette="Blues_d")
  sns.set(font_scale = 1.5)
  fig.set_xlabel("Distrito",fontsize=20)
  fig.set_ylabel("Preço ($)",fontsize=20)

  st.pyplot()

  st.write("At 169 days, Brooklyn has the lowest average availability. At 226, Staten Island has the highest average availability.\
  If we include expensive listings (price>=$200), the numbers are 171 and 230 respectively.")
  st.markdown("_**Note:** There are 18431 records with `availability_365` 0 (zero), which I've ignored._")


  ################### DISTRIBUIÇÃO PERCENTUAL POR DISTRITO #####################

  st.header("Distribuição Percentual por Distrito.")
  st.write("Using a radio button restricts selection to only one option at a time.")
  st.write("💡 Notice how we use a static table below instead of a data frame. \
  Unlike a data frame, if content overflows out of the section margin, \
  a static table does not automatically hide it inside a scrollable area. \
  Instead, the overflowing content remains visible.")
  neighborhood = st.radio("Distrito", df.neighbourhood_group.unique())
  is_expensive = st.checkbox("Acomodações Caras")
  is_expensive = " and price<200" if not is_expensive else ""

  @st.cache
  def get_availability(show_exp, neighborhood):
      return df.query(f"""neighbourhood_group==@neighborhood{is_expensive}\
          and availability_365>0""").availability_365.describe(\
              percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T

  st.table(get_availability(is_expensive, neighborhood))


  ###################### MÉDIA DE PREÇO POR ACOMODAÇÃO #######################

  st.header("Média de Preço por Tipo de Acomodação")
  st.write("You can also display static tables. As opposed to a data frame, with a static table you cannot sorting by clicking a column header.")
  st.table(df.groupby("room_type").price.mean().reset_index()\
      .round(2).sort_values("price", ascending=False)\
      .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))


  ######################### ANFITRIÕES MAIS LISTADOS ##########################

  st.header("Quais os andfitriões mais bem avaliados")


  rcParams['figure.figsize'] = 20,10
  ranked = df.groupby(['host_name'])['number_of_reviews'].count().sort_values(ascending=False).reset_index()
  ranked = ranked.head(5)
  sns.set_style("whitegrid")
  sns.set(font_scale = 1.5)
  fig = sns.barplot(y='host_name', x='number_of_reviews', data=ranked,palette="Blues_d",)
  fig.set_xlabel("Nº de Reviews",fontsize=20)
  fig.set_ylabel("Host",fontsize=20)

  st.pyplot()

  st.write(f"""O anfitrião **{ranked.iloc[0].host_name}** aparece no topo da lista com {ranked.iloc[0].number_of_reviews} reviews.
  **{ranked.iloc[1].host_name}** é o segundo com {ranked.iloc[1].number_of_reviews} reviews. Cabe salientar ainda que reviews não se tratam de revies positivas ou negativas, mas uma contagem de feedbacks fornecidos para a acomodação.""")


  #################### ANÁLISE DA DISTRIBUIÇÃO DO PREÇO ######################

  st.header("Distribuição dos Preços")
  st.write("""Select a custom price range from the side bar to update the histogram below displayed as a Plotly chart using
  [`st.plotly_chart`](https://streamlit.io/docs/api.html#streamlit.plotly_chart).""")
  values = st.slider("Faixa de Preço", float(df.price.min()), float(df.price.clip(upper=1000.).max()), (50., 300.))
  f = px.histogram(df.query(f"price.between{values}"), x="price", nbins=100, title="Price distribution")
  f.update_xaxes(title="Price")
  f.update_yaxes(title="No. of listings")
  st.plotly_chart(f, color='lifeExp')

  @st.cache
  def get_availability(show_exp, neighborhood):
    return df.query(f"""neighbourhood_group==@neighborhood{show_exp}\
    and availability_365>0""").availability_365.describe(\
    percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T


  ################## LISTANDO HOTEIS POR NUMERO DE REVIEWS ####################

  st.header("Quais as propriedades mais bem avaliadas")
  st.write("Enter a range of numbers in the sidebar to view properties whose review count falls in that range.")

  st.markdown("_**Note:** É possível otimizar ainda mais sua busca clicando em cima do nome da caracteristica que mais te interessa._")
  reviews = st.slider('', 0, 12000, (100))

  df.query(f"number_of_reviews<={reviews}").sort_values("number_of_reviews", ascending=False)\
  .head(50)[["number_of_reviews", "price", "neighbourhood", "room_type", "host_name"]]

  st.write("654 é o número mais alto de críticas e apenas uma única propriedade o possui. Em geral, listagens com mais de 400 avaliações têm um preço abaixo de US $ 100. Alguns estão entre US $ 100 e US $ 200, e apenas um tem preço acima de US $ 200.")



  ################################ SIDEBAR ################################

  st.sidebar.subheader("Bem-vindo!")

  st.sidebar.markdown(" ")
  st.sidebar.markdown(" ")
  st.sidebar.markdown("Sou pesquisador nas áreas de Machine Learning/DS, com ênfase em Visão Computacional e Análise de Dados. Atuo principalmente nos seguintes temas: reconhecimento de padrões, estatística inferencial e descritiva, probabilidade, aprendizado profundo.")

  st.sidebar.markdown("**Projeto:** Análise exploratória dos dados do Airbnb")

  st.sidebar.markdown("**Autor**: Toni Esteves")
  st.sidebar.markdown("**Contato**: toni.esteves@gmail.com")

  st.sidebar.markdown("- [Linkedin](https://www.linkedin.com/in/toniesteves/)")
  st.sidebar.markdown("- [Twitter](https://twitter.com/)")
  st.sidebar.markdown("- [Medium](https://medium.com/@toni_esteves)")


  st.sidebar.markdown("**Versão:** 1.0.0")

  st.markdown(get_table_download_link(df), unsafe_allow_html=True)


  st.markdown('-----------------------------------------------------')
  st.text('Desenvolvido por Toni Esteves - 2020')
  st.text('Contato: toni.esteves@gmail.com')

if __name__ == '__main__':
	main()
