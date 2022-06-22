# FamPay Assignment

This is a project which contains an API service to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

**Framework used to develop REST API** - Django   
**Database** - PostgreSQL  


## Installation Procedure

**1) Docker**  
In order to run the application, you will need docker installed on your system. You can install it from [Here](https://docs.docker.com/engine/install/). Once the download is complete you can run the installer and follow the mentioned steps. 

To check if the installation is complete, write the following command in your command line.
```sh
docker version  
```

**2) Download docker-compose file**  
Next download the docker-compose.yml file from the root directory of this project. 


**3) Migrate**  
Open command prompt and navigate to the folder containing the docker-compose.yml file. Now run the following command in order to download the docker image and to migrate to the database. 
```sh
docker-compose run web python manage.py migrate
```


**4) Create superuser (optional)**  
In order to login to django admin, create a superuser by writing the following command.  
```sh
docker-compose run web python manage.py createsuperuser  
```
Create the required credentials.  


**5) Run the server**  
Type the following command next to run the server on your localhost.   
```sh
docker-compose up    
```
On completion you will see in the command prompt that the server is up and running. You can now go to http://localhost:8000/ and test the API.  


## Working and API Endpoints  

- **Async Calls to YoutubeData API**  
You can see on the command prompt that every 30 secs an API call is made to YoutubeData API and the response is stored in the database. You would see the following statements being printed in the command prompt.  
**Note that the nextPageToken is used to make the next API Call.**    

```sh
Getting Data from youtube API...  
```
```sh
Youtube Data added to Database..  
```
**NOTE:** The default search query to YoutubeData API is "football".  

**1) Paginated Response of the Video Data stored in the Database**  

The API Endpoint - http://localhost:8000/youtube-api/videos will give a list of the stored data in a paginated manner in reverse chronological order of publishedAt attribute. The response received will contain **count** -  indicating number of entries, **next** - link to the next page, **previous** - link to the previous page, **results** - List of all the video data stored in database.   

The default results per page is set to **5**. You can change that by sending a *page_size* query parameter. For example, http://localhost:8000/youtube-api/videos?page_size=8 will give 8 results per page.   

**NOTE:** Maximum page size allowed is 10. Above that it will simply take page size to be 10.  

**2) Search API**  

In order to search using title and description, you can send one or more of these values through query parameters. Example, http://localhost:8000/youtube-api/videos?title=skills&description=goalkeeper - This would return all results which have "skills" in its title **or** "goalkeeper" in its description.  

The Search API has been optimised to search for multiple words by seperating them with a space in between. For example, [http://localhost:8000/youtube-api/videos?title=skills goal](http://localhost:8000/youtube-api/videos?title=skills%20goal) will return all results with title having either of the words "skills" or "goal".  



## Files   
The project contains one app called Youtube. The important files inside it include,  
- **youtubeApiCall.py**  
Handles the creation of a thread to start the async process of calling the YoutubeData API in background every 30 secs and adding the data to the database. **It also handles switching API_KEY in case of quota exhaustion.**     
- **views.py**  
Contains a class-based view called YoutubeData which handles the requests on the API endpoint - http://localhost:8000/youtube-api/videos  
