from django.shortcuts import render
from django.db.models import Q
from .models import Dish
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def search_dishes(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Perform search based on dish names containing the query
        results = Dish.objects.filter(name__icontains=query)

        # If exact match found, prioritize it
        exact_match = results.filter(name__iexact=query).first()
        if exact_match:
            results = [exact_match] + [dish for dish in results if dish != exact_match]

        # Recommend best matches based on similarity
        recommended_results = recommend_best_matches(query)
        
        results = list(set(results) | set(recommended_results))
    print(results)

    return render(request, 'search_results.html', {'results': results, 'query': query})

def recommend_best_matches(query):
    # Using TF-IDF and cosine similarity for recommendation
    dishes = Dish.objects.all()
    dish_names = [dish.name for dish in dishes]

    # Create TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=1, stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(dish_names)

    # cosine similarity calculation
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_vectorizer.transform([query]))

    # indices of top recommendations
    indices = cosine_similarities.argsort().flatten()
    top_indices = indices[-5:][::-1]  # top 5 recommendations

    # Fetch recommended dishes
    recommended_results = [dishes[i] for i in top_indices if cosine_similarities[i] > 0]

    return recommended_results
