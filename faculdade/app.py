from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados "pré-populado" com alguns livros
books = [
    {'id': 1, 'title': 'O Pequeno Príncipe', 'author': 'Antoine de Saint-Exupéry', 'price': 29.90, 'category': 'Infantil'},
    {'id': 2, 'title': 'Dom Casmurro', 'author': 'Machado de Assis', 'price': 49.90, 'category': 'Romance'},
    {'id': 3, 'title': 'Harry Potter e a Pedra Filosofal', 'author': 'J.K. Rowling', 'price': 39.90, 'category': 'Fantasia'},
    {'id': 4, 'title': 'Divina Comédia', 'author': 'Dante Alighieri', 'price': 29.90, 'category': 'Poesia'},
    {'id': 5, 'title': 'Palido Ponto Azul', 'author': 'Carl Sagan', 'price': 19.90, 'category': 'Cientifico'},
    {'id': 6, 'title': 'Senhor Dos Anéis', 'author': 'J.R.R. Tolkien', 'price': 59.90, 'category': 'Fantasia'},
]

book_id_counter = 7  # Começamos do 7, já que temos 6 livros criados


# Rota principal: lista de livros
@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    selected_category = request.args.get('category', '').lower()

    filtered_books = books

    if search_query:
        filtered_books = [b for b in filtered_books if b['title'].lower().startswith(search_query)]

    if selected_category:
        filtered_books = [b for b in filtered_books if selected_category == b['category'].lower()]

    # Extrair lista única de categorias
    categories = sorted(set(book['category'] for book in books))
    return render_template('index.html', books=filtered_books, categories=categories)


# Rota para criar novo livro
@app.route('/create', methods=['GET', 'POST'])
def create():
    global book_id_counter
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = float(request.form['price'])
        category = request.form['category']


        # Verificar se já existe um livro com o mesmo título
        if any(book['title'].lower() == title.lower() for book in books):
            error = "Já existe um livro com este título!"
            return render_template('create.html', error=error)

        books.append({'id': book_id_counter,
                      'title': title,
                      'author': author,
                      'price': price,
                      'category': category})
        book_id_counter += 1
        return redirect(url_for('index'))

    return render_template('create.html')


# Rota para editar livro
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = next((b for b in books if b['id'] == id), None)
    if book is None:
        return "Livro não encontrado", 404

    if request.method == 'POST':
        book['title'] = request.form['title']
        book['author'] = request.form['author']
        book['price'] = float(request.form['price'])
        book['category'] = request.form['category']
        return redirect(url_for('index'))

    return render_template('edit.html', book=book)

# Rota para deletar livro
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    global books
    books = [b for b in books if b['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
