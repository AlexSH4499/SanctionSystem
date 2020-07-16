from flask import Flask, request, jsonify, make_response,g,json
import typing
import Sanction
import sanctioned_data_parser
import sqlite3 as sql

app = Flask(__name__)

import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sanctioned.db")


DATABASE = db_path

def get_db():
    db = getattr(g,'_database', None)

    if not db:
        db = g._database = sql.connect(DATABASE)
    db.row_factory = sql.Row# returns all rows as named tuples
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g,'_database', None)

    if db:
        db.close()

def make_dicts(cursor, row):
    return {(cursor.description[idx][0], value) for idx, value in enumerate(row)}

def query_db(query, args=(), one= False):
    cur = get_db().execute(query,args)
    rv = cur.fetchall()

    res = []
    for r in rv:
        print(tuple(r))
        indv, org, country =tuple(r)
        res.append({'Individuals':indv,'Organizations':org,'Countries':country})
    # cur.close()
    # NEVER  CLOSES THE CURSOR, MIGHT BE MEMORY LEAK
    return res

def test_data():
    data = [{'name':'Kristopher Doe',
              'sanctioned':True},
            {'name':'Royal Arctic Line',
              'sanctioned':True},
            ]
    return data

@app.route('/', methods=['GET','POST'])
def home():

    if request.method == 'POST':
        pass

    if request.method == 'GET':
        pass

    return "<h1>Sanctions Archive</h1><p>This site is a prototype API for verifying sanctioned indivs.</p>"

@app.route('/sanctioned/individuals/',methods=['GET'])
def get_sanctioned_individuals():
    sanctioned=[{ "name": di['Individuals'],'Sanctioned' : True } for di in query_db("select * from sanctioned")]

    return jsonify(sanctioned)

@app.route('/sanctioned/organizations/',methods=['GET'])
def get_sanctioned_organizations():
    sanctioned=[{ "name": di['Organizations'],'Sanctioned' : True } for di in query_db("select * from sanctioned")]

    return jsonify(sanctioned)

@app.route('/sanctioned/countries/',methods=['GET'])
def get_sanctioned_countries():
    sanctioned=[{ "name": di['Countries'],'Sanctioned' : True } for di in query_db("select * from sanctioned")]

    return jsonify(sanctioned)

@app.route('/sanctioned/individuals/<string:name>',methods=['GET'])
def get_sanctioned_individual(name):
    sanctioned=[]
    people, countries, orgs =sanctioned_data_parser.parsed_data_params()
    
    #check here if in the sanctioned list or not
    for row in query_db('select * from sanctioned'):
        sanctioned.append(row[people])

    status, prob = Sanction.is_sanctioned(name, sanctioned)
    
    return jsonify({people : name,'Sanctioned':status , 'Probability':prob})


@app.route('/sanctioned/organizations/<string:name>',methods=['GET'])
def get_sanctioned_organization(name):
    sanctioned=[]
    people, countries, orgs =sanctioned_data_parser.parsed_data_params()
    
    #check here if in the sanctioned list or not
    for row in query_db('select * from sanctioned'):
        sanctioned.append(row[orgs])

    status, prob = Sanction.is_sanctioned(name, sanctioned)
    
    return jsonify({orgs : name,'Sanctioned':status , 'Probability':prob})


@app.route('/sanctioned/countries/<string:name>',methods=['GET'])
def get_sanctioned_country(name):
    sanctioned=[]
    people, countries, orgs =sanctioned_data_parser.parsed_data_params()
    
    #check here if in the sanctioned list or not
    for row in query_db('select * from sanctioned'):
        sanctioned.append(row[countries])

    status, prob = Sanction.is_sanctioned(name, sanctioned)
    
    return jsonify({countries : name,'Sanctioned':status , 'Probability':prob})


@app.route('/sanctioned/',methods=['GET'])
def get_sanctioned():

    all = [di for di in query_db('select * from sanctioned')]

    return jsonify(all)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error':'Not Found'}),404)


if __name__ == "__main__":
    app.run(debug=True)