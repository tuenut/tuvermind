__all__ = ["SWAGGER_SETTINGS"]

SWAGGER_SETTINGS = {
    "DEFAULT_MODEL_RENDERING": "example",
    "EXPAND_RESPONSES": "200, 201",
    "REQUIRED_PROPS_FIRST": True,
    "DEFAULT_FIELD_INSPECTORS": [
        "drf_yasg.inspectors.CamelCaseJSONFilter",
        "drf_yasg.inspectors.InlineSerializerInspector",
        "drf_yasg.inspectors.RelatedFieldInspector",
        "drf_yasg.inspectors.ChoiceFieldInspector",
        "drf_yasg.inspectors.FileFieldInspector",
        "drf_yasg.inspectors.DictFieldInspector",
        "drf_yasg.inspectors.SimpleFieldInspector",
        "drf_yasg.inspectors.StringDefaultFieldInspector",
    ],
    "OPERATIONS_SORTER": "alpha",
}
