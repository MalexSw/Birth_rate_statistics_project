import sys
import matplotlib
import calculations as calc
import fileRead as fileRead
from InquirerPy import inquirer

if sys.stdout.isatty():
    matplotlib.use('TkAgg')
else:
    matplotlib.use('Agg')


def run():
    while True:
        choice = inquirer.select(
            message="📊 What do you want to do?",
            choices=[
                "1. Check birthes amount over years",
                "2. Check birthes rate by countries",
                "3. Table options",
                "4. Check a hypothesis",
                "5. Exit",
            ],
            pointer="👉",
            instruction="Use arrows ↑↓ and Enter ⏎"
        ).execute()

        if choice.startswith("1"):
            print("👉 You selected: Check birthes amount over years")
            births_per_year = fileRead.readFileBirthesOverYears()
            calc.weightOverYears(births_per_year)

        elif choice.startswith("2"):
            print("👉 You selected: Check birthes rate by countries")

            births_by_countries = fileRead.readFileBirthCountsByCountry()
            available_countries = sorted(fileRead.findCountries(births_by_countries))

            selected_countries = inquirer.checkbox(
                message="✅ Select countries to compare:",
                choices=available_countries,
                pointer="👉",
                instruction="Use spacebar to select, Enter to confirm"
            ).execute()

            if selected_countries:
                calc.countriesComparing(births_by_countries, selected_countries)
            else:
                print("⚠️ No countries selected.")

        elif choice.startswith("3"):
            table_choice = inquirer.select(
                message="🔢 Which table do you want?",
                choices=[
                    "1. Clean and Plot",
                    "2. Normal Plot",
                ],
                pointer="👉",
                instruction="Use arrows ↑↓ and Enter ⏎"
            ).execute()

            birth_counts = fileRead.readFileBirthCounts()

            if table_choice.startswith("1"):
                print("👉 You selected: Clean and Plot")
                calc.clean_and_plot_birth_counts(birth_counts)
            else:
                print("👉 You selected: Normal Plot")
                calc.birth_counts(birth_counts)

        elif choice.startswith("4"):
            print("👉 You selected: Hypothesis Testing")

            df = fileRead.readFileBirthCountsByCountry()
            available_countries = sorted(fileRead.findCountries(df))

            selected = inquirer.checkbox(
                message="✅ Select exactly 2 countries to compare:",
                choices=available_countries,
                pointer="👉",
                instruction="Use spacebar to select, Enter to confirm"
            ).execute()

            if len(selected) != 2:
                print("⚠️ Please select exactly two countries.")
                continue

            # Hypothesis direction selection
            hypothesis_choices = [
                "Two-sided (≠)",
                "Greater than (>)",
                "Less than (<)"
            ]
            selected_test = inquirer.select(
                message="📈 Type of test:",
                choices=hypothesis_choices,
                pointer="👉",
                instruction="Choose a hypothesis direction (↑↓ + ⏎)"
            ).execute()

            test_mapping = {
                "Two-sided (≠)": "two-sided",
                "Greater than (>)": "greater",
                "Less than (<)": "less"
            }

            alternative = test_mapping.get(selected_test)
            if alternative is None:
                print(f"⚠️ Invalid test type: '{selected_test}', defaulting to 'two-sided'")
                alternative = "two-sided"

            # Significance level input
            alpha_input = inquirer.text(
                message="📉 Enter significance level (e.g., 0.05 for 5%):",
                default="0.05"
            ).execute()

            try:
                alpha = float(alpha_input)
            except ValueError:
                print("⚠️ Invalid alpha. Defaulting to 0.05")
                alpha = 0.05

            result = calc.check_mean_difference(
                df=df,
                metric="OBS_VALUE",
                group_col="geo",
                group1=selected[0],
                group2=selected[1],
                alternative=alternative,
                alpha=alpha
            )

            print("\n🧪 Hypothesis Test Result:")
            print(calc.interpret_result(result))
            print(f"Group {selected[0]} mean: {result['group1_mean']:.2f}")
            print(f"Group {selected[1]} mean: {result['group2_mean']:.2f}")
            print(f"T-statistic: {result['t_statistic']:.4f}")
            print(f"P-value: {result['p_value']:.4f}")
            print()

        elif choice.startswith("5"):
            print("👋 Exiting the program. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    run()
