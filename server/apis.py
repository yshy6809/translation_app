from server import api
from server.resources import GetFile, PostFile, ProjectResource, TextflowResource, Random


api.add_resource(GetFile, "/api/file/get/<int:file_id>")
api.add_resource(PostFile, "/api/file/upload/<int:project_id>")
api.add_resource(ProjectResource, "/api/project/<int:project_id>")
api.add_resource(TextflowResource, "/api/text_flow/<int:id>")
api.add_resource(Random, "/api/random")




