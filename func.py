from flask import Flask, url_for
from flask import request
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets



class nsempf_moviedbs(db.Model):
    MovieID = db.Column(db.Integer, primary_key=True)
    Movie_name = db.Column(db.String(255))
    Movie_rating = db.Column(db.Integer)
    LeadActor = db.Column(db.String(255))
    Release_date = db.Column(db.Date)
    Director = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    Trivia = db.Column(db.String(255))


class MovieForm(FlaskForm):
    MovieID = IntegerField('MovieID:')
    Movie_name = StringField('Movie:', validators=[DataRequired()])
    Movie_rating = IntegerField('Rating:', validators=[DataRequired()])
    LeadActor = StringField('Lead Actor\'s name: ', validators=[DataRequired()])
    Release_date = DateField('Release date of film: ', validators=[DataRequired()])
    Director = StringField('Dircetor: ', validators=[DataRequired()])
    Description = StringField('Description: ', validators=[DataRequired()])
    Trivia = StringField('Trivia: ', validators=[DataRequired()])

@app.route('/')
def index():
    all_movies = nsempf_moviedbs.query.all()
    return render_template('posts.html', movies = all_movies, pageTitle="CINErate")


    @app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = nsempf_moviedbs.query.filter(or_(nsempf_moviedbs.Movie_name.like(search),
                                                    nsempf_moviedbs.LeadActor.like(search),
                                                    nsempf_moviedbs.Release_date.like(search),
                                                    nsempf_moviedbs.Director.like(search)).all())
        return render_template('library.html', movies=results, pageTitle='CINErate', legend="Search Results")
    else:
        return redirect('/')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        Movie = nsempf_moviedbs(Movie_name=form.Movie_name.data, Movie_rating=form.Movie_rating.data, LeadActor=form.LeadActor.data, Release_date=form.Release_date.data, Director=form.Director.data, Description=form.Description.data, Trivia=form.Trivia.data)
        db.session.add(Movie)
        db.session.commit()

        return redirect('/library')
 
    return render_template('database.html', form=form, pageTitle='CINErate')

@app.route('/delete_movie/<int:MovieID>', methods=['GET','POST'])
def delete_movie(MovieID):
    if request.method == 'POST':
        Movie = nsempf_moviedbs.query.get_or_404(MovieID)
        db.session.delete(Movie)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")


@app.route('/movie/<int:MovieID>', methods=['GET','POST'])
def get_movie(MovieID):
    Movie = nsempf_moviedbs.query.get_or_404(MovieID)
    return render_template('posts.html', form=Movie, pageTitle='Movie Details', legend="Movie Details")


@app.route('/movie/<int:MovieID>/update', methods=['GET', 'POST'])
def update_movie(MovieID):
    Movie = nsempf_moviedbs.query.get_or_404(MovieID)
    form = MovieForm()

    if form.validate_on_submit():
        Movie.Movie_name = form.Movie_name.data
        Movie.Movie_rating = form.Movie_rating.data
        Movie.LeadActor = form.LeadActor.data
        Movie.Release_date = form.Release_date.data
        Movie.Dircetor = form.Director.data
        Movie.Description = form.Description.data
        Movie.Trivia = form.Trivia.data
        db.session.commit()
        return redirect(url_for('get_movie', MovieID=Movie.MovieID))
    form.MovieID.data = Movie.MovieID
    form.Movie_name.data = Movie.Movie_name
    form.Movie_rating.data = Movie.Movie_rating
    form.LeadActor.data = Movie.LeadActor
    form.Release_date.data = Movie.Release_date
    form.Director.data = Movie.Dircetor
    form.Description.data = Movie.Description
    form.Trivia.data = Movie.Trivia
    return render_template('about.html', form=form, pageTitle='Update Movie', legend="Update a movie")



if __name__ == '__main__':
    app.run(debug=True)


