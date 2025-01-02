## RestAPIAutomationPython

### <u>Project Overview:</u>
RestAPIAutomationPython is a Python-based project built using version 3.9.9. It provides an automation framework for REST API testing, leveraging tools like Behave for behavior-driven development (BDD) and Allure for detailed reporting. This framework is structured to support efficient, maintainable, and scalable test automation.

---

### <u>Table of Contents:</u>
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Reports](#reports)

---

### <u id="features">Features:</u>
- Behavior-Driven Development (BDD) support using Behave.
- Comprehensive reporting with Allure.
- Modular structure for easy scalability and maintenance.
- Configuration-driven setup using `behave.ini`.
- Implementation for multiple api authentication mechanisms like Oauth and Oauth2.0.
- Implementation for multiple assertion types.
- Ease of use and setup.
- Support for webservice orchestration.
- Capable of supporting multiple applications with different hosts.
- Ready to go for realtime corporate projects.
- Requires integration with CI/CD tools.

---

### <u id="project-structure">Project Structure:</u>
```
RestAPIAutomationPython/
|
|-- application/                                # application-specific source code
|   |-- apischema/                              # directory containing the schema of every api based on environment
|       |-- dev/                                # environment
|           |-- api1/                           # api Name
|               |-- request.json                # request schema of the api
|               |-- testdata.yml                # test data for all scenarios associated with the api.
|               |-- validation_mapping.yml      # validation data for api response associated with the api
|   |-- config/
|       |-- envconfig.yml                       # file containing configurations for all environments
|   |-- features/
|       |-- steps/
|               |-- application_steps.py
|               |-- __init__.py
|       |-- environment.py                      # python file for hooks for features within the application directory
|       |-- feature_dir/                        # directory containing feature files for a particular feature
|               |-- feature1.yml                # feature file
|-- commons/                                    # Shared utilities and resources
|   |-- config/
|       |-- logging_config.py
|   |-- utils/
|       |-- file_handlers.py
|       |-- __init__.py
|   |-- steps/
|       |-- GivenTestSteps.py
|       |-- WhenTestSteps.py
|       |-- ThenTestSteps.py
|       |-- __init__.py
|   |-- service_manager/
|       |-- assertion_manager.py
|       |-- request_manager.py
|       |-- response_manager.py
|       |-- __init__.py
|   |-- __init__.py
|-- behave.ini                                  # Behave configuration file
|-- requirements.txt                            # Project dependencies
|-- runner.py                                   # Script to execute tests
|-- README.md                                   # Project documentation
```

---

### <u id="setup-instructions">Setup Instructions:</u>

1. **Install Python 3.9.9**
   - Ensure Python 3.9.9 is installed on your system.

2. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd RestAPIAutomationPython
   ```

3. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

### <u id="usage">Usage:</u>

- ***Environment Setup***:

     Environment setup for any api testing project in this framework happens at 2 levels:
  1. First is the environment setup. Directories need to be created for every available environment in
     which the application scenarios need to be executed. These directories for individual environments
     are required to be placed under root/<application>/apischema/. Please refer to the project structure
     for more info.
  2. Secondly the envconfig.yml which is stored at the root/<application>/config/. The file is
     supposed to contain data which remains common for all api s across an environment. The file can
     store similar data for multiple different environment. Please refer to the project structure for
     more info.

- ***Data Setup***:
     
     Data setup specific to an individual api happens in 3 different files:
  1. request.json file: This file contains the generalised json structure of the api with some or all the
     values parameterized. These values may be headers, query parameters, auth parameters or response body
     parameters. These parameterized values should be in the format '"key": "(parameter_name)"'. Please
     refer to the project structure for more info.
  2. testdata.yml file: This file contains the datasets for all the scenarios in which the api was used.
     Each individual dataset contains execution data and expected values in the response for the sake of
     assertions.
  3. validation_mapping.yml file: This file contains datasets for mapping data api response specific to
     each scenario where the api is called. The mapping contains parameter against its corresponding json
     path in the api response.
     
  For more information please refer to the project structure.

- ***Running Tests***:

     Execution of the test feature file can happen in two ways:
  1. Using the runner.py file: Executing the runner.py file is fairly simple and self-explanatory. This
     can be achieved by simply executing the file using your IDE. Otherwise, in case of an IDE you can
     execute the following command line argument using after navigating to the project root directory.
        ```bash
        python runner.py
       ```
  2. The other way is to use the behave commandline arguments. Please refer the below example:
     ```bash
     behave application/features --tags=Smoke --define dir=application --define env=dev --format=allure_behave.formatter:AllureFormatter -o allure-result --no-capture
        ```
     This command is necessary to execute the test cases in pipelines or on commandline in the absence of
     a runner file. The corresponding parameter values have to replaced with custom values native to the
     application you intend to test.

- ***Generate Reports***:

     Generation of the allure report happens automatically if the test execution happens through the 
     runner.py file. However, when using the behave bash commands to execute the feature files, the
     results are generated and stored in the allure-result folder, but the report is not generated.
     Generating the reports requires the execution of the following bash command:
       ```bash
       allure generate allure-results/ --clean -o allure-report/
       ```

---

### <u id="reports">Reports:</u>
Allure generates interactive and detailed test execution reports. The reports can be accessed by running the `allure serve` command (see above).

