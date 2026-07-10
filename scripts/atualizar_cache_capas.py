# Script para atualizar o cache de capas, sempre que novos livros forem adicionados basta executar "python scripts/atualizar_cache_capas.py"
import time
from app.services.api_planilhas import verificar_planilha_de_trabalho
from app.services.capa_cache_service import carregar_cache, obter_aba_cache
from app.services.capa_service import obter_capa

def main():
    print("=" * 60)
    print("Atualização do cache de capas")
    print("=" * 60)
    
    aba_livro = verificar_planilha_de_trabalho("Livro")
    livros = aba_livro.get_all_records()
    
    cache = carregar_cache()
    print(f"Entradas em cache: {len(cache)}")
    aba_cache = obter_aba_cache()
    
    total = len(livros)
    processados = 0
    ignorados = 0
    
    for livro in livros:
        isbn = str(livro.get("ISBN", "")).strip()
        
        if not isbn:
            ignorados += 1
            continue
        
        if isbn in cache:
            ignorados += 1
            continue
        
        titulo = livro.get("titulo", "Sem titulo")
        print(f"Processando: {titulo}")
        
        obter_capa(
            isbn,
            cache,
            aba_cache
        )
        
        registro = cache.get(isbn)
        print(
            f"   -> {registro['fonte']} ({registro['status']})"
        )
        
        processados += 1
        
        time.sleep(0.15)
        
    print()
    print("=" * 60)
    print("Resumo")
    print("=" * 60)
    print(f"Livros encotrados : {total}")
    print(f"Novos processados : {processados}")
    print(f"Já em cache       : {ignorados}")
    print(f"cache final       : {len(cache)} ISBNs")
    
if __name__ == "__main__":
    main()