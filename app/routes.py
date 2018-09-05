from datetime import datetime
import json

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.models import User, Post, Job
from flask import g
from app.forms import SearchForm

from flask import g

@app.before_request
def search_form():
	g.search_form = SearchForm()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/jobs')
def jobs():
	company = [r.company for r in db.session.query(Job.company).distinct()]
	jobs = Job.query
	job_count = {co:len(jobs.filter_by(company = co).all()) for co in company}

	return render_template('jobs.html', title = 'Jobs', jobs = jobs, job_counts = job_count, companies = company)

@app.route('/search', methods=['GET', 'POST'])
def search():
	if not g.search_form.validate():
		return redirect(url_for('jobs'))
	jobs_results, total = Job.search(g.search_form.q.data)

	return render_template('search.html', title=('Search'), jobs_results=jobs_results, total=total)


@app.route('/learn', methods=['GET'])
def landing():
	#just a landing
	return render_template('learn.html', title='Learn')

@app.route('/visualize', methods=['GET'])
def visualize():
	#just a visualize
	return render_template('visualize.html', title='visualize')