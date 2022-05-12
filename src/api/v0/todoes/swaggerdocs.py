from drf_yasg.utils import swagger_auto_schema
from api.swagger.custom import ExcludeParametersAutoSchema


todoes_list_docs = swagger_auto_schema(
    operation_summary="Get list of todoes."
)

todoes_create_docs = swagger_auto_schema(
    operation_summary="Create new todo.",
    operation_description="""\
You can set title, description, dates of start and end task, also set of \
reminders. Other parameters will set automatically.
For change status - use special actions."""
)

todoes_partial_update_docs = swagger_auto_schema(
    operation_summary="Partial update TODO.",
    operation_description="You can not change a completed task."
)

todoes_destroy_docs = swagger_auto_schema(
    operation_summary="Delete TODO.",
)

todoes_retrieve_docs = swagger_auto_schema(
    operation_summary="Retrieve TODO by `id`."
)

todoes_update_docs = swagger_auto_schema(
    operation_summary="Edit task.",
    operation_description="You can not change a completed task."
)

todoes_complete_docs = swagger_auto_schema(
    operation_summary="This is the only way to complete task.",
    operation_description=""
)

todoes_today_docs = swagger_auto_schema(
    auto_schema=ExcludeParametersAutoSchema,
    operation_summary="Shortcut to get tasks list filtered by today date.",
    operation_description=""
)
