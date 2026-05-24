import subprocess


# Step 1: Run behave with allure output
subprocess.run([
    "python",
    "-m",
    "behave",
    "features",
    "-f",
    "allure_behave.formatter:AllureFormatter",
    "-o",
    "reports/allure-results"
])


# Step 2: Generate report
subprocess.run([
    "allure",
    "generate",
    "reports/allure-results",
    "-o",
    "reports/allure-report",
    "--clean"
])


# Step 3: Open report (better than open → use serve optionally)
subprocess.run([
    "allure",
    "serve",
    "reports/allure-results"
])