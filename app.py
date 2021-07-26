from flask import Flask , jsonify,make_response,request #import flask

taches = []
#creation de l'application
app=Flask(__name__)

#creation de la route 
@app.route('/')
def home():
    return 'hello world'

@app.route('/users')
def get_all_user():
    users = ['user1', 'user2','user3']
    return str(users)
    
@app.route('/person')
def get_all_personn():
    users = [
    {
      "email": "espoir@truggle.com",
      "firstname": "Norbert",
      "gender": "M",
      "id": 18,
      "image": "https://i.pravatar.cc/150?u=espoir@truggle.com",
      "lastname": "Truggle",
      "type": "admin"
    },
    {
      "email": "admin@truggle.com",
      "firstname": "Schedule",
      "gender": "M",
      "id": 17,
      "image": "https://i.pravatar.cc/150?u=admin@truggle.com",
      "lastname": "Truggle",
      "type": "admin"
    },
    {
      "email": "jmp@truggle.com",
      "firstname": "Jean-Marie",
      "gender": "M",
      "id": 16,
      "image": "https://i.pravatar.cc/150?u=jmp@truggle.com",
      "lastname": "Preira",
      "type": "teacher"
    },
    {
      "email": "demba.sow@truggle.com",
      "firstname": "Sow",
      "gender": "M",
      "id": 15,
      "image": "https://i.pravatar.cc/150?u=demba.sow@truggle.com",
      "lastname": "Demba",
      "type": "teacher"
    },
    {
      "email": "doudou.faye@truggle.com",
      "firstname": "Doudou",
      "gender": "M",
      "id": 14,
      "image": "https://i.pravatar.cc/150?u=doudou.faye@truggle.com",
      "lastname": "Faye",
      "type": "teacher"
    },
    {
      "email": "moustapha.nder@truggle.com",
      "firstname": "Moustapha",
      "gender": "M",
      "id": 13,
      "image": "https://i.pravatar.cc/150?u=moustapha.nder@truggle.com",
      "lastname": "Nder",
      "type": "teacher"
    },
    {
      "email": "ghislain.akinocho@truggle.com",
      "firstname": "Ghislain",
      "gender": "M",
      "id": 12,
      "image": "https://i.pravatar.cc/150?u=ghislain.akinocho@truggle.com",
      "lastname": "Akinocho",
      "type": "teacher"
    },
    {
      "email": "jmp.preira@truggle.com",
      "firstname": "Jean-Marie",
      "gender": "M",
      "id": 11,
      "image": "https://i.pravatar.cc/150?u=jmp.preira@truggle.com",
      "lastname": "Preira",
      "type": "teacher"
    },
    {
      "email": "maigaissoufou.etu.@truggle.com",
      "firstname": "Issoufou",
      "gender": "M",
      "id": 10,
      "image": "https://i.pravatar.cc/150?u=maigaissoufou.etu.@truggle.com",
      "lastname": "Maiga ",
      "type": "student"
    },
    {
      "email": "aidadiao.etu.@truggle.com",
      "firstname": "Aida",
      "gender": "F",
      "id": 9,
      "image": "https://i.pravatar.cc/150?u=aidadiao.etu.@truggle.com",
      "lastname": "Diao ",
      "type": "student"
    },
    {
      "email": "ouedraogo.etu.@truggle.com",
      "firstname": "Luc",
      "gender": "M",
      "id": 8,
      "image": "https://i.pravatar.cc/150?u=ouedraogo.etu.@truggle.com",
      "lastname": "Ouedraogo ",
      "type": "student"
    }
    ]
    #retourne le tableau
    return make_response(jsonify(users = users)),200

@app.route('/person/<int:id>')
def get_one_personn(id):
    resultat = {'id_person' : id}
    return make_response(jsonify(person= resultat)),200

@app.route('/person/create', methods=['POST'])
def create_personn():
   #get json data
   data = request.get_json()
   return jsonify({'name': data['name']})
   

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)