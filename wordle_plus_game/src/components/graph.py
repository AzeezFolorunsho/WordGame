import matplotlib.pyplot as plt

class LineGraph:
    def __init__(self):
        pass

    def create_graph(self, data):
        # Organizing data by difficulty levels
        difficulty_levels = {}
        for entry in data:
            difficulty = entry['Difficulty']
            if difficulty not in difficulty_levels:
                difficulty_levels[difficulty] = {'Score': [], 'Time': []}
            difficulty_levels[difficulty]['Score'].append(entry['Score'])
            difficulty_levels[difficulty]['Time'].append(entry['Time'])

        # Plotting the line graphs
        plt.figure(figsize=(10, 6))
        for difficulty, values in difficulty_levels.items():
            plt.plot(values['Time'], values['Score'], marker='o', label=f"{difficulty} Level")
        plt.title("Score vs. Time for Different Difficulty Levels")
        plt.xlabel("Time")
        plt.ylabel("Score")
        plt.legend(title="Difficulty Levels")
        plt.grid(True)
        plt.show()