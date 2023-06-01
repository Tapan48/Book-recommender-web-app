from flask import Flask, render_template,request
import pandas as pd
import pickle


popular_df=pickle.load(open('popular.pkl','rb'))

pt=pickle.load(open('pt.pkl','rb'))                          
books=pickle.load(open('books.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
   
  
    
    # Pass your DataFrame to the template
    return render_template('index.html')

@app.route('/recommend_page')

def recommend_page():
    return render_template("recommend.html")

@app.route('/recommend_books',methods=["post"])

def recommend_book():
    
    searched_book=request.form.get("user_input")
    book_title_index = pt.index.get_loc(searched_book)       ## gets the index of bookname in pt table
    similar_books=sorted(list(enumerate(similarity[book_title_index])),key=lambda x:x[1],reverse=True)[1:6] 
    ### using that index we go in the similarity scores array to get the similarity scores of that particular book
    
    recommendedbooks=[]
    for item in similar_books:     ## (index,similarity_score)
        
        book=[]
        
        temp_df=books[books["Book-Title"]==pt.index[item[0]]]         ####   book name,book author, book image
        book.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        book.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        book.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))
        
        recommendedbooks.append(book)
        
    return render_template("recommend.html", recommendedbooks=recommendedbooks, searched_book=searched_book)

    



if __name__ == '__main__':
    app.run(debug=True)
