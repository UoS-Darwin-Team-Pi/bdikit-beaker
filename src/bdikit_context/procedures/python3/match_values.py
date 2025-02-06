import bdikit as bdi
value_mappings = bdi.match_values({{ dataset }}, column_mapping={{ column_mapping }}, target="{{ target }}", method="{{ method }}")
value_mappings.to_markdown()