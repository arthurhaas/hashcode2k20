#!/usr/bin/env python
# coding: utf-8

# In[183]:


import pandas as pd
import numpy as np
import math
import os


# In[184]:


OUTPUT_FOLDER = 'output'


# In[185]:


def input(path):
    
    f = open(path, "r")
    lines = f.readlines()
    f.close()

    [num_books, num_lib, num_days] = map(lambda x: int(x), lines[0].rstrip('\n').split(' '))
    scores = list(map(lambda x: int(x), lines[1].rstrip('\n').split(' ')))
    print("Number of books:", num_books)
    print("Number of librarys:", num_lib)
    print("Number of day:", num_days)

    mat_lib = np.zeros((num_lib, 3))
    book_lib_list = []
    for n in range(2, num_lib * 2 + 2, 2):
        [num_books_tot, num_su_days, num_book_days] = map(lambda x: int(x),lines[n].rstrip('\n').split(' '))
        mat_lib[int(((n/2)-1)),0] = num_books_tot
        mat_lib[int(((n/2)-1)),1] = num_su_days
        mat_lib[int(((n/2)-1)),2] = num_book_days
        list_books = list(map(int,lines[n+1].rstrip('\n').split(' ')))
        list_books.sort()
        book_lib_list.append(list_books)


    df_libs = pd.DataFrame(mat_lib, columns=["num_books","reg_time","shipping_num"])
    return num_books, num_lib, num_days, scores, df_libs, book_lib_list


# In[186]:


def score_lib(reg_days, scaled_book_score, scaled_book_per_day, scaled_books_tot):
    a = 0.01
    b = 1/3
    c = 1/3
    d = 1/3
    return math.exp(-a*reg_days)*(b*scaled_book_score + c*scaled_book_per_day + d*scaled_books_tot)


# In[187]:


def exract_used_books(df):
    used_books = set()
    
    list(df[df.used == 1].index)
    
    return #set


# In[203]:


def solve(num_books, num_libs, num_days, scores, df_libs, books_with_scores):
    remaining_days = 10
    used_books = set()
    solution = []


    #prepare_dataframe(df_libs, books_with_scores)
    while (remaining_days >= 0) and (df_libs[df_libs.used == 0].shape[0] > 0):
        
        # 1. Unbenutze Librarys auswählen
        df_tmp = df_libs[df_libs.used == 0].copy()

        # 2. Bücher subtrahieren
        tmp_books_with_scores = []
        scores_by_lib = []
        for i, library in enumerate(books_with_scores):
            lib_books_with_scores = []
            tmp_score = 0
            for book in library:
                if book[0] not in used_books:
                    lib_books_with_scores.append(book)
                    tmp_score += book[1]
            tmp_books_with_scores.append(lib_books_with_scores)
            scores_by_lib.append(tmp_score)
           
        # MVP todo
        # 4. Bücher ab aktuellem Datum - registration abschneiden !!! books per day mit einbeziehen
            #(num_days - reg_days - passed_days)*shipping_num
        """
        total_scores_by_library = []
        for i, library in enumerate(books_with_scores):
            score = 0
            
            lib_remaining_days = 
            for book in library:
                #filtering by not used books
                if book[0] not in used_books:
                    lib_books_with_scores.append(book)
                

        """
        
        max_books_score_by_lib = max(scores_by_lib)
        max_shipping_num = df_tmp.shipping_num.max()
        max_num_books = df_tmp.num_books.max()
        

        # 5. Score berechnen.
        for index, row in df_tmp.iterrows():
            reg_days = row['reg_time']
            scaled_book_score = scores_by_lib[index] / max_books_score_by_lib
            scaled_book_per_day = row['shipping_num'] / max_shipping_num
            scaled_books_tot = row['num_books'] / max_num_books
            df_tmp.loc[index,'score'] = score_lib(reg_days, scaled_book_score, scaled_book_per_day, scaled_books_tot)
        
        # gather max score
        df_tmp.score.max()
        
        # todo - case of multiple libraries with same score
        idx = df_tmp.index[(df_tmp.score == df_tmp.score.max()) & (df_tmp.used == 0.0)].values[0]
        df_libs.iloc[idx, df_libs.columns.get_loc('used')] = 1
        
        # todo
        solution_first_row = ' '.join(str(x) for x in [idx, len(tmp_books_with_scores[idx])])
        solution_second_row = ' '.join(str(x) for x in [book[0] for book in tmp_books_with_scores[idx]])
        solution.append(solution_first_row + '\n' + solution_second_row)
        
        # todo
        # reduce tmp_books_with_scores
        used_books.update(set([book[0] for book in tmp_books_with_scores[idx]]))
        # todo 
        remaining_days -= 1
        

    return solution

# Tage die noch übrig bleiben


# In[200]:


def generate_book_tuples(books, scores):
    """
    returns: [(book_id, book_scores)]
    """
    tupel_list = []
    for book in books:
        tupel_list.append((book, scores[book]))
    
    return sorted(tupel_list, key=lambda tup: tup[1], reverse=True)


# In[201]:


def output(solutions, path):
    """Cleaning and output"""

    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    f = open(path, "w")
    f.write(str(len(solutions)) + "\n")
    f.write('\n'.join(str(library) for library in solutions))
    f.close()


# In[204]:


if __name__ == '__main__':
    paths = ["data/a_example.txt",
                "data/b_read_on.txt",
                #"data/c_incunabula.txt",
                "data/d_tough_choices.txt",
                "data/e_so_many_books.txt",
                "data/f_libraries_of_the_world.txt"]

    for path in paths:
        print("processing file {}".format(path))
        
        # import
        num_books, num_libs, num_days, scores, df_libs, book_list = input(path)

        # preprocessing
        print('-- preprocessing')
        books_with_scores = []
        for books in book_list:
            books_with_scores.append(generate_book_tuples(books, scores))
        df_libs['used'] = np.zeros(num_libs)
        df_libs['score'] = 0

        print('-- start solver')
        solution = solve(num_books, num_libs, num_days, scores, df_libs, books_with_scores)

        print('-- output')
        output_path = os.path.join(OUTPUT_FOLDER, path.split('/')[1])
        output(solution, output_path)
        
        print("")
