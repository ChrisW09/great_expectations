import warnings
from typing import Optional

import numpy as np
import pandas as pd

from great_expectations.execution_engine import (
    PandasExecutionEngine,
    SparkDFExecutionEngine,
)
from great_expectations.execution_engine.sqlalchemy_execution_engine import (
    SqlAlchemyExecutionEngine,
)
from great_expectations.expectations.metrics.map_metric_provider import (
    ColumnMapMetricProvider,
    column_condition_partial,
)
from great_expectations.expectations.metrics.util import parse_value_set


class ColumnValuesNotInSet(ColumnMapMetricProvider):
    condition_metric_name = "column_values.not_in_set"
    condition_value_keys = (
        "value_set",
        "parse_strings_as_datetimes",
    )

    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(
        cls,
        column,
        value_set,
        **kwargs,
    ):
        # no need to parse as datetime; just compare the strings as is
        parse_strings_as_datetimes: bool = (
            kwargs.get("parse_strings_as_datetimes") or False
        )
        if parse_strings_as_datetimes:
            warnings.warn(
                f"""The parameter "parse_strings_as_datetimes" is no longer supported and will be deprecated in a \
future release.  Please update code accordingly.  Moreover, in "{cls.__name__}._pandas()", it is not used.
""",
                DeprecationWarning,
            )

        if value_set is None:
            # Vacuously true
            return np.ones(len(column), dtype=np.bool_)
        if pd.api.types.is_datetime64_any_dtype(column):
            parsed_value_set = parse_value_set(value_set=value_set)
        else:
            parsed_value_set = value_set

        return ~column.isin(parsed_value_set)

    @column_condition_partial(engine=SqlAlchemyExecutionEngine)
    def _sqlalchemy(
        cls,
        column,
        value_set,
        **kwargs,
    ):
        # no need to parse as datetime; just compare the strings as is
        parse_strings_as_datetimes: bool = (
            kwargs.get("parse_strings_as_datetimes") or False
        )
        if parse_strings_as_datetimes:
            warnings.warn(
                f"""The parameter "parse_strings_as_datetimes" is no longer supported and will be deprecated in a \
            future release.  Please update code accordingly.  Moreover, in "{cls.__name__}._sqlalchemy()", it is not used.
            """,
                DeprecationWarning,
            )

        if value_set is None or len(value_set) == 0:
            return True

        return column.notin_(tuple(value_set))

    @column_condition_partial(engine=SparkDFExecutionEngine)
    def _spark(
        cls,
        column,
        value_set,
        **kwargs,
    ):
        # no need to parse as datetime; just compare the strings as is
        parse_strings_as_datetimes: bool = (
            kwargs.get("parse_strings_as_datetimes") or False
        )
        if parse_strings_as_datetimes:
            warnings.warn(
                f"""The parameter "parse_strings_as_datetimes" is no longer supported and will be deprecated in a \
            future release.  Please update code accordingly.  Moreover, in "{cls.__name__}._spark()", it is not used.
            """,
                DeprecationWarning,
            )

        return ~column.isin(value_set)
