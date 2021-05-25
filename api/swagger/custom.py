from drf_yasg.inspectors import SwaggerAutoSchema


class ExcludeParametersAutoSchema(SwaggerAutoSchema):
    def get_query_parameters(self):
        return self.get_pagination_parameters()
