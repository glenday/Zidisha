from a_Model import ModelIt
from flask import render_template, request
from app import app
import pymysql as mdb

db = mdb.connect(user="root", host="localhost", db="world",  charset='utf8')

@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html",
  title = 'Home', user = { 'nickname': 'Miguel' },
  )

@app.route('/db')
def cities_page():

  with db: 
    cur = db.cursor()
    cur.execute("SELECT Name FROM City LIMIT 15;")
    query_results = cur.fetchall()
  cities = ""
  for result in query_results:
    cities += result[0]
    cities += "<br>"
  return cities

@app.route("/db_fancy")
def cities_page_fancy():
#  db = mdb.connect(user="root", host="localhost", db="world",  charset='utf8')
  with db:
    cur = db.cursor()
    cur.execute("SELECT Name, CountryCode, Population FROM City ORDER BY Population LIMIT 15;")

    query_results = cur.fetchall()
  cities = []
  for result in query_results:
    cities.append(dict(name=result[0], country=result[1], population=result[2]))
  return render_template('cities.html', cities=cities)

@app.route('/input')
def cities_input():
  return render_template("input.html")

@app.route('/output')
def cities_output():
  #pull 'ID' from input field and store it
  city = request.args.get('ID')

  with db:
    cur = db.cursor()
    #just select the city from the world_innodb that the user inputs
    cur.execute("SELECT Name, CountryCode,  Population FROM City WHERE Name='%s';" % city)
    query_results = cur.fetchall()
  
  cities = []
  the_result = 0
  if(query_results):
    for result in query_results:
      cities.append(dict(name=result[0], country=result[1], population=result[2]))
  
    #call a function from a_Model package. note we are only pulling one result in the query
    pop_input = cities[0]['population']
    the_result = ModelIt(city, pop_input)
  else:
    cities = [dict(name='Error: city not in database. Please try again.')]
  
  return render_template("output.html", cities = cities, the_result = the_result)
