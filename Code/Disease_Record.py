class Disease_Record:

    def __init__(self, year, state, topic, question, data_value,
                 data_value_unit, data_value_type, stratification):
        self.year = year
        self.state = state
        self.topic = topic
        self.question = question
        self.stratification = stratification


        self.data_value = data_value
        self.data_value_unit = data_value_unit
        self.data_value_type = data_value_type


    def is_valid(self):

        if self.data_value is None:
            return False

            # this if statement works because NA values aren't equal to themselves
        if self.data_value != self.data_value:
            return False
        return True
    def short_label(self):

        return f"{self.state} - {self.year} - {self.topic}"

    def __str__(self):
        if self.is_valid():
            text = f"{self.data_value:.2f} {self.data_value_unit} {self.data_value_type}"
        else:
            text = "No Data"
        return (f"[{self.year}] {self.state} | {self.topic} | "
                f"{self.stratification} -> {text}")

    def to_dict(self):
        return {
            "year": self.year,
            "state": self.state,
            "topic": self.topic,
            "question": self.question,
            "stratification": self.stratification,
            "data_value": self.data_value,
            "data_value_unit": self.data_value_unit,
            "data_value_type": self.data_value_type,
        }