
# Uni-portal

This repository contains the code for the Uni-portal application. This README provides instructions on how to set up the environment and run the application using Conda.

## Prerequisites

* **Conda:** You need to have Conda installed on your system. If you don't have Conda, you can install Miniconda or Anaconda Distribution by following the instructions on the official Conda documentation: [https://docs.conda.io/en/latest/user-guide/install/index.html](https://docs.conda.io/en/latest/user-guide/install/index.html)

## Setup

1.  **Clone the repository:**

    Open your terminal or command prompt and clone the repository using the following command:

    ```bash
    git clone [https://github.com/SkaarFacee/Uni-portal.git](https://github.com/SkaarFacee/Uni-portal.git)
    ```

2.  **Navigate to the repository directory:**

    Change your current directory to the cloned repository:

    ```bash
    cd Uni-portal
    ```

3.  **Create a Conda environment:**

    Create a new Conda environment named `uni-portal-env` with Python version 3.12.

    ```bash
    conda create -n uni-portal-env python=3.12
    ```

    When prompted to proceed, type `y` and press Enter.

4.  **Activate the Conda environment:**

    Activate the newly created environment:

    ```bash
    conda activate uni-portal-env
    ```

    Your terminal prompt should now show `(uni-portal-env)` at the beginning, indicating that you are in the activated environment.

5.  **Install dependencies:**

    Navigate to the cloned repository directory (if you are not already there) and install any necessary dependencies. It is assumed that there might be a `requirements.txt` file in the repository. If there is, run:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Ensure the Conda environment is activated:**

    If you have closed your terminal or deactivated the environment, activate it again:

    ```bash
    conda activate uni-portal-env
    ```

2.  **Run the main file:**

    Execute the `cli.py` file using the Python interpreter from your activated environment:

    ```bash
    python cli.py
    ```

This will start the Uni-portal application. Follow any on-screen instructions provided by the application.
