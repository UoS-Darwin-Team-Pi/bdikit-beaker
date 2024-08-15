# bdikit-example

This is an example Beaker context for [NYU's BDIKit library](https://bdi-kit.readthedocs.io/en/latest/index.html).

First, add your OpenAI API key to the environment:

```
export OPENAI_API_KEY=your key goes here
```

Then use `docker compose` to build and run the BDIKit Beaker context:

```
docker compose build
docker compose up -d
```

Navigate to `localhost:8888` and select the `bdikit_context`. You can experiment with the following script:

```
1. Load the file dou.csv as a dataframe and subset it to the following columns: Country, Histologic_type, FIGO_stage, BMI, Age, Race, Ethnicity, Gender, Tumor_Focality, Tumor_Size_cm.
2. Please match this to the gdc schema using the two_phase method.
```