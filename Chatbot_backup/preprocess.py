import json
import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import logging

# Setup logging
logging.basicConfig(
    filename='pre_processing.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def load_and_preprocess(json_file):
    """
    Load JSON data and preprocess by splitting multiple questions.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.info(f"Loaded data from {json_file}")
    except Exception as e:
        logging.error(f"Error loading JSON file: {e}")
        raise e

    question_intent_map = []
    for entry in data:
        # Manually split questions by " OR " surrounded by spaces (case-insensitive)
        questions = re.split(r'\s+OR\s+', entry['question'], flags=re.IGNORECASE)
        questions = [q.strip().lower() for q in questions if q.strip()]

        for question in questions:
            question_intent_map.append({
                'question': question,
                'intent': entry['intent'],
                'sub_intent': entry['sub_intent'],
                'responses': entry['responses']
            })
    logging.info(f"Preprocessed data into {len(question_intent_map)} individual questions")
    return question_intent_map

def generate_embeddings(questions, model_name='all-mpnet-base-v2'):
    """
    Generate embeddings for a list of questions using SentenceTransformer.
    """
    try:
        model = SentenceTransformer(model_name)
        embeddings = model.encode(questions, convert_to_numpy=True, show_progress_bar=True)
        logging.info(f"Generated embeddings using {model_name}")
    except Exception as e:
        logging.error(f"Error generating embeddings: {e}")
        raise e
    return embeddings

def create_faiss_index(embeddings, index_file='faiss_index.bin'):
    """
    Create a FAISS index from embeddings and save it to a file.
    """
    try:
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)  # Simple L2 index
        index.add(embeddings)
        faiss.write_index(index, index_file)
        logging.info(f"FAISS index created and saved to {index_file}")
    except Exception as e:
        logging.error(f"Error creating FAISS index: {e}")
        raise e
    return index

def save_mapping(question_intent_map, mapping_file='index_mapping.json'):
    """
    Save the mapping from index to intent, sub-intent, and responses.
    """
    try:
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(question_intent_map, f, indent=4)
        logging.info(f"Mapping file saved to {mapping_file}")
    except Exception as e:
        logging.error(f"Error saving mapping file: {e}")
        raise e

def main():
    json_file = 'question_bank.json'  # Replace with your actual JSON file name
    faiss_index_file = 'faiss_index.bin'
    mapping_file = 'index_mapping.json'

    # Step 1: Load and preprocess data
    question_intent_map = load_and_preprocess(json_file)
    
    # Step 2: Generate embeddings
    questions = [item['question'] for item in question_intent_map]
    embeddings = generate_embeddings(questions)
    
    # Step 3: Create FAISS index
    create_faiss_index(embeddings, faiss_index_file)
    
    # Step 4: Save mapping
    save_mapping(question_intent_map, mapping_file)

    logging.info("Preprocessing completed successfully.")

if __name__ == "__main__":
    main()
