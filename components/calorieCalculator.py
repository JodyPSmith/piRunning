def calculate_calories_burned(gender, age_years, weight_kgs, heart_rate_bpm, time_min):
    """
    Calculates estimated calories burned during a workout based on gender-specific formulas.

    Args:
        gender (str): 'male' or 'female'.
        age_years (int): Age in years.
        weight_lbs (float): Weight in pounds.
        heart_rate_bpm (int): Average heart rate during the workout in beats per minute.
        time_min (float): Duration of the workout in minutes.

    Returns:
        float: Estimated calories burned.
    """
    if gender.lower() == 'male':
        # Formula for men
        calories = ((age_years * 0.2017) + (weight_kgs * 0.1988) + (heart_rate_bpm * 0.6309) - 55.0969) * (time_min / 4.184)
    elif gender.lower() == 'female':
        # Formula for women
        calories = ((age_years * 0.074) - (weight_kgs * 0.12631) + (heart_rate_bpm * 0.4472) - 20.4022) * (time_min / 4.184)
    else:
        raise ValueError("Invalid gender. Please enter 'male' or 'female'.")
    return calories

# Example usage:
# try:
#     gender = input("Enter gender (male/female): ")
#     age = int(input("Enter age in years: "))
#     weight = float(input("Enter weight in pounds: "))
#     heart_rate = int(input("Enter average heart rate during workout (bpm): "))
#     time = float(input("Enter workout duration in minutes: "))

#     calories_burned = calculate_calories_burned(gender, age, weight, heart_rate, time)
#     print(f"Estimated calories burned: {calories_burned:.2f} calories")

# except ValueError as e:
#     print(f"Error: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")