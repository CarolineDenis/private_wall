from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO messages (content, sender_id, receiver_id, created_at, updated_at) VALUES (%(content)s,%(sender_id)s,%(receiver_id)s,NOW(),NOW())"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all_for_user(cls,data):
        query = "SELECT * FROM messages WHERE receiver_id=%(id)s;"
        results =  connectToMySQL(DATABASE).query_db(query,data)
        new_list_messages =[]
        for b in results:
            new_list_messages.append(cls(b))
        return new_list_messages

    @classmethod
    def delete_message(cls, data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all_sent(cls,data):
        query = "SELECT * FROM messages WHERE sender_id=%(id)s;"
        results =  connectToMySQL(DATABASE).query_db(query,data)
        new_list_messages =[]
        for b in results:
            new_list_messages.append(cls(b))
        return new_list_messages