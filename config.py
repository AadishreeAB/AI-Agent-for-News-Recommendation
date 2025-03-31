import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys & Configurations
TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
VECTOR_DB_PATH = "faiss_index"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")












#TOGETHER_AI_API_KEY = "tgp_v1_M_Ga7Af4Ynjmr55kx0Or_79lA0QzuGbRU2BE7-wnqlw"
#VECTOR_DB_PATH = "data/faiss_index"
#asknews api client secret- .P1EHBfH2zhHTWcuI2ygwjSsH7
#asknews client id- 81931c0d-b6c6-4363-840c-069dbb19c3fa
#news api key=ee842b20d9f14aeb92c0428584524746