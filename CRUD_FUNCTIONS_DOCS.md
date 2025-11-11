# 📚 Novas Funções CRUD - Histórico de Livros do Usuário

## Resumo das Adições

Adicionadas 5 novas funções ao `crud.py` para recuperar o histórico de interações do usuário com livros (likes, dislikes, cliques).

---

## 📖 Funções Adicionadas

### 1. `get_user_liked_books(db, user_id)`

Retorna **lista de livros** que o usuário deu like.

```python
def get_user_liked_books(db: Session, user_id: int) -> List[models.Book]:
    """List all books liked by a user"""
```

**Uso:**
```python
liked_books = crud.get_user_liked_books(db, user_id=1)
for book in liked_books:
    print(f"📗 {book.title} - {book.authors}")
```

**Retorna:**
- Lista de objetos `Book` que o usuário deu like
- Vazio se não houver likes

---

### 2. `get_user_disliked_books(db, user_id)`

Retorna **lista de livros** que o usuário deu dislike.

```python
def get_user_disliked_books(db: Session, user_id: int) -> List[models.Book]:
    """List all books disliked by a user"""
```

**Uso:**
```python
disliked_books = crud.get_user_disliked_books(db, user_id=1)
for book in disliked_books:
    print(f"👎 {book.title}")
```

**Retorna:**
- Lista de objetos `Book` que o usuário deu dislike
- Vazio se não houver dislikes

---

### 3. `get_user_clicked_books(db, user_id)`

Retorna **lista de livros** que o usuário clicou (sem duplicatas).

```python
def get_user_clicked_books(db: Session, user_id: int) -> List[models.Book]:
    """List all books clicked by a user"""
```

**Uso:**
```python
clicked_books = crud.get_user_clicked_books(db, user_id=1)
for book in clicked_books:
    print(f"🔗 {book.title}")
```

**Retorna:**
- Lista de objetos `Book` únicos que o usuário clicou
- Vazio se não houver cliques

---

### 4. `get_user_liked_books_with_events(db, user_id)`

Retorna **pares (Book, Event)** de livros com like (mais informações detalhadas).

```python
def get_user_liked_books_with_events(db: Session, user_id: int) -> List[tuple]:
    """List all books liked by a user with their event data (book, event)"""
```

**Uso:**
```python
liked_with_events = crud.get_user_liked_books_with_events(db, user_id=1)
for book, event in liked_with_events:
    print(f"📗 {book.title}")
    print(f"   Reward: {event.reward}")
    print(f"   Timestamp: {event.timestamp}")
    print(f"   Slate ID: {event.slate_id}")
```

**Retorna:**
- Lista de tuples: `(Book, Event)`
- Inclui dados do evento (reward, timestamp, slate_id, pos, etc)

---

### 5. `get_user_disliked_books_with_events(db, user_id)`

Retorna **pares (Book, Event)** de livros com dislike (mais informações detalhadas).

```python
def get_user_disliked_books_with_events(db: Session, user_id: int) -> List[tuple]:
    """List all books disliked by a user with their event data (book, event)"""
```

**Uso:**
```python
disliked_with_events = crud.get_user_disliked_books_with_events(db, user_id=1)
for book, event in disliked_with_events:
    print(f"👎 {book.title}")
    print(f"   Reward: {event.reward}")
    print(f"   Position: {event.pos}")
```

**Retorna:**
- Lista de tuples: `(Book, Event)`
- Inclui dados completos do evento

---

## 🎯 Casos de Uso

### Streamlit - Página de Likes
```python
# pages/Likes.py
import crud

liked_books = crud.get_user_liked_books(db, st.session_state.user_id)

for book in liked_books:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"📗 **{book.title}**")
        st.caption(f"por {book.authors}")
    with col2:
        if st.button("Remover", key=f"remove_{book.id}"):
            # lógica de remoção
```

### FastAPI - Endpoint de Histórico
```python
# app/api/routes.py
@router.get("/api/users/{user_id}/liked-books")
def get_liked_books(user_id: int, db: Session = Depends(get_db)):
    books = crud.get_user_liked_books(db, user_id)
    return {"liked_books": [book.dict() for book in books]}
```

### Análise Offline - Jupyter Notebook
```python
# Contar likes/dislikes por usuário
liked_count = len(crud.get_user_liked_books(db, user_id=1))
disliked_count = len(crud.get_user_disliked_books(db, user_id=1))

print(f"User 1: {liked_count} likes, {disliked_count} dislikes")
```

---

## 📊 Comparação de Funções

| Função | Retorna | Inclui Event | Uso |
|--------|---------|-------------|-----|
| `get_user_liked_books` | `List[Book]` | ❌ | UI simples |
| `get_user_disliked_books` | `List[Book]` | ❌ | UI simples |
| `get_user_clicked_books` | `List[Book]` | ❌ | UI simples |
| `get_user_liked_books_with_events` | `List[tuple]` | ✅ | Analytics |
| `get_user_disliked_books_with_events` | `List[tuple]` | ✅ | Analytics |

---

## 🔍 Exemplos Completos

### Exemplo 1: Dashboard de Usuário
```python
def show_user_dashboard(user_id: int):
    db = SessionLocal()
    
    # Obter estatísticas
    liked = crud.get_user_liked_books(db, user_id)
    disliked = crud.get_user_disliked_books(db, user_id)
    clicked = crud.get_user_clicked_books(db, user_id)
    
    print(f"Likes: {len(liked)}")
    print(f"Dislikes: {len(disliked)}")
    print(f"Cliques: {len(clicked)}")
    
    db.close()
```

### Exemplo 2: Export para CSV
```python
import pandas as pd

def export_user_history(user_id: int, filename: str):
    db = SessionLocal()
    
    liked_with_events = crud.get_user_liked_books_with_events(db, user_id)
    
    data = []
    for book, event in liked_with_events:
        data.append({
            'Book ID': book.id,
            'Title': book.title,
            'Authors': book.authors,
            'Action': 'LIKE',
            'Reward': event.reward,
            'Timestamp': event.timestamp
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
    db.close()
```

### Exemplo 3: Recomendações Baseadas em Histórico
```python
def get_recommendations_based_on_likes(user_id: int, limit: int = 10):
    db = SessionLocal()
    
    # Obter livros que o usuário gostou
    liked_books = crud.get_user_liked_books(db, user_id)
    
    if not liked_books:
        # Se não há likes, retornar livros populares
        return crud.get_all_books(db, limit=limit)
    
    # Buscar livros similares (mesmas categorias)
    liked_categories = set()
    for book in liked_books:
        if book.categories:
            liked_categories.update(book.categories.split(','))
    
    # Filtrar livros similares que ainda não foram marcados
    liked_ids = {b.id for b in liked_books}
    disliked_ids = {b.id for b in crud.get_user_disliked_books(db, user_id)}
    
    similar_books = [
        b for b in crud.get_all_books(db, limit=limit * 2)
        if b.id not in (liked_ids | disliked_ids) and
           any(cat.strip() in b.categories for cat in liked_categories if b.categories)
    ]
    
    db.close()
    return similar_books[:limit]
```

---

## ✅ Checklist de Funcionalidades

- ✓ Lista livros com like
- ✓ Lista livros com dislike
- ✓ Lista livros com click
- ✓ Inclui dados de evento (detalhado)
- ✓ Integração com modelos SQLAlchemy
- ✓ Tipagem completa (type hints)
- ✓ Docstrings em inglês
- ✓ Pronto para uso em Streamlit/FastAPI

---

## 🚀 Próximos Passos

1. Integrar com Streamlit (páginas Likes.py, Dislikes.py)
2. Criar endpoints FastAPI para essas funcionalidades
3. Adicionar paginação para grandes volumes de dados
4. Implementar filtros por data/período
5. Adicionar caching/performance optimization

