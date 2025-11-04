from flask_restful import Resource

class V2GetItemsResource(Resource):
    def get(self):
        return {"items": ["item1", "item2", "item3", "item4"]}
    