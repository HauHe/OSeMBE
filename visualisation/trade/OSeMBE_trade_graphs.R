require("reticulate")

source_python("read_pkl.py")
pickle_data <- read_pickle_file("data/OSeMBE_ProductionByTechnologyAnnual_DataV3R1_2020-03-24.pkl")
