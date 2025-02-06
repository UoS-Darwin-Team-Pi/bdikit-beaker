import bdikit as bdi
gdc_acceptable_values = bdi.preview_domain("gdc", column="{{ column }}")
gdc_acceptable_values.to_markdown()