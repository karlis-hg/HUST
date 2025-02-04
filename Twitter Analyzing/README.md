## Final kibana visualization found on report: https://github.com/karlis-hg/HUST/blob/main/Twitter%20Analyzing/report-Xproblem.pdf  

### Spark-dataProcessing&Cleaning  
### GCSBucket-dataStoring  
### ElasticsearchKibana-dataIndexing&Pushing to Visualizing
3 steps for processing Twitter data:  
Bot Account Removal: Identified and removed bot accounts to ensure data integrity.  
Geo-bert Model for Location Prediction: Used Geo-bert for geographical predictions from tweet content and openstreetmap geo api for decoding location field.  
Sentiment Analysis of Tweets: Analyzed tweets for sentiment to understand user opinions and emotions.  

## Data Structure 

### Object: user
| Field         | Data type     | Description               |
|---------------|---------------|---------------------------|
|id             |Int            |Twitter ID                 |
|username       |String         |Twitter tag                |
|displayName    |String         |Twitter Display Name       |
|url            |String         |Link to user's twitter     |
|intro          |String         |Twitter biography          |
|join_date      |String         |Date and time joined       |
|location       |String         |User's location            |
|friends_count  |Int            |Number of friends          |
|favorite_count |Int            |Number of favorites        |
|followers_count|Int            |Number of followers        |
|media_count    |Int            |Number of medias uploaded  |
|status_count   |Int            |Number of status uploaded  |
|listed_count   |Int            |Number of list             |
|is_protected   |Boolean        |Is the account protected?  |
|is_verified    |Boolean        |Is the account verified?   |
|ref            |Object         |Reference links            |
### Array of object: tweets
| Field         | Data type     | Description               |
|---------------|---------------|---------------------------|
|user           |String        |Username of tweet's uploader|
|tweet_id       |Int            |ID of tweet                |
|tweet_content  |String         |Content of tweet           |
|tweet_created_at|String      |Upload date and time of tweet|
|like_count     |Int            |Number of likes            |
|retweet_count  |Int            |Number of retweets         |
|comment_count  |Int            |Number of comments         |
|view_count     |Int            |Number of views            |
|quote_count    |Int            |Number of quotes           |
|hashtags       |Array          |All hashtags used          |
|place          |String         |Upload location of tweet   |
|mentioned_users|Array          |Users mentioned in tweet   |

### Stage 1:  
Crawling  
### Stage 2:  
Preprocessing including check Bot account and Tweets proccessing  
### Stage 3:  
Analysing including labelling Continent tag of user by using Geo decoding Nominatim with Geo-bert tweet-location prediction and Tweets Sentiment Analysising
