import os

db_path = 'queen_memory.db'

if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Arquivo {db_path} removido com sucesso.")
else:
    print(f"Arquivo {db_path} não encontrado.")


