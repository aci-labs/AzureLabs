# Fabric Capacity Management

This folder contains the code and documentation for managing Microsoft Fabric Capacity of in Azure.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

In this project, I aim to provide a solution for effectively managing a Fabric Capacity  in Azure, by automating Suspend and Resume of the capacity via Azure Automation Accounts.

## Installation

To use this project, you will need to have the following prerequisites:

- Azure subscription (or more) containing the capacities you want to manage.
- A Microsoft Entra ID service principal with Reader rights on subscriptions containing the capacities and Contributor rights on the Capacities themselves
- Python 3.8 or higher


Follow these steps to install and configure the project:

1. Clone the repository: `git clone https://github.com/your-username/fabric-capacity-management.git`
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage

To use this project, follow these steps:

For local testing:

1. Open a terminal and navigate to the project directory.
2. Update the scripts: `ResumeCapacity.py` and `SuspendCapacity.py` with the correct details by commenting out the lines 10-14 and 20-23 and uncommenting the lines 17-19.
3. Run the script: `python ResumeCapacity.py` or `python SuspendCapacity.py`

For using the scripts inside an Azure Automation Account:

1. Either manually create an Azure Automation Account following [these steps](https://learn.microsoft.com/en-us/azure/automation/quickstarts/create-azure-automation-account-portal).
2. Or use the [Azure Resource Manager template](./AutomationAccountTemplate/template.json) to create an Azure Automation Account.
2. Update the variables in the automation account with the correct details.
3. Check the `Runbook` section of the automation account to see the list of runbooks.
4. Check the `Python Packages` are imported correctly, if not, import them manually using the list of packages in the [requirements.txt](./AutomationAccountTemplate/requirements.txt) file.
5. Test your runbooks by clicking on the `Test Pane`.


## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the [GNU License](../LICENSE).