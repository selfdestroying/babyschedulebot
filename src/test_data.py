from models.Child import Child

test_user = {
    "name": "John",
    "phone": "+7 999 999 99 99",
    "email": "qVQp5@example.com",
    "child": Child(name="Mary", gender="Девочка", age="7", food_type="breast"),
    "schedule": {
        "28.01": {
            "start_night_sleep_time": "22:00",
            "end_night_sleep_time": "09:00",
            "night_duration": 660,
            "night_rating": 3,
            "sleeps": [
                {
                    "start_sleep_time": "12:00",
                    "end_sleep_time": "13:00",
                    "sleep_duration": 60,
                },
                {
                    "start_sleep_time": "16:00",
                    "end_sleep_time": "17:00",
                    "sleep_duration": 60,
                },
                {
                    "start_sleep_time": "19:00",
                    "end_sleep_time": "20:00",
                    "sleep_duration": 60,
                },
            ],
        }
    },
}
