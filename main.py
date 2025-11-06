from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required # User must be logged in to access
def index():
    return render_template('index.html', user=current_user)

@main_bp.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@main_bp.route('/get_recommendations', methods=['POST'])
@login_required
def get_recs():
    from app import recommender  # Access the initialized service
    from services.image_service import get_game_image_url

    game_title = request.form.get('Name')
    if game_title:
        recommendation_titles = recommender.get_recommendations(game_title)
        if not recommendation_titles:
            return render_template(
                'results.html',
                recommendations=[],
                query=game_title,
                message="Game not found or no recommendations available."
            )
        recommendations_with_images = []
        for title in recommendation_titles:
            image_url = get_game_image_url(title)
            recommendations_with_images.append({'Name': title, 'Header image': image_url})

        return render_template('results.html', recommendations=recommendation_titles, query=game_title)

    return redirect(url_for('main.index'))
