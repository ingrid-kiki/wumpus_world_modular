import pickle
import pandas as pd

# Specify the path to your pickle file
file_path = './results/AG_PyGAD_dict_6x6_e6.pkl' 

try:
    with open(file_path, 'rb') as f:
        # Load the object(s) from the pickle file
        data = pickle.load(f)
    print("Data successfully loaded from pickle file.")
    data_df = pd.DataFrame(data)
    data_df.to_csv("./resultados.csv")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred while loading the pickle file: {e}")
