# Uni Mannheim information retrieval project

To get a better understanding of the tasks and the dataset you can look at the following papers and documents:

- https://www.cs.rit.edu/~dprl/ARQMath/arqmath-resources.html
- https://www.cs.rit.edu/~rlaz/files/ARQMath_2022_Overview_WorkingNotes.pdf
- http://ceur-ws.org/Vol-2936/paper-01.pdf
- https://link.springer.com/content/pdf/10.1007/978-3-030-99739-7.pdf (page 408-414)
- The README_DATA.md is helpful to get a better understanding of the concrete dataset structure (also see the class
  diagram)

## Important notes

- We don't need to install the LaTeXML tool since we don't have to preprocess the dataset. The LaTeXML tool is only
  needed to scrape the comments from the MathStackExchange snapshot. Therefore, the only thing you need to install
  is the prepared conda environment (more dependencies will be added in the future)
- You can download the ARQMath dataset from the google drive
  folder (https://drive.google.com/drive/folders/1YekTVvfmYKZ8I5uiUMbs21G2mKwF9IAm). Copy the files to
  the `arqmath_dataset` directory as shown in the screenshot. The concrete directory structure may change in the
  future ![image](example_arqmath_directory.png)
- In the `understand_the_dataset` jupyter notebook you can get a better understanding of the ARQMth dataset and you can explore the dataset yourself. The   code used to read the dataset is copied from the ARQMath GitHub repo (https://github.com/ARQMath/ARQMathCode).
- The code for preprocessing the dataset and creating an index for PyTerrier can be found in
  this [repo](https://gitlab.com/dprl/pt-arqmath/-/tree/main/). Only the code for translating mathematical symbols into a text representation was copied   and used.


## Project requirements

- We can use libraries that have already implemented concrete functions that are used in information retrieval models (
  e.g. scikit-learn TfidfVectorizer and PyTerrier).
- Jupyter notebooks are used as a frontend to run the retrieval pipeline. The model implementation itself is in the `src` folder.
- Still not clear if we need to write a project report.
- Project presentation on December 7, 2022
- The overall goal should be to compare different models (old approaches vs new approaches).

## Implemented models, pre-processors and post-processors

### Implemented models

- S-Bert with question title embedding
- S-Bert cross encoder
- General PyTerrier model for ad-hoc retrieval. The used retrieval model can be configured via a parameter and all retrival models that are provided by     PyTerrier can be used (e.g. TF, TF-IDF, BM25, Hiemstra-LM). For a complete list of all available models take a look [here](http://terrier.org/docs/current/javadoc/org/terrier/matching/models/package-summary.html). The path to the PyTerrier index must be handled carefully, as  the index will be loaded if an index already exists under the specified path. This is done to improve performance because the index creation is very computationally intensive. In general, an index that contains all ARQMath answers can be used because the model always checks whether the returned results from the Pyterrier index are part of the documents passed to the model.
- Latent Dirichlet Allocation: The number of topics on which the model is trained can be configured via a parameter. Currently there are results for 50 and 200 topics

### Implemented post-processors

- Top-K filer: This filter returns the top k results for each topic. The parameter k ist set to 1000 by default because the ARQMath evaluation expects 1000 results per topic.

- Answer score retriever for questions: For each ranked question the top answer is returned together with the score from the question.

### Runner

The implemented runner executes the passed pipeline and saves the ranking results to a .tsv file. This .tsv file is in the expected format for the ARQMath evaluation scripts.

## Environment

You can create a conda environment out of the ir.yml
see [conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment)
on Building Identical Environments for details. The environment includes Pyterrier which needs a JAVA-Runtime so make
sure OpenJDK or any Version of Java is installed and can be reached by any program.

If you get an error regarding JAVA_HOME, you might have to check if your environment variables are set up correctly. To
do that, open the anaconda command line and check with `java --version`, which Java Version Anaconda is using. If you
get an error message here, you might want to check, if you have JDK installed. Furthermore with `echo %JAVA_HOME%` check
where you have to set the JAVA_HOME variable path to. Now set a new Environment variable to "JAVA_HOME" with the path
from earlier and also add the path to the "path" variable. Restart your command line and set up the environment again.

## Architecture
In the following you'll find a short overview over the architecture to use when coding your Pipeline and Models. All these classes
will be given to you. The idea is to inherit them to define your Model and Pipeline.
### Model-Class:
- init(model_config: dict) # model_config_dict defined elsewhere in a config file
  - Model initialization steps
- forward(queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[Tuple[Topic, Union[Question, Answer], float]]
  - here you write your model code

### PostProcessor
- forward(queries: List[Topic], documents: List[Tuple[Topic, Union[Question, Answer], float]]) -> List[Topic, Tuple[Union[Question, Answer], float]]
  - here you write the code for a post processor that takes ranked documents and returns another set of ranked documents. For example a filter.

### PreProcessor
- forward(queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[Union[Question, Answer]]
  - here you write the code for a pre processor that takes documents and returns another list of documents. For example a filter.

### Runner:
This class will be predefined and used for evaluating and running your pipeline so you won't have to tinker with it.
- init(Pipeline, n=1) -> Data loading, Pipeline init
- pipeline.run()
- Rank & Sort & Evaluate

### Pipeline-Class:
init():
- Init all models
run() -> List[Tuple[Answer, float]]:
- Chain models, apply processing

**The following example is only for *VISUAL UNDERSTANDING* purposes of the architecture and does not pose a real world use case!!!**
Pipeline e.g.: PreProcessing -> Model (Binary Tag Retrieval) -> Model (Question Retrieval) -> Model(Answer retrieval Title) -> Model (Cross encoding) -> Model (Top K Filtering)
													             					| -> Answer Retrieval Formulas ->

## Further Info

For further Information please consult the Jupyter Notebooks in the notebooks folder. There are several notebooks that that were used to better understan the dataset and the evaluation.
