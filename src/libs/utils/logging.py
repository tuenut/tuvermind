from typing import Union


def combine_with(modifier: Union[all, any], inverse=False):
    """Helper function to create complex  logger filters in functional style."""

    def combine_filters(*filters):
        def combined_filter(record):
            result = modifier([fn(record) for fn in filters])
            return not result if inverse else result

        return combined_filter

    return combine_filters


not_any_of = combine_with(any, inverse=True)
