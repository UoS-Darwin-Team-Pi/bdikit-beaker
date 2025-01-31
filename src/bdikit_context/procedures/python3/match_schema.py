import bdikit as bdi
column_mappings = bdi.match_schema({{ dataset }}, target="{{ target }}", method="{{ method }}")
column_mappings.to_markdown()