# Finalproject
Business problem - In current world when a user does a web search for a restaurant in his/her area it returns the point in time rating of business and does not give a comparative rating of venue compared to other venues in the area. For example, a rating of 4 does not give clear picture on how it compares to other restaurant with same rating in the area. Any user who is searching for restaurants on web are end users.

Data to be used: I have mentioned the data that will be used for the project under data folder. I have used below Foursquare API to fetch the venues in a neighborhood:
https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}&query={}
I have also mentioned the final dataset which was created to map the 20 venues on the map with actual rating and comparative rating of the restaurant. This is stored in the Data folder.

Methodology: I have done exploratory data analysis to use the details fetched for each of the venues and then compare the ratings, price and likes for the venue to create a comparative ranking for the venues.

Results: As part of project I have mapped 20 restaurants in Soho neighborhood, in Manhatttan borough based on their comparative rating. Top 10 are highlighted as green and bottom 10 are highlighted as red.

Please refer the final dataset used for plotting in the data section.

Observation: Here we can observe that the comparative rating is done based on actual rating, average price and likes returned for each venue. 
•	We can see restaurants Pasquale Jones and Champion Pizza Soho have same rating and price indicator but different likes count. The comparative rating for Pasquale Jones is higher than Champion Pizza Soho as former had higher number of likes.
•	Take example of restaurants sweetgreen and Ruby’s Café. Even though Ruby’s Café has 5 rating and sweetgreen is rated 3.5 we see that comparative rating of sweetgreen is almost same as Ruby’s Café. This is because the price indicator for Ruby’s Café is higher than sweetgreen.
For my exploratory analysis I have given weightage of 50% to ratings, 40% to the price indicator and 10% to likes.

Conclusion: This exploratory analysis compares the rating of the restaurant, price indicator of the restaurant and number of likes registered for the restaurant and gives a comparative ranking for the restaurants in the area. Here we have given 50% weightage to Rating, 40% weightage to Price indicator and 10% weightage to likes. This goes to show that even a restaurant with slightly higher rating can be less preferred if the price indicator is used in the ranking as cost plays a big part in the decision making on choosing the restaurant.
