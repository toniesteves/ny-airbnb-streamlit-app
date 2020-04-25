from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import altair as alt
import seaborn as sns
sns.set_style("whitegrid")
import base64
import datetime
from matplotlib import rcParams
from  matplotlib.ticker import PercentFormatter


@st.cache
def get_data():
  # return pd.read_csv("http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv")
  return pd.read_csv("data/listings.csv")

@st.cache
def get_profile_pic():
  return Image.open('profile.png')

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(sep='\t', decimal=',', index=False, header=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download</a>'
    return href


def main():
  df = get_data()

  ################################ SIDEBAR ################################

  st.sidebar.image(get_profile_pic(), use_column_width=False, width=250)
  st.sidebar.header("Welcome!")

  st.sidebar.markdown(" ")
  st.sidebar.markdown("*I am a researcher in Machine Learning/DS, with an emphasis on Computer Vision and Data Analysis. I work mainly on the following themes: pattern recognition, inferential and descriptive statistics, probability, deep learning.*")

  st.sidebar.markdown("**Author**: Toni Esteves")
  st.sidebar.markdown("**Mail**: toni.esteves@gmail.com")

  st.sidebar.markdown("- [Linkedin](https://www.linkedin.com/in/toniesteves/)")
  st.sidebar.markdown("- [Twitter](https://twitter.com/)")
  st.sidebar.markdown("- [Medium](https://medium.com/@toni_esteves)")


  st.sidebar.markdown("**Version:** 1.0.0")


  ################################ SUMMARY ################################

  st.title("Airbnb NY listings Data Analysis")
  st.markdown('-----------------------------------------------------')

  st.markdown("*Through Airbnb NY data we will conduct an exploratory analysis and offer insights into that data. For this we will use the data behind the website **Inside Airbnb** come from publicly available information on the Airbnb website available [here](http://insideairbnb.com/), containing advertisements for accommodation in NY until 2020*")


  st.header("Summary")

  st.markdown("Airbnb is a platform that provides and guides the opportunity to link two groups - the hosts and the guests. Anyone with an open room or free space can provide services on Airbnb to the global community. It is a good way to provide extra income with minimal effort. It is an easy way to advertise space, because the platform has traffic and a global user base to support it. Airbnb offers hosts an easy way to monetize space that would be wasted.")

  st.markdown("On the other hand, we have guests with very specific needs - some may be looking for affordable accommodation close to the city's attractions, while others are a luxury apartment by the sea. They can be groups, families or local and foreign individuals. After each visit, guests have the opportunity to rate and stay with their comments. We will try to find out what contributes to the listing's popularity and predict whether the listing has the potential to become one of the 100 most reviewed accommodations based on its attributes.")

  st.markdown('-----------------------------------------------------')

  st.header("Airbnb New York Listings: Data Analysis")
  st.markdown("Following is presented the first 10 records of Airbnb data. These records are grouped along 16 columns with a variety of informations as host name, price, room type, minimum of nights,reviews and reviews per month.")
  st.markdown("We will start with familiarizing ourselves with the columns in the dataset, to understand what each feature represents. This is important, because a poor understanding of the features could cause us to make mistakes in the data analysis and the modeling process. We will also try to reduce number of columns that either contained elsewhere or do not carry information that can be used to answer our questions.")

  st.dataframe(df.head(10))

  st.markdown("Another point about our data is that it allows sorting the dataframe upon clicking any column header, it a more flexible way to order data to visualize it.")

  #################### DISTRIBUIÇÃO GEOGRÁFICA ######################

  st.header("Listing Locations")
  st.markdown("Airbnb’s first New York listing was in Harlem in the year 2008, and the growth since has been exponential. Below we highlight the geographical distribution of listings. Initially we can filter them by price range, minimum number of available nights and number of reviews, so more flexibility is added when looking for a place. ")
  st.markdown("We could also filter by listing **price**, **minimum nights** on a listing or minimum of **reviews** received. ")

  values = st.slider("Price Range ($)", float(df.price.min()), float(df.price.clip(upper=10000.).max()), (500., 1500.))
  min_nights_values = st.slider('Minimum Nights', 0, 30, (1))
  reviews = st.slider('Minimum Reviews', 0, 700, (0))
  st.map(df.query(f"price.between{values} and minimum_nights<={min_nights_values} and number_of_reviews>={reviews}")[["latitude", "longitude"]].dropna(how="any"), zoom=10)

  st.markdown("In a general way the map shows that locations in the city centre are more expensive, while the outskirts are cheaper (a pattern that probably does not only exists in New York). In addition, the city centre seems to have its own pattern.")
  st.markdown("Unsurprisingly, Manhattan island has the highest concentration of expensive Airbnbs. Some are scattered over Brooklyn too. The heftiest price tag is $10.000,00. Another likely insight is that if we know that a specific location is very close to a place we consider expensive most probably the whole sorrounding area will be expensive.")
  st.markdown("Highly rated locations also tend to be the most expensive ones. Again downtown Manhattan and adjacent areas of Brooklyn receive the highest location scores, with East Village being an exception. A marked drop in location scores is seen as the subway lines end.")
  st.markdown("In a side analysis it can be possible to see that around Manhattan there are much fewer flats than compared to areas around, in addition, most of the points of interest (_Empire State Buildind, Times Square, Central Park_) are located in ‘expensive’ areas, especially around Dam Square's district.")
  st.markdown("In Staten Island, the areas close to the State Park have the highest location scores. Brooklyn neighbourhoods close to Manhattan tend to have higher location ratings. Looking at the NY subway system in Brooklyn, it is interesting to observe that the highly rated areas correspond with subway line presence. The same is true for Bronx where subway lines do not go.")

  #################### AREAS OF INTEREST ######################

  st.header("What you looking for?")
  st.write(f"Out of the {df.shape[1]} columns, you might want to view only a subset. These are the most correlated columns to prince listing, besides that is possible filter by first interest")
  st.markdown("_**Note:** In a  more conventient way to filter our data is possible filter our data through the following features: **Price**, **Room Type**, **Minimum of Nights**, **District(Neighbourhood)**, **Host Name**, **Reviews**_")
  defaultcols = ["price", "minimum_nights", "room_type", "neighbourhood", "name", "number_of_reviews"]
  cols = st.multiselect('', df.columns.tolist(), default=defaultcols)
  st.dataframe(df[cols].head(10))


  ################################## DISTRICT ###############################

  st.header("Districts")
  st.markdown("The New York City encompasses five county-level administrative divisions called * boroughs *: ** Bronx **, ** Brooklyn **, ** Manhattan **, ** Queens ** and ** Staten Island **. Each * borough * matches a respective New York State county. The boroughs of Queens and Bronx are concurrent with the counties of the same name, while the boroughs of Manhattan, Brooklyn and Staten Island correspond to those of New York, Kings and Richmond, respectively.")

  st.markdown("Again unsurprisingly it is possible see that the average price in the Manhattan district can be much higher than other districts. Manhattan has an average price of twice the Bronx ")

  fig = sns.barplot(x='neighbourhood_group', y='price', data=df.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False).reset_index(),
  palette="Blues_d")
  sns.set(font_scale = 1.5)
  fig.set_xlabel("District",fontsize=10)
  fig.set_ylabel("Price ($)",fontsize=10)

  st.pyplot()


  ################### PERCENTAGE DISTRIBUTION BY DISTRICT #####################

  st.header("Availability and Distribution by District.")
  st.markdown("The **availability_365** feature mean the number of days of the year (365) listing availability. Let's check it out.")

  neighborhood = st.radio("District", df.neighbourhood_group.unique())
  is_expensive = st.checkbox("Expensive Listings")
  is_expensive = " and price<100" if not is_expensive else ""

  @st.cache
  def get_availability(show_exp, neighborhood):
      return df.query(f"""neighbourhood_group==@neighborhood{is_expensive}\
          and availability_365>0""").availability_365.describe(\
              percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T

  st.table(get_availability(is_expensive, neighborhood))
  st.markdown("_**Note:** There are 18431 records with **availability_365** 0 (zero), which I've ignored._")
  st.markdown("At 170 days, Brooklyn has the lowest average availability. At 224, Staten Island has the highest average availability. If we include expensive listings (more tha $100 in a listing), the numbers are 171 and 230 respectively.")

  ###################### QUANTITY OF ROOM TYPES BY DISTRICT #######################

  st.markdown("Following, let's check the relationship between property type and neighbourhood. The primary question we aim to answer is whether different boroughs constitute of different rental types. Though in the expanded dataset there are more than 20 types, we will be focussing on the top 4 by their total count in the city and understanding their distribution in each borough.")

  room_types_df = df.groupby(['neighbourhood_group', 'room_type']).size().reset_index(name='Quantity')
  room_types_df = room_types_df.rename(columns={'neighbourhood_group': 'District', 'room_type':'Room Type'})
  room_types_df['Percentage'] = room_types_df.groupby(['District'])['Quantity'].apply(lambda x:100 * x / float(x.sum()))

  sns.set_style("whitegrid")
  sns.set(rc={'figure.figsize':(11.7,8.27)})
  fig = sns.catplot(y='Percentage', x='District', hue="Room Type", data=room_types_df, height=6, kind="bar", palette="muted", ci=95);
  fig.set(ylim=(0, 100))


  for ax in fig.axes.flat:
      ax.yaxis.set_major_formatter(PercentFormatter(100))
  plt.show()

  st.pyplot()

  st.markdown("The plot shows the ratio of property type and the total number of properties in the borough.")

  st.subheader("Some key observations from the graph are:")

  st.markdown(" - We can see that **Private Room** listings are highest in number in all tree borough except Manhattan and Staten Island. Staten Island has more ‘House’ style property than ‘Apartments’ thus, probably the only possible listings are apartments. This analysis seems intuitive, as we know that Staten Island is not that densely populated and has a lot of space.")

  st.markdown(" - The maximum **Entire home/apt** listings are located in Manhattan, constituting 60.55% of all properties in that neighborhood. Next is Staten Island with 49.86% **Entire home/apt**.")

  st.markdown(" - Queens, Brooklyn and the Bronx also have many listings for **Private room**. In Queens, 59.25% of the apartments are of the **Private room** type, which is larger than in the Bronx.")

  st.markdown(" - **Shared Room** listings types are also common in New York. Bronx constitutes of 5.59% of **Shared Room** listings type followed by Queens with 3.58% **Shared Room** listings type.")

  st.markdown(" - Manhattan has nearly 1.55% of **Hotel Room** listings. Next is Queens with 6.83% **Hotel Room** listings followed by Brooklyn with 3.32%. The other tree borough does not present any **Hotel Room** listings.")


  ###################### PRICE AVERAGE BY ACOMMODATION #########################

  st.header("Average price by room type")

  st.markdown("To listings based on room type, we can show price average grouped by borough.")

  avg_price_room = df.groupby("room_type").price.mean().reset_index()\
      .round(2).sort_values("price", ascending=False)\
      .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y))

  avg_price_room = avg_price_room.rename(columns={'room_type':'Room Type', 'avg_price': 'Average Price ($)', })

  st.table(avg_price_room)

  st.markdown("Despite together **Hotel Room** listings represent just over 10%, they are responsible for the highest price average, followed by **Entire home/apt**. Thus there are a small number of **Hotel Room** listings due its expensive prices.")


  ############################ MOST RATED HOSTS #############################

  st.header("Most rated hosts")

  rcParams['figure.figsize'] = 15,7
  ranked = df.groupby(['host_name'])['number_of_reviews'].count().sort_values(ascending=False).reset_index()
  ranked = ranked.head(5)
  sns.set_style("whitegrid")
  fig = sns.barplot(y='host_name', x='number_of_reviews', data=ranked,palette="Blues_d",)
  fig.set_xlabel("Nº de Reviews",fontsize=10)
  fig.set_ylabel("Host",fontsize=10)

  st.pyplot()

  st.write(f"""The host **{ranked.iloc[0].host_name}** is at the top with {ranked.iloc[0].number_of_reviews} reviews.
  **{ranked.iloc[1].host_name}** is second with {ranked.iloc[1].number_of_reviews} reviews. It should also be noted that reviews are not positive or negative reviews, but a count of feedbacks provided for the accommodation.""")


  #################### DEMAND AND PRICE ANALYIS ######################

  st.header("Demand and Price Analysis")

  st.markdown("In this section, we will analyse the demand for Airbnb listings in New York City. We will look at demand over the years since the inception of Airbnb in 2010 and across months of the year to understand seasonlity. We also wish to establish a relation between price and demand. The question we aspire to answer is whether prices of listings fluctuate with demand. We will also conduct a more granular analysis to understand how prices vary by days of the week.")
  st.markdown("To study the demand, since we did not have data on the bookings made over the past year, we will use **number of reviews** variable as the indicator for demand. As per Airbnb, about 50% of guests review the hosts/listings, hence studying the number of review will give us a good estimation of the demand.")

  accommodation = st.radio("Room Type", df.room_type.unique())

  all_accommodation = st.checkbox('All Accommodations')

  demand_df = df[df.last_review.notnull()]
  demand_df.loc[:,'last_review'] = pd.to_datetime(demand_df.loc[:,'last_review'])
  price_corr_df = demand_df

  if all_accommodation:
    demand_df = df[df.last_review.notnull()]
    demand_df.loc[:,'last_review'] = pd.to_datetime(demand_df.loc[:,'last_review'])
  else:
    demand_df = demand_df.query(f"""room_type==@accommodation""")

  fig = px.scatter(demand_df, x="last_review", y="number_of_reviews", color="room_type")
  fig.update_yaxes(title="Nª Reviews")
  fig.update_xaxes(title="Last Review Dates")
  st.plotly_chart(fig)

  st.markdown("The number of unique listings receiving reviews has increased over the years. Highly rated locations also tend to be the most expensive ones. We can see an almost exponential increase in the number of reviews, which as discussed earlier, indicates an exponential increase in the demand.")

  st.markdown("But about the price ? We also can show the same plot, but this time we take into account the **price** feature along years. Again we use **last review dates** to modeling time series in order to achieve a proportion between price over the years. Let's check it out.")

  fig = px.scatter(price_corr_df, x="last_review", y="price", color="neighbourhood_group")
  fig.update_yaxes(title="Price ($)")
  fig.update_xaxes(title="Last Review Dates")
  st.plotly_chart(fig)

  st.markdown("The price smoothly increases along the years if we take into account the number of reviews according the borough. Sightly Manhattan it's most expensive borough followed by Brooklyn, some listings apear also as outliers in past 2 years. Let's take a look again in the number of reviews, but this time we group by boroughs.")

  fig = px.scatter(price_corr_df, x="last_review", y="number_of_reviews", color="neighbourhood_group")
  fig.update_yaxes(title="Nª Reviews")
  fig.update_xaxes(title="Last Review Dates")
  st.plotly_chart(fig)

  st.markdown("The number of reviews for Queens appears more often. We get some insights here. 1)  the room type most sought in Queens is the **private room** (as seen in the previous plot). 2)  the price range in Queens is below Manhattan, so perhaps the Queens contemplate the _\"best of both worlds\"_ being the most cost-effective district.")

  st.markdown("But there is some correlation between reviews increase and prices? Let's check it out.")

  fig = px.scatter(price_corr_df, y="price", x="number_of_reviews", color="neighbourhood_group")
  fig.update_xaxes(title="Nª Reviews")
  fig.update_yaxes(title="Price ($)")
  st.plotly_chart(fig)

  st.markdown("Well, actually does not happens a correlation between reviews and price apparently, the cheaper the more opinions he has. Another point is,  Queens has more reviews than others, which reinforces our theory about being the most cost-effective district.")


  st.header("Most Rated Listings")
  st.markdown("We can slide to filter a range of numbers in the sidebar to view properties whose review count falls in that range.")

  reviews = st.slider('', 0, 12000, (100))

  df.query(f"number_of_reviews<={reviews}").sort_values("number_of_reviews", ascending=False)\
  .head(50)[["number_of_reviews", "price", "neighbourhood", "room_type", "host_name"]]

  st.write("654 is the highest number of reviews and only a single property has it. In general, listings with more than 400 reviews are priced below $ 100,00. Some are between $100,00 and $200,00, and only one is priced above $200,00.")


  ############################# PRICE DISTRIBUTION ###########################

  st.header("Price Distribution")

  st.markdown("Bellow we can select a custom price range from the side bar to update the histogram below and check the distribution skewness.")
  st.write("""Select a custom price range from the side bar to update the histogram below.""")
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


  ############################# CONCLUSIONS ###########################

  st.header("Conclusions")

  st.markdown("Through this exploratory data analysis and visualization project, we gained several interesting insights into the Airbnb rental market. Below we will summarise the answers to the questions that we wished to answer at the beginning of the project:")

  st.markdown("**How do prices of listings vary by location? What localities in NYC are rated highly by guests?** Manhattan has the most expensive rentals compared to the other boroughs. Prices are higher for rentals closer to city hotspots. Rentals that are rated highly on the location by the host also have higher prices")

  st.markdown("**How does the demand for Airbnb rentals fluctuate across the year and over years?** In general, the demand (assuming that it can be inferred from the number of reviews) for Airbnb listings has been steadily increasing over the years.")

  st.markdown("**Are the demand and prices of the rentals correlated?** Average prices of the rentals increase across the year, which correlates with demand.")

  st.header("Limitations")

  st.markdown(" - We did not have data for past years and hence could not compare current rental trends with past trends. Hence, there was an assumption made, particularly in the demand and supply section of the report to understand the booking trends.")

  st.markdown(" Below the data used in this research is available to reproducible research.")

  st.markdown(get_table_download_link(df), unsafe_allow_html=True)

  ################################## FOOTER ##################################

  st.markdown('-----------------------------------------------------')
  st.text('Developed by Toni Esteves - 2020')
  st.text('Mail: toni.esteves@gmail.com')

if __name__ == '__main__':
	main()
