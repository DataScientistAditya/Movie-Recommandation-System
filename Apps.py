#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, redirect, render_template, url_for



Final_Data = pd.read_csv('Final_Data.csv')


Final_Data.head()


Final_Data['original_title'] =Final_Data['original_title'].map(lambda x: x.lower())
Final_Data['Actor1'] =Final_Data['Actor1'].map(lambda x: x.lower())
Final_Data['Actor2'] =Final_Data['Actor2'].map(lambda x: x.lower())
Final_Data['Actor3'] =Final_Data['Actor3'].map(lambda x: x.lower())
Final_Data['Director_Name'] =Final_Data['Director_Name'].map(lambda x: x.lower())
Final_Data['genres_list'] = Final_Data['genres_list'].map(lambda x: x.lower())


Cm = CountVectorizer().fit_transform(Final_Data['Comb'])


Cs = cosine_similarity(Cm)



Recomanded_Movie = []
def Recomanded_Movies(Title):
    if len(Recomanded_Movie)>0:
        Recomanded_Movie.clear()
    Movie_id = Final_Data[Final_Data.original_title == Title]['id'].index[0]
    Cs_Score = list(enumerate(Cs[Movie_id]))
    Sorted_Score = sorted(Cs_Score, key= lambda x: x[1], reverse=True)
    j = 0
    for item in Sorted_Score:
        
        Movie_ID = Final_Data['original_title'][Final_Data.index == item[0]].values
        if len(Movie_ID)==1:
            Recomanded_Movie.append(Movie_ID[0])
            j = j +1
            if j>6:
                break



app = Flask(__name__,template_folder='Templates')


# In[ ]:


Recomanded_Actor = []
def Recomanded_Actors(Actor_Name):
    if len(Recomanded_Actor)>0:
        Recomanded_Actor.clear()
    if Final_Data.Actor1[Final_Data.Actor1 == Actor_Name].count()>0:
        Actor_Name1 = Final_Data[Final_Data.Actor1 == Actor_Name]['id'].index[0]
        Cs_Score = list(enumerate(Cs[Actor_Name1]))
        Sorted_Score = sorted(Cs_Score, key= lambda x: x[1], reverse=True)
        j = 0
        for item in Sorted_Score:
            Actor_NAME = Final_Data['original_title'][Final_Data.index == item[0]].values
            if len(Actor_NAME)==1:
                Recomanded_Actor.append(Actor_NAME[0])
                j = j +1
                if j>6:
                    break 
    elif Final_Data.Actor2[Final_Data.Actor2 == Actor_Name].count()>0:
        Actor_Name2 = Final_Data[Final_Data.Actor2 == Actor_Name]['id'].index[0]
        Cs_Score = list(enumerate(Cs[Actor_Name2]))
        Sorted_Score = sorted(Cs_Score, key= lambda x: x[1], reverse=True)
        j = 0
        for item in Sorted_Score:
            Actor_NAME = Final_Data['original_title'][Final_Data.index == item[0]].values
            if len(Actor_NAME)==1:
                Recomanded_Actor.append(Actor_NAME[0])
                j = j +1
                if j>6:
                    break 
        return Cs_Score
    elif Final_Data.Actor3[Final_Data.Actor3 == Actor_Name].count()>0:
        Actor_Name3 = Final_Data[Final_Data.Actor3 == Actor_Name]['id'].index[0]
        Cs_Score = list(enumerate(Cs[Actor_Name3]))
        Sorted_Score = sorted(Cs_Score, key= lambda x: x[1], reverse=True)
        j = 0
        for item in Sorted_Score:
            Actor_NAME = Final_Data['original_title'][Final_Data.index == item[0]].values
            if len(Actor_NAME)==1:
                Recomanded_Actor.append(Actor_NAME[0])
                j = j +1
                if j>6:
                    break
    elif Final_Data.Director_Name[Final_Data.Director_Name == Actor_Name].count()>0:
        Dirct_Name = Final_Data[Final_Data.Director_Name == Actor_Name]['id'].index[0]
        Cs_Score = list(enumerate(Cs[Dirct_Name]))
        Sorted_Score = sorted(Cs_Score, key= lambda x: x[1], reverse=True)
        j = 0
        for item in Sorted_Score:
            Actor_NAME = Final_Data['original_title'][Final_Data.index == item[0]].values
            if len(Actor_NAME)==1:
                Recomanded_Actor.append(Actor_NAME[0])
                j = j +1
                if j>6:
                     break
    elif Final_Data.genres_list[Final_Data.genres_list == Actor_Name].count()>0:
        Genre_ID = Final_Data[Final_Data.genres_list == Actor_Name]['id'].index[0]
        Cs_Score = list(enumerate(Cs[Genre_ID]))
        Sorted_Score = sorted(Cs_Score, key= lambda x: x[1], reverse=True)
        j = 0
        for item in Sorted_Score:
            Genre_NAME = Final_Data['original_title'][Final_Data.index == item[0]].values
            if len(Genre_NAME)==1:
                Recomanded_Actor.append(Genre_NAME[0])
                j = j +1
                if j>6:
                    break
        
            
        
    else:
        print('N/A')       


# In[ ]:


from omdbapi.movie_search import GetMovie


# In[ ]:


Final_Data.shape


# In[ ]:


Final_Data.tail(20)


# In[ ]:


def Poster(Title):
    movie = GetMovie(title=Title, api_key='457c3e6d')
    movie = GetMovie(title= Title, api_key='457c3e6d', plot='full')
    Url =movie.get_data('Poster')
    for i in Url:
        poster = Url[i]
    return poster


# In[ ]:


Titel_Ratings = []
def Titel_Fetch(Titles):
    if len(Titel_Ratings)>0:
        Titel_Ratings.clear()
    movie = GetMovie(title=Titles, api_key='457c3e6d')
    movie = GetMovie(title= Titles, api_key='457c3e6d', plot='full')
    Titel_Rating =movie.get_data('Title','Year','Director','Actors','imdbRating')
    for i in Titel_Rating:
        Titel_Ratings.append(Titel_Rating[i])
    return Titel_Ratings


# In[ ]:


Recomanded_Movie_Posters = []
def Recomandation_Posters_Movie():
    if len(Recomanded_Movie_Posters)>0:
        Recomanded_Movie_Posters.clear()
    for i in Recomanded_Movie:
        if Poster(i) != 'N/A' and Poster(i) != 'key not found!':
            Recomanded_Movie_Posters.append(Poster(i))
    return Recomanded_Movie_Posters


# In[ ]:


List_Url = []
def List_Poster_BY_Actor_Director(Name):
    if len(List_Url)>0:
        List_Url.clear()
    Recomanded_Actors(Name)
    for i in Recomanded_Actor:
        List_Url.append(Poster(i))
    return List_Url


# In[ ]:


@app.route('/')
def home():
    return render_template('index.html')


# In[ ]:


@app.route('/Movies',methods=['POST', 'GET'])
def Movies():
    Movie_Nm = request.form["Movie_Name"]
    Movie_Nm = Movie_Nm.lower()
    Int = Final_Data['id'][Final_Data['original_title'] == Movie_Nm].count()
    Act1 = Final_Data.Actor1[Final_Data.Actor1 == Movie_Nm].count()
    Act2 = Final_Data.Actor2[Final_Data.Actor2 == Movie_Nm].count()
    Act3 = Final_Data.Actor3[Final_Data.Actor3 == Movie_Nm].count()
    Dict_Name = Final_Data.Director_Name[Final_Data.Director_Name == Movie_Nm].count()
    Genre_nm = Final_Data.genres_list[Final_Data.genres_list == Movie_Nm].count()
    if Int>0:
        Movie_Poster = Poster(Movie_Nm)
        Recomanded_Movies(Movie_Nm)
        Recomandation_Posters_Movie()
        Titel_Fetch(Movie_Nm)
        return render_template('index.html',url = Movie_Poster,rcm1 = Recomanded_Movie_Posters[0],
                               rcm2 = Recomanded_Movie_Posters[1], rcm3 = Recomanded_Movie_Posters[2],
                               Title = "Title: ",Name_T =Titel_Ratings[0], Year ="Year: ",YY = Titel_Ratings[1],
                               Director = "Director: ",Name_D = Titel_Ratings[2],Actors ='Actors: ',Name_A = Titel_Ratings[3],
                               IMDB = "Ratings: ", Rating = Titel_Ratings[4] )
    elif Act1>0 or Act2>0 or Dict_Name>0 or Genre_nm>0:
        List_Poster_BY_Actor_Director(Movie_Nm)
        
        return render_template('index.html',rc1 = List_Url[0],rc2 = List_Url[1],rc3 = List_Url[2], 
                               rc4 = List_Url[3],rc5 = List_Url[4],rc6 =List_Url[5])
        
    else:
        return render_template('index.html',Your_Movie = "Not Available")


# In[ ]:



if __name__ == "__main__":
    app.run(debug=False)

