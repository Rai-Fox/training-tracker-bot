class GoalCalculator:
    def calculate_user_calories_goal(self, user_data):
        weight = user_data["weight"]
        height = user_data["height"]
        age = user_data["age"]
        activity_time = user_data["activity"]
        gender = user_data["gender"]

        if gender == "мужской":
            calories_goal = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            calories_goal = 10 * weight + 6.25 * height - 5 * age - 161

        calories_goal *= self.calculate_activity_coef(activity_time)

        return calories_goal

    def calculate_activity_coef(self, activity_time):
        if activity_time < 30:
            return 1.2
        elif activity_time < 60:
            return 1.375
        elif activity_time < 90:
            return 1.55
        elif activity_time < 120:
            return 1.725
        else:
            return 1.9

    def calculate_user_water_goal(self, user_data, current_temp):
        weight = user_data["weight"]
        activity_time = user_data["activity"]

        water_goal = weight * 30 + activity_time * 500 / 30

        if current_temp < 25:
            pass
        elif current_temp < 30:
            water_goal += 500
        elif current_temp < 35:
            water_goal += 750
        else:
            water_goal += 1000

        return water_goal
