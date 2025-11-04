from flask_restful import Resource

class V1GetItemsResource(Resource):
    def get(self):
        return {"items": ["item1", "item2", "item3"]}
    