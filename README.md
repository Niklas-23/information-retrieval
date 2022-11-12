# Uni Mannheim information retrieval project

To get a better understanding of the tasks and the dataset you can look at the following papers and documents:

- https://www.cs.rit.edu/~dprl/ARQMath/arqmath-resources.html
- https://www.cs.rit.edu/~rlaz/files/ARQMath_2022_Overview_WorkingNotes.pdf
- http://ceur-ws.org/Vol-2936/paper-01.pdf
- https://link.springer.com/content/pdf/10.1007/978-3-030-99739-7.pdf (page 408-414)
- The README_DATA.md is helpful to get a better understanding of the concrete dataset structure (also see the class
  diagram)

Current state of understanding:

- We don't need to install the LaTeXML tool since we don't have to preprocess the dataset. The LaTeXML tool is only
  needed to scrape the comments from the MathStackExchange snapshot. Therefore, the only thing you need to install
  is the prepared conda environment (more dependencies will be added in the future)
- You can download the ARQMath dataset from the google drive
  folder (https://drive.google.com/drive/folders/1YekTVvfmYKZ8I5uiUMbs21G2mKwF9IAm). Copy the files to
  the `arqmath_dataset` directory as shown in the screenshot. The concrete directory structure may change in the
  future ![image](example_arqmath_directory.png)
- In the `understand_the_dataset` jupyter notebook I tried to read and print the dataset. Currently, only the memory
  address is printed (don't know why, further investigation needed). However, it worked to generate html
  pages (see html_pages directory). The code used to read the dataset is copied from the ARQMath GitHub
  repo (https://github.com/ARQMath/ARQMathCode).
- Code for preprocessing the dataset and creating an index for PyTerrier can be found in
  this [repo](https://gitlab.com/dprl/pt-arqmath/-/tree/main/).

Open questions for the coaching session (feel free to add questions if you have any):

- Can we use libraries that have already implemented concrete functions that are used in information retrieval models (
  e.g. scikit-learn TfidfVectorizer) or should we implement all of them ourselves?
- What is about PyTerrier as this is an information retrieval framework and provides a lot of ready-to-use information
  retrieval models. I think it's still difficult to get everything working due to the complex dataset.
- Do we need a frontend or cli? I hope not and would prefer to use jupyter notebooks as a kind of frontend to run
  retrieval models.
- Do we need to write a project report? If yes, how many pages? What should be the content of the report, should we also
  explain the models or just evaluate our results?

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

### PostProcessor
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

For further Information please consult the Jupyter Notebooks in the notebooks folder
