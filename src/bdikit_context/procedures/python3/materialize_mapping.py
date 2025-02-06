import bdikit as bdi
harmonized_df = bdi.materialize_mapping({{ dataset }}, mapping_spec={{ mapping_spec }})
harmonized_df.to_csv("{{ output_file }}", index=False)
harmonized_df.head(10).to_markdown()