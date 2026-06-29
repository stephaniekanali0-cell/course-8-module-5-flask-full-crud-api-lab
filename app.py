from flask import Flask, jsonify, request

#This is to instanciate the app
app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Defines the end points
@app.route("/events", methods=["POST"])
def create_event():

    # Get info from the client to add it to our server
    data = request.get_json()
    #Increment the ID

    new_event = Event( len(events)+ 1, data["title"] )

    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

    
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    
    # First see if it is there
    event = next ((event for event in events if event.id == event_id), None)

    data = request.get_json()

    if not event:
        return jsonify("Event not found"), 404

    if "title" in data:
        event.title =data["title"]
    return jsonify(event.to_dict()), 200 



@app.route("/events/<int:event_id>", methods=["DELETE"])
#Use Id to get the event you want to delete first
def delete_event(event_id):

    event = next((event for event in events if event.id == event_id), None)

    if not event:
        return jsonify("Event not found"),404
    
    #filter the events that are there already using list compression
    events[:] = [event for event in events if event.id != event_id]

    return jsonify("Event deleted successfuly"),204

    
if __name__ == "__main__":
    app.run(debug=True)
