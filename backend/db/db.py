from sqlalchemy import create_engine, text

DB_URI = "postgresql+psycopg2://postgres:1234@localhost:5432/redot"

def criar_banco():
    try:
        with open('db/scripts.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        engine = create_engine(DB_URI)
        with engine.connect() as conn:
            conn.execute(text(sql_script))
            
        return True
    except Exception as e:
        print(f"❌ Erro ao criar banco: {str(e)}")
        return False

if __name__ == "__main__":
    criar_banco()